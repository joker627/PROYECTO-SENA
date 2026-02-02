from app.core.database import get_connection

def eliminar_reporte(id_reporte: int):
    """Elimina un reporte de la base de datos (cuando se resuelve)"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Verificar que existe
            cursor.execute("SELECT id_reporte FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            if not cursor.fetchone():
                return None  # No encontrado
            
            # Eliminar
            cursor.execute("DELETE FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error eliminando reporte {id_reporte}: {e}")
        return False
    finally:
        conn.close()

def obtener_reportes(estado: str = None, prioridad: str = None, query: str = None, skip: int = 0, limit: int = 100):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Base Queries
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
            
            # Count
            cursor.execute(count_sql, tuple(params))
            total = cursor.fetchone()['total']
            
            # Data
            sql += " ORDER BY r.fecha_reporte DESC LIMIT %s OFFSET %s"
            data_params = params.copy()
            data_params.extend([limit, skip])
            
            cursor.execute(sql, tuple(data_params))
            data = cursor.fetchall()
            
            return {"total": total, "data": data}
    finally:
        conn.close()

def actualizar_gestion_reporte(id_reporte: int, estado: str = None, prioridad: str = None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Verificar que el reporte existe
            cursor.execute("SELECT id_reporte FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            if not cursor.fetchone():
                return None  # Reporte no encontrado
            
            updates = []
            params = []
            if estado:
                updates.append("estado = %s")
                params.append(estado)
            if prioridad:
                updates.append("prioridad = %s")
                params.append(prioridad)
            
            if not updates:
                return True  # Sin cambios pero válido
                
            sql = f"UPDATE reportes_errores SET {', '.join(updates)} WHERE id_reporte = %s"
            params.append(id_reporte)
            
            cursor.execute(sql, tuple(params))
            conn.commit()
            return True  # Éxito
    except Exception as e:
        print(f"Error actualizando reporte {id_reporte}: {e}")
        return False  # Error de DB
    finally:
        conn.close()

def obtener_stats_reportes():
    conn = get_connection()
    try:
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
    finally:
        conn.close()
