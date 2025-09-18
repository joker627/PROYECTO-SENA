from config.db import get_db_connection

# Funciones para interactuar con la tabla de usuarios
def get_user_by_email(correo):
    with get_db_connection() as conn:
        with conn.cursor() as cursor: 
            cursor.execute('SELECT * FROM usuarios WHERE correo=%s', (correo,))
            return cursor.fetchone()


# Validar usuario por correo y contraseña
def validate_user(correo, contrasena):
    user = get_user_by_email(correo)
    if user and user['contrasena'] == contrasena:
        return user
    return None

# Registrar nuevo usuario
def register_user(nombre, correo, contrasena):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)', (nombre, correo, contrasena))
                conn.commit()
                return True
            except Exception as e:
                print(f"Eror al registrar el usuario: {e}")
                return False
