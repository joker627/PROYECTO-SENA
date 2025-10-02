from config.db import get_db_connection
from utils.utils import hash_password, verify_password


# Funciones para interactuar con la tabla de usuarios
def get_user_by_email(correo):
    with get_db_connection() as conn:
        with conn.cursor() as cursor: 
            cursor.execute('SELECT * FROM usuario WHERE correo=%s', (correo,))
            return cursor.fetchone()

# Función para obtener todos los roles
def get_all_roles():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM rol')
            return cursor.fetchall()


# Validar usuario por email y contraseña
def validate_user(correo, contrasena):
    try:
        # Buscar usuario por email
        user = get_user_by_email(correo)
        
        if not user:
            return None
        
        # Verificar contraseña
        pwd_ok = verify_password(contrasena, user['contrasena'])
        
        if pwd_ok:
            # Actualizar último acceso en la base de datos
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'UPDATE usuario SET ultimo_acceso = NOW() WHERE id_usuario = %s',
                        (user['id_usuario'],))
                    conn.commit()
            return user
        else:
            return None
            
    except Exception as e:
        print(f"Error en validate_user: {e}")
        return None


# Registrar nuevo usuario
def register_user(nombre, correo, contrasena, id_rol):
    try:
        # Convertir contraseña a formato seguro antes de guardar
        safe_pwd = hash_password(contrasena)
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO usuario (nombre, correo, contrasena, id_rol) VALUES (%s, %s, %s, %s)', 
                    (nombre, correo, safe_pwd, id_rol)
                )
                conn.commit()
                
        return True
        
    except Exception as e:
        print(f"Error registrando usuario: {e}")
        return False


# Cambiar contraseña de usuario
def change_user_password(id_usuario, nueva_contrasena):
    try:
        # Convertir nueva contraseña a formato seguro
        safe_new_pwd = hash_password(nueva_contrasena)
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE usuario SET contrasena = %s WHERE id_usuario = %s',
                    (safe_new_pwd, id_usuario)
                )
                conn.commit()
                
                return cursor.rowcount > 0
                    
    except Exception as e:
        print(f"Error cambiando contraseña: {e}")
        return False


# Verificar contraseña actual antes de cambiarla
def verify_current_password(id_usuario, contrasena_actual):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT contrasena FROM usuario WHERE id_usuario = %s', (id_usuario,))
                user = cursor.fetchone()
                
                if user:
                    return verify_password(contrasena_actual, user['contrasena'])
                else:
                    return False
                    
    except Exception as e:
        print(f"Error: {e}")
        return False
