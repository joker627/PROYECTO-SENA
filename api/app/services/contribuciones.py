"""Servicios de gestión de contribuciones de señas."""

import pymysql
from fastapi import HTTPException, status
from app.core.database import get_connection
from app.core.logger import logger

def obtener_contribuciones(estado: str = None, query: str = None, skip: int = 0, limit: int = 100):
    """Lista paginada de contribuciones con filtros."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            sql = """
            SELECT c.*, u.nombre_completo as nombre_usuario 
            FROM contribuciones_senas c
            LEFT JOIN usuarios u ON c.id_usuario_envio = u.id_usuario
            WHERE 1=1
            """
            count_sql = """
            SELECT COUNT(*) as total 
            FROM contribuciones_senas c 
            LEFT JOIN usuarios u ON c.id_usuario_envio = u.id_usuario 
            WHERE 1=1
            """
            params = []
            
            if estado and estado != 'todos':
                sql += " AND c.estado = %s"
                count_sql += " AND c.estado = %s"
                params.append(estado)
                
            if query:
                search_term = f"%{query}%"
                sql += " AND (c.palabra_asociada LIKE %s OR c.descripcion LIKE %s OR u.nombre_completo LIKE %s)"
                count_sql += " AND (c.palabra_asociada LIKE %s OR c.descripcion LIKE %s OR u.nombre_completo LIKE %s)"
                params.extend([search_term, search_term, search_term])
                
            cursor.execute(count_sql, tuple(params))
            total = cursor.fetchone()['total']
            
            sql += " ORDER BY c.fecha_contribucion DESC LIMIT %s OFFSET %s"
            data_params = params.copy()
            data_params.extend([limit, skip])
            
            cursor.execute(sql, tuple(data_params))
            data = cursor.fetchall()
            
            return {"total": total, "data": data}
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_contribuciones: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar contribuciones"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_contribuciones: {e}", exc_info=True)
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


def actualizar_estado_contribucion(id_contribucion: int, estado: str, observaciones: str = None):
    """Actualiza estado de una contribución."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            sql = """
            UPDATE contribuciones_senas 
            SET estado=%s, observaciones_gestion=%s, fecha_gestion=NOW() 
            WHERE id_contribucion=%s
            """
            cursor.execute(sql, (estado, observaciones, id_contribucion))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Contribución {id_contribucion} actualizada a estado: {estado}")
                return True
            return False
            
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de BD en actualizar_estado_contribucion: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar contribución"
        )
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error inesperado en actualizar_estado_contribucion: {e}", exc_info=True)
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


def obtener_stats_contribuciones():
    """Obtiene estadísticas agregadas de contribuciones."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END) as pendientes,
                SUM(CASE WHEN estado = 'aprobada' THEN 1 ELSE 0 END) as aprobadas
            FROM contribuciones_senas
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            
            return {
                "total": result.get('total', 0) or 0,
                "pendientes": int(result.get('pendientes', 0) or 0),
                "aprobadas": int(result.get('aprobadas', 0) or 0)
            }
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_stats_contribuciones: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener estadísticas"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_stats_contribuciones: {e}", exc_info=True)
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
