"""Servicios de gestión de reportes de errores."""

import pymysql
from fastapi import HTTPException, status
from app.core.database import get_connection
from app.core.logger import logger

def eliminar_reporte(id_reporte: int):
    """Elimina un reporte resuelto."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_reporte FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            if not cursor.fetchone():
                return None
            
            cursor.execute("DELETE FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            conn.commit()
            logger.info(f"Reporte {id_reporte} eliminado")
            return True
            
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de BD eliminando reporte {id_reporte}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar reporte"
        )
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado eliminando reporte {id_reporte}: {e}", exc_info=True)
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

def obtener_reportes(estado: str = None, prioridad: str = None, query: str = None, skip: int = 0, limit: int = 100):
    """Lista paginada de reportes con filtros opcionales."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            sql = """
            SELECT r.*, u.nombre_completo as nombre_usuario 
            FROM reportes_errores r
            LEFT JOIN usuarios u ON r.id_usuario_reporta = u.id_usuario
            WHERE 1=1
            """
            count_sql = "SELECT COUNT(*) as total FROM reportes_errores r LEFT JOIN usuarios u ON r.id_usuario_reporta = u.id_usuario WHERE 1=1"
            params = []
            
            if estado and estado != "todos":
                sql += " AND r.estado = %s"
                count_sql += " AND r.estado = %s"
                params.append(estado)
            
            if prioridad and prioridad != "todas":
                sql += " AND r.prioridad = %s"
                count_sql += " AND r.prioridad = %s"
                params.append(prioridad)
                
            if query:
                search_term = f"%{query}%"
                sql += " AND (r.descripcion_error LIKE %s OR u.nombre_completo LIKE %s)"
                count_sql += " AND (r.descripcion_error LIKE %s OR u.nombre_completo LIKE %s)"
                params.extend([search_term, search_term])
            
            cursor.execute(count_sql, tuple(params))
            total = cursor.fetchone()['total']
            
            sql += " ORDER BY r.fecha_reporte DESC LIMIT %s OFFSET %s"
            data_params = params.copy()
            data_params.extend([limit, skip])
            
            cursor.execute(sql, tuple(data_params))
            data = cursor.fetchall()
            
            return {"total": total, "data": data}
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_reportes: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar reportes"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_reportes: {e}", exc_info=True)
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

def actualizar_gestion_reporte(id_reporte: int, estado: str = None, prioridad: str = None):
    """Actualiza estado y/o prioridad de un reporte."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_reporte FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            if not cursor.fetchone():
                return None
            
            updates = []
            params = []
            if estado:
                updates.append("estado = %s")
                params.append(estado)
            if prioridad:
                updates.append("prioridad = %s")
                params.append(prioridad)
            
            if not updates:
                return True
                
            sql = f"UPDATE reportes_errores SET {', '.join(updates)} WHERE id_reporte = %s"
            params.append(id_reporte)
            
            cursor.execute(sql, tuple(params))
            conn.commit()
            logger.info(f"Reporte {id_reporte} actualizado")
            return True
            
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de BD actualizando reporte {id_reporte}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar reporte"
        )
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado actualizando reporte {id_reporte}: {e}", exc_info=True)
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

def obtener_stats_reportes():
    """Obtiene estadísticas agregadas de reportes."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END) as pendientes,
                SUM(CASE WHEN estado = 'en_revision' THEN 1 ELSE 0 END) as en_revision,
                SUM(CASE WHEN prioridad = 'alta' THEN 1 ELSE 0 END) as alta_prioridad
            FROM reportes_errores
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            
            return {
                "total": result.get('total', 0) or 0,
                "pendientes": int(result.get('pendientes', 0) or 0),
                "en_revision": int(result.get('en_revision', 0) or 0),
                "alta_prioridad": int(result.get('alta_prioridad', 0) or 0)
            }
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_stats_reportes: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener estadísticas de reportes"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_stats_reportes: {e}", exc_info=True)
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
