from backend.config.db import get_db_connection


# Funciones para interactuar con la tabla de usuarios
def get_user_by_email(correo):
    with get_db_connection() as conn:
        with conn.cursor() as cursor: 
            cursor.execute('SELECT * FROM usuario WHERE correo=%s', (correo,))
            return cursor.fetchone()

# funcion para obtener todos los roles
def get_all_roles():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM rol')
            return cursor.fetchall()


# Validar usuario por correo y contraseña
def validate_user(correo, contrasena):
    user = get_user_by_email(correo)
    if user and user['contrasena'] == contrasena:
        # Actualizar último acceso en la base de datos
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE usuario SET ultimo_acceso = NOW() WHERE id_usuario = %s',
                    (user['id_usuario'],))
                conn.commit()
        return user
    return None


# Registrar nuevo usuario
def register_user(nombre, correo, contrasena, id_rol):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO usuario (nombre, correo, contrasena, id_rol) VALUES (%s, %s, %s,%s)', (nombre, correo, contrasena,id_rol))
                conn.commit()
                return True
            except Exception as e:
                print(f"Eror al registrar el usuario: {e}")
                return False
