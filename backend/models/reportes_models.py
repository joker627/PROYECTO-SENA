"""Model functions for reportes (converted from ReportesModels class)."""

from connection.db import get_connection
from datetime import datetime
from utils.error_handler import error_db


def get_all_reportes():
    """Obtiene todos los reportes de error"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    r.id_reporte,
                    r.nombre_reportante,
                    r.correo_contacto,
                    r.tipo_error,
                    r.descripcion,
                    r.evidencia_url,
                    r.id_traduccion,
                    r.origen,
                    r.fecha,
                    r.estado,
                    r.fecha_resolucion,
                    r.id_responsable,
                    NULL as uuid_transaccion,
                    u.nombre as nombre_responsable
                FROM reportes_error r
                LEFT JOIN usuarios u ON r.id_responsable = u.id_usuario
                ORDER BY 
                    CASE r.estado
                        WHEN 'pendiente' THEN 1
                        WHEN 'en revision' THEN 2
                        WHEN 'resuelto' THEN 3
                    END,
                    r.fecha DESC
            """
            cursor.execute(query)
            reportes = cursor.fetchall()
            # Calcular tiempo transcurrido
            for reporte in reportes:
                reporte['tiempo_transcurrido'] = calculate_time_ago(reporte['fecha'])
            return reportes
    except Exception as e:
        print(f"Error al obtener reportes: {e}")
        error_db('get_all_reportes', f'Error en consulta: {str(e)}', 'models/reportes_models.py')
        return []
    finally:
        if connection:
            connection.close()


def get_reporte_by_id(id_reporte):
    """Obtiene un reporte específico por ID"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    r.id_reporte,
                    r.nombre_reportante,
                    r.correo_contacto,
                    r.tipo_error,
                    r.descripcion,
                    r.evidencia_url,
                    r.id_traduccion,
                    r.origen,
                    r.fecha,
                    r.estado,
                    r.fecha_resolucion,
                    r.id_responsable,
                    NULL as uuid_transaccion,
                    u.nombre as nombre_responsable
                FROM reportes_error r
                LEFT JOIN usuarios u ON r.id_responsable = u.id_usuario
                WHERE r.id_reporte = %s
            """
            cursor.execute(query, (id_reporte,))
            reporte = cursor.fetchone()
            if reporte:
                reporte['tiempo_transcurrido'] = calculate_time_ago(reporte['fecha'])
            return reporte
    except Exception as e:
        print(f"Error al obtener reporte: {e}")
        error_db('get_reporte_by_id', f'Error en consulta: {str(e)}', 'models/reportes_models.py')
        return None
    finally:
        if connection:
            connection.close()


def get_reportes_by_estado(estado):
    """Obtiene reportes filtrados por estado"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    r.id_reporte,
                    r.nombre_reportante,
                    r.correo_contacto,
                    r.tipo_error,
                    r.descripcion,
                    r.evidencia_url,
                    r.id_traduccion,
                    r.origen,
                    r.fecha,
                    r.estado,
                    r.fecha_resolucion,
                    r.id_responsable,
                    NULL as uuid_transaccion,
                    u.nombre as nombre_responsable
                FROM reportes_error r
                LEFT JOIN usuarios u ON r.id_responsable = u.id_usuario
                WHERE r.estado = %s
                ORDER BY r.fecha DESC
            """
            cursor.execute(query, (estado,))
            reportes = cursor.fetchall()
            for reporte in reportes:
                reporte['tiempo_transcurrido'] = calculate_time_ago(reporte['fecha'])
            return reportes
    except Exception as e:
        print(f"Error al obtener reportes por estado: {e}")
        error_db('get_reportes_by_estado', f'Error en consulta: {str(e)}', 'models/reportes_models.py')
        return []
    finally:
        if connection:
            connection.close()


def count_reportes_pendientes():
    """Cuenta los reportes pendientes"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) as total FROM reportes_error WHERE estado = 'pendiente'"
            cursor.execute(query)
            result = cursor.fetchone()
            return result['total'] if result else 0
    except Exception as e:
        print(f"Error al contar reportes pendientes: {e}")
        error_db('count_reportes_pendientes', f'Error en consulta: {str(e)}', 'models/reportes_models.py')
        return 0
    finally:
        if connection:
            connection.close()


def count_reportes(estado=None):
    """Cuenta reportes, opcionalmente filtrados por estado"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            if estado:
                query = "SELECT COUNT(*) as total FROM reportes_error WHERE estado = %s"
                cursor.execute(query, (estado,))
            else:
                query = "SELECT COUNT(*) as total FROM reportes_error"
                cursor.execute(query)
            result = cursor.fetchone()
            return result['total'] if result else 0
    except Exception as e:
        print(f"Error al contar reportes (general): {e}")
        error_db('count_reportes', f'Error en consulta: {str(e)}', 'models/reportes_models.py')
        return 0
    finally:
        if connection:
            connection.close()


