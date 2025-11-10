from connection.db import get_connection
from utils.error_handler import error_db


def obtener_todas_las_notificaciones():
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id_alerta, modulo, tipo_error, severidad, descripcion, estado, fecha, id_responsable "
                "FROM alertas_sistema ORDER BY fecha DESC"
            )
            return cursor.fetchall()
    except Exception as e:
        error_db('obtener_todas_las_notificaciones', str(e), 'models/notification_models.py')
        return []
    finally:
        if conexion:
            conexion.close()


def obtener_notificaciones_pendientes():
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id_alerta, modulo, tipo_error, severidad, descripcion, estado, fecha "
                "FROM alertas_sistema WHERE estado != 'resuelto' ORDER BY fecha DESC"
            )
            return cursor.fetchall()
    except Exception as e:
        error_db('obtener_notificaciones_pendientes', str(e), 'models/notification_models.py')
        return []
    finally:
        if conexion:
            conexion.close()


def contar_notificaciones_pendientes():
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM alertas_sistema WHERE estado != 'resuelto'")
            resultado = cursor.fetchone()
            return resultado['count'] if resultado else 0
    except Exception as e:
        error_db('contar_notificaciones_pendientes', str(e), 'models/notification_models.py')
        return 0
    finally:
        if conexion:
            conexion.close()


def cambiar_estado_notificacion(id_notificacion, nuevo_estado):
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE alertas_sistema SET estado = %s WHERE id_alerta = %s", (nuevo_estado, id_notificacion))
            conexion.commit()
            return cursor.rowcount > 0
    except Exception as e:
        error_db('cambiar_estado_notificacion', str(e), 'models/notification_models.py')
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()


def eliminar_notificacion(id_notificacion):
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM alertas_sistema WHERE id_alerta = %s", (id_notificacion,))
            conexion.commit()
            return cursor.rowcount > 0
    except Exception as e:
        error_db('eliminar_notificacion', str(e), 'models/notification_models.py')
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()


def marcar_todas_como_resueltas():
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE alertas_sistema SET estado = 'resuelto' WHERE estado != 'resuelto'")
            conexion.commit()
            return True
    except Exception as e:
        error_db('marcar_todas_como_resueltas', str(e), 'models/notification_models.py')
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()


def eliminar_todas_las_notificaciones():
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM alertas_sistema")
            conexion.commit()
            return True
    except Exception as e:
        error_db('eliminar_todas_las_notificaciones', str(e), 'models/notification_models.py')
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()


def eliminar_notificaciones_resueltas():
    conexion = None
    try:
        conexion = get_connection()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM alertas_sistema WHERE estado = 'resuelto'")
            conexion.commit()
            return True
    except Exception as e:
        error_db('eliminar_notificaciones_resueltas', str(e), 'models/notification_models.py')
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()
