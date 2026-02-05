from app.core.database import get_connection
from app.core.logger import logger

def obtener_contribuciones(estado: str = None, query: str = None, skip: int = 0, limit: int = 100):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Base Query
            sql = """
            SELECT c.*, u.nombre_completo as nombre_usuario 
            FROM contribuciones_senas c
            LEFT JOIN usuarios u ON c.id_usuario_envio = u.id_usuario
            WHERE 1=1
            """
            count_sql = "SELECT COUNT(*) as total FROM contribuciones_senas c LEFT JOIN usuarios u ON c.id_usuario_envio = u.id_usuario WHERE 1=1"
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
                
            # Count
            cursor.execute(count_sql, tuple(params))
            total = cursor.fetchone()['total']
            
            # Data
            sql += " ORDER BY c.fecha_contribucion DESC LIMIT %s OFFSET %s"
            data_params = params.copy()
            data_params.extend([limit, skip])
            
            cursor.execute(sql, tuple(data_params))
            data = cursor.fetchall()
            logger.info(f"Contribuciones obtenidas: {len(data)} resultados, filtros aplicados")
            return {"total": total, "data": data}
    except Exception as e:
        logger.error(f"Error obteniendo contribuciones: {e}")
        raise
    finally:
        conn.close()

def actualizar_estado_contribucion(id_contribucion: int, estado: str, observaciones: str = None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE contribuciones_senas SET estado=%s, observaciones_gestion=%s, fecha_gestion=NOW() WHERE id_contribucion=%s"
            cursor.execute(sql, (estado, observaciones, id_contribucion))
            conn.commit()
            updated = cursor.rowcount > 0
            if updated:
                logger.info(f"Estado de contribución actualizado: ID {id_contribucion} -> {estado}")
            else:
                logger.warning(f"No se encontró contribución para actualizar: ID {id_contribucion}")
            return updated
    except Exception as e:
        logger.error(f"Error actualizando estado de contribución {id_contribucion}: {e}")
        raise
    finally:
        conn.close()

def obtener_stats_contribuciones():
    conn = get_connection()
    try:
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
    finally:
        conn.close()