def get_reportes_paginated(page=1, per_page=10, estado=None):
    """Obtiene reportes paginados desde la base de datos. Si `estado` es suministrado,
    aplica filtro por estado. Ordena por fecha descendente.
    """
    connection = None
    try:
        # Normalizar y validar parámetros
        try:
            page_i = int(page)
            if page_i < 1:
                page_i = 1
        except Exception:
            page_i = 1

        try:
            per_page_i = int(per_page)
            if per_page_i < 1:
                per_page_i = 10
        except Exception:
            per_page_i = 10

        offset = max(0, (page_i - 1)) * per_page_i
        connection = get_connection()
        with connection.cursor() as cursor:
            if estado:
                query = """
                    SELECT 
                        r.id_reporte,
                        r.nombre_reportante,
                        r.correo_contacto,
                        r.tipo_error,
                        r.descripcion,
                        r.evidencia_url,
                        r.id_traduccion,
                        r.origen,
                        r.fecha,
                        r.estado,
                        r.fecha_resolucion,
                        r.id_responsable,
                        NULL as uuid_transaccion,
                        u.nombre as nombre_responsable
                    FROM reportes_error r
                    LEFT JOIN usuarios u ON r.id_responsable = u.id_usuario
                    WHERE r.estado = %s
                    ORDER BY r.fecha DESC
                    LIMIT %s OFFSET %s
                """
                params = (estado, per_page_i, offset)
                cursor.execute(query, params)
            else:
                query = """
                    SELECT 
                        r.id_reporte,
                        r.nombre_reportante,
                        r.correo_contacto,
                        r.tipo_error,
                        r.descripcion,
                        r.evidencia_url,
                        r.id_traduccion,
                        r.origen,
                        r.fecha,
                        r.estado,
                        r.fecha_resolucion,
                        r.id_responsable,
                        NULL as uuid_transaccion,
                        u.nombre as nombre_responsable
                    FROM reportes_error r
                    LEFT JOIN usuarios u ON r.id_responsable = u.id_usuario
                    ORDER BY r.fecha DESC
                    LIMIT %s OFFSET %s
                """
                params = (per_page_i, offset)
                cursor.execute(query, params)

            reportes = cursor.fetchall()
            for reporte in reportes:
                reporte['tiempo_transcurrido'] = calculate_time_ago(reporte['fecha'])
            return reportes
    except Exception as e:
        # Loguear el query/params no sensibles para facilitar debugging
        try:
            detalle = f'Error en consulta: {str(e)}'
            if 'params' in locals():
                detalle += f' | params={params}'
        except Exception:
            detalle = str(e)
        print(f"Error al obtener reportes paginados: {detalle}")
        error_db('get_reportes_paginated', detalle, 'models/reportes_models.py')
        return []
    finally:
        if connection:
            connection.close()


def update_estado_reporte(id_reporte, nuevo_estado):
    """Actualiza el estado de un reporte"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Si el estado es 'resuelto', actualizar fecha_resolucion
            if nuevo_estado == 'resuelto':
                query = """
                    UPDATE reportes_error 
                    SET estado = %s, fecha_resolucion = NOW()
                    WHERE id_reporte = %s
                """
            else:
                query = """
                    UPDATE reportes_error 
                    SET estado = %s
                    WHERE id_reporte = %s
                """
            cursor.execute(query, (nuevo_estado, id_reporte))
            connection.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar estado del reporte: {e}")
        if connection:
            connection.rollback()
        error_db('update_estado_reporte', f'Error al actualizar estado: {str(e)}', 'models/reportes_models.py')
        return False
    finally:
        if connection:
            connection.close()


def delete_reporte(id_reporte):
    """Elimina un reporte"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = "DELETE FROM reportes_error WHERE id_reporte = %s"
            cursor.execute(query, (id_reporte,))
            connection.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar reporte: {e}")
        if connection:
            connection.rollback()
        error_db('delete_reporte', f'Error al eliminar reporte: {str(e)}', 'models/reportes_models.py')
        return False
    finally:
        if connection:
            connection.close()


def delete_all_resolved():
    """Elimina todos los reportes resueltos"""
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Primero contar cuántos se eliminarán
            cursor.execute("SELECT COUNT(*) as total FROM reportes_error WHERE estado = 'resuelto'")
            result = cursor.fetchone()
            count = result['total'] if result else 0
            # Eliminar todos los resueltos
            query = "DELETE FROM reportes_error WHERE estado = 'resuelto'"
            cursor.execute(query)
            connection.commit()
            return count
    except Exception as e:
        print(f"Error al eliminar reportes resueltos: {e}")
        if connection:
            connection.rollback()
        error_db('delete_all_resolved', f'Error: {str(e)}', 'models/reportes_models.py')
        return 0
    finally:
        if connection:
            connection.close()


def calculate_time_ago(fecha):
    """Calcula el tiempo transcurrido desde una fecha"""
    if not fecha:
        return "Fecha no disponible"
    now = datetime.now()
    diff = now - fecha
    if diff.days > 365:
        years = diff.days // 365
        return f"hace {years} año{'s' if years > 1 else ''}"
    elif diff.days > 30:
        months = diff.days // 30
        return f"hace {months} mes{'es' if months > 1 else ''}"
    elif diff.days > 0:
        return f"hace {diff.days} día{'s' if diff.days > 1 else ''}"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"hace {hours} hora{'s' if hours > 1 else ''}"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
    else:
        return "hace un momento"
