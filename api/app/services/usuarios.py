"""Servicios de gestión de usuarios.

Capa de lógica de negocio para operaciones CRUD de usuarios,
con manejo robusto de excepciones y transacciones."""

import pymysql
from fastapi import HTTPException, status
from app.core.database import get_connection
from app.core.logger import logger
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password

# Whitelist de campos permitidos para actualización
ALLOWED_FIELDS = {
    'nombre_completo', 'correo', 'contrasena', 
    'tipo_documento', 'numero_documento', 'imagen_perfil', 
    'id_rol', 'estado'
}


def obtener_usuarios(skip: int = 0, limit: int = 100, rol: int = None, estado: str = None, query: str = None):
    """Obtiene lista paginada de usuarios con filtros opcionales."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # Base query
            sql = "SELECT u.*, r.nombre_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol WHERE 1=1"
            count_sql = "SELECT COUNT(*) as total FROM usuarios u WHERE 1=1"
            params = []
            
            if rol:
                sql += " AND u.id_rol = %s"
                count_sql += " AND u.id_rol = %s"
                params.append(rol)
            
            if estado:
                sql += " AND u.estado = %s"
                count_sql += " AND u.estado = %s"
                params.append(estado)
                
            if query:
                search_term = f"%{query}%"
                sql += " AND (u.nombre_completo LIKE %s OR u.correo LIKE %s OR u.numero_documento LIKE %s)"
                count_sql += " AND (u.nombre_completo LIKE %s OR u.correo LIKE %s OR u.numero_documento LIKE %s)"
                params.extend([search_term, search_term, search_term])

            # Get Total
            cursor.execute(count_sql, tuple(params))
            total = cursor.fetchone()['total']
            
            # Get Data
            sql += " ORDER BY u.fecha_registro DESC LIMIT %s OFFSET %s"
            data_params = params.copy()
            data_params.extend([limit, skip])
            
            cursor.execute(sql, tuple(data_params))
            data = cursor.fetchall()
            
            return {"total": total, "data": data}
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_usuarios: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar usuarios"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_usuarios: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")


def obtener_usuario_por_id(id_usuario: int):
    """Obtiene un usuario por su ID."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = "SELECT u.*, r.nombre_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol WHERE u.id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchone()
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_usuario_por_id: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar usuario"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_usuario_por_id: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")


def crear_usuario(usuario: UsuarioCreate):
    """Crea un nuevo usuario en el sistema."""
    conn = None
    try:
        conn = get_connection()
        hashed_password = hash_password(usuario.contrasena)
        
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO usuarios (nombre_completo, correo, contrasena, tipo_documento, numero_documento, id_rol, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.nombre_completo, usuario.correo, hashed_password,
                usuario.tipo_documento, usuario.numero_documento, usuario.id_rol, usuario.estado
            ))
            conn.commit()
            logger.info(f"Usuario creado exitosamente: {usuario.correo}")
            return cursor.lastrowid
            
    except pymysql.IntegrityError as e:
        if conn:
            conn.rollback()
        logger.warning(f"Error de integridad al crear usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo o documento ya está registrado"
        )
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de BD en crear_usuario: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear usuario"
        )
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado en crear_usuario: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")


def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    """Actualiza un usuario existente con validación de campos."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            fields = []
            values = []
            
            # Validar y construir query dinámicamente
            for field, value in usuario.dict(exclude_unset=True).items():
                if field not in ALLOWED_FIELDS:
                    raise ValueError(f"Campo no permitido: {field}")
                
                # Hash password si se está actualizando
                if field == 'contrasena' and value:
                    value = hash_password(value)
                    
                fields.append(f"{field}=%s")
                values.append(value)
            
            if not fields:
                logger.warning(f"Intento de actualizar usuario {id_usuario} sin campos")
                return False
                
            values.append(id_usuario)
            sql = f"UPDATE usuarios SET {', '.join(fields)} WHERE id_usuario=%s"
            cursor.execute(sql, tuple(values))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Usuario {id_usuario} actualizado exitosamente")
                return True
            return False
            
    except ValueError as e:
        logger.warning(f"Validación fallida en actualizar_usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except pymysql.IntegrityError as e:
        if conn:
            conn.rollback()
        logger.warning(f"Error de integridad al actualizar usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo o documento ya está registrado"
        )
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de BD en actualizar_usuario: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar usuario"
        )
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado en actualizar_usuario: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")


def eliminar_usuario(id_usuario: int):
    """Elimina un usuario del sistema."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Usuario {id_usuario} eliminado exitosamente")
                return True
            return False
            
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de BD en eliminar_usuario: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar usuario"
        )
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado en eliminar_usuario: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")


def obtener_stats_usuarios():
    """Obtiene estadísticas agregadas de usuarios."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN id_rol = 1 THEN 1 ELSE 0 END) as administradores,
                SUM(CASE WHEN id_rol = 2 THEN 1 ELSE 0 END) as colaboradores,
                SUM(CASE WHEN estado = 'activo' THEN 1 ELSE 0 END) as activos
            FROM usuarios
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            
            return {
                "total": result.get('total', 0) or 0,
                "administradores": int(result.get('administradores', 0) or 0),
                "colaboradores": int(result.get('colaboradores', 0) or 0),
                "activos": int(result.get('activos', 0) or 0)
            }
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_stats_usuarios: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener estadísticas"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_stats_usuarios: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")
