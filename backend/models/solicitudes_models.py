"""
Modelo para Solicitudes de Colaboración
"""

from connection.db import get_connection
from datetime import datetime
from utils.error_handler import error_db


def get_all_solicitudes():
    """Obtener todas las solicitudes"""
    connection = get_connection()
    if not connection:
        return []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.*,
                    u.nombre as revisor_nombre
                FROM solicitudes_colaboracion s
                LEFT JOIN usuarios u ON s.id_revisor = u.id_usuario
                ORDER BY 
                    CASE s.estado
                        WHEN 'pendiente' THEN 1
                        WHEN 'aceptado' THEN 2
                        WHEN 'rechazado' THEN 3
                    END,
                    s.fecha DESC
            """)
            return cursor.fetchall()
    except Exception as e:
        error_db('get_all_solicitudes', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al obtener solicitudes: {e}")
        return []
    finally:
        connection.close()

def get_solicitud_by_id(id_solicitud):
    """Obtener una solicitud por ID"""
    connection = get_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.*,
                    u.nombre as revisor_nombre
                FROM solicitudes_colaboracion s
                LEFT JOIN usuarios u ON s.id_revisor = u.id_usuario
                WHERE s.id_solicitud = %s
            """, (id_solicitud,))
            return cursor.fetchone()
    except Exception as e:
        error_db('get_solicitud_by_id', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al obtener solicitud: {e}")
        return None
    finally:
        connection.close()

def get_solicitudes_pendientes():
    """Obtener solicitudes pendientes"""
    connection = get_connection()
    if not connection:
        return []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM solicitudes_colaboracion
                WHERE estado = 'pendiente'
                ORDER BY fecha DESC
            """)
            return cursor.fetchall()
    except Exception as e:
        error_db('get_solicitudes_pendientes', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al obtener solicitudes pendientes: {e}")
        return []
    finally:
        connection.close()

def count_solicitudes_pendientes():
    """Contar solicitudes pendientes"""
    connection = get_connection()
    if not connection:
        return 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM solicitudes_colaboracion WHERE estado = 'pendiente'")
            result = cursor.fetchone()
            return result['total'] if result else 0
    except Exception as e:
        error_db('count_solicitudes_pendientes', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al contar solicitudes pendientes: {e}")
        return 0
    finally:
        connection.close()

def update_estado_solicitud(id_solicitud, estado, id_revisor, motivo_rechazo=None):
    """Actualizar estado de una solicitud"""
    connection = get_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            # Verificar si la tabla tiene columna motivo_rechazo
            if motivo_rechazo and estado == 'rechazado':
                cursor.execute("""
                    UPDATE solicitudes_colaboracion
                    SET estado = %s, id_revisor = %s, motivo_rechazo = %s
                    WHERE id_solicitud = %s
                """, (estado, id_revisor, motivo_rechazo, id_solicitud))
            else:
                cursor.execute("""
                    UPDATE solicitudes_colaboracion
                    SET estado = %s, id_revisor = %s
                    WHERE id_solicitud = %s
                """, (estado, id_revisor, id_solicitud))
            connection.commit()
            return True
    except Exception as e:
        error_db('update_estado_solicitud', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al actualizar solicitud: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def create_user_from_solicitud(id_solicitud):
    """Crear usuario en la tabla usuarios cuando se acepta una solicitud"""
    connection = get_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            # Obtener datos de la solicitud
            cursor.execute("""
                SELECT nombre, correo
                FROM solicitudes_colaboracion
                WHERE id_solicitud = %s
            """, (id_solicitud,))
            solicitud = cursor.fetchone()
            if not solicitud:
                print(f"Solicitud {id_solicitud} no encontrada")
                return False
            # Verificar si ya existe un usuario con ese correo
            cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s", (solicitud['correo'],))
            existing_user = cursor.fetchone()
            if existing_user:
                print(f"Usuario con correo {solicitud['correo']} ya existe")
                return True  # No es error, simplemente ya existe
            # Obtener el id_rol para 'GESTOR'
            cursor.execute("SELECT id_rol FROM roles WHERE nombre = 'GESTOR'")
            rol_result = cursor.fetchone()
            if not rol_result:
                print("Error: Rol 'GESTOR' no encontrado en la base de datos")
                return False
            id_rol_gestor = rol_result['id_rol']
            # Generar contraseña temporal (hash de correo + 'temp123')
            import hashlib
            temp_password = f"{solicitud['correo']}temp123"
            password_hash = hashlib.sha256(temp_password.encode()).hexdigest()
            # Crear usuario con rol 'GESTOR'
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contrasena, id_rol, fecha_registro, estado)
                VALUES (%s, %s, %s, %s, NOW(), 'ACTIVO')
            """, (solicitud['nombre'], solicitud['correo'], password_hash, id_rol_gestor))
            connection.commit()
            print(f"✅ Usuario creado: {solicitud['nombre']} ({solicitud['correo']}) - Rol: GESTOR (id_rol={id_rol_gestor})")
            return True
    except Exception as e:
        error_db('create_user_from_solicitud', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al crear usuario desde solicitud: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def delete_solicitud(id_solicitud):
    """Eliminar una solicitud"""
    connection = get_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM solicitudes_colaboracion WHERE id_solicitud = %s", (id_solicitud,))
            connection.commit()
            return True
    except Exception as e:
        error_db('delete_solicitud', f'Error: {str(e)}', 'models/solicitudes_models.py')
        print(f"Error al eliminar solicitud: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def calculate_time_ago(fecha):
    """Calcular tiempo transcurrido"""
    if not fecha:
        return "Fecha desconocida"
    now = datetime.now()
    diff = now - fecha
    if diff.days > 365:
        years = diff.days // 365
        return f"Hace {years} año{'s' if years > 1 else ''}"
    elif diff.days > 30:
        months = diff.days // 30
        return f"Hace {months} mes{'es' if months > 1 else ''}"
    elif diff.days > 0:
        return f"Hace {diff.days} día{'s' if diff.days > 1 else ''}"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"Hace {hours} hora{'s' if hours > 1 else ''}"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"Hace {minutes} minuto{'s' if minutes > 1 else ''}"
    else:
        return "Hace un momento"
