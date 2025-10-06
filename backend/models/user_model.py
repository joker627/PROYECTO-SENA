from config.db import get_db_connection
from utils.utils import hash_password, verify_password


# Buscar usuario por email
def get_user_by_email(correo):
    with get_db_connection() as conn:
        with conn.cursor() as cursor: 
            cursor.execute('SELECT * FROM usuario WHERE correo=%s', (correo,))
            return cursor.fetchone()

# Obtener todos los roles del sistema
def get_all_roles():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM rol')
            return cursor.fetchall()


# Validar login y actualizar último acceso
def validate_user(correo, contrasena):
    try:
        user = get_user_by_email(correo)
        
        if not user:
            return None
        
        pwd_ok = verify_password(contrasena, user['contrasena'])
        
        if pwd_ok:
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


# Crear nuevo usuario en la BD
def register_user(nombre, correo, contrasena, id_rol):
    try:
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


# Cambiar contraseña del usuario
def change_user_password(id_usuario, nueva_contrasena):
    try:
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


# Verificar contraseña actual del usuario
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


# Buscar usuario por ID
def get_user_by_id(id_usuario):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id_usuario,))
                return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
        return None


# Cambiar nombre del usuario
def update_user_username(id_usuario, new_username):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE usuario SET nombre = %s WHERE id_usuario = %s',
                    (new_username, id_usuario)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar username: {e}")
        return False


# Cambiar email del usuario
def update_user_email(id_usuario, new_email):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE usuario SET correo = %s WHERE id_usuario = %s',
                    (new_email, id_usuario)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar email: {e}")
        return False


# Eliminar usuario de la BD
def delete_user_account(id_usuario):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM usuario WHERE id_usuario = %s', (id_usuario,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
