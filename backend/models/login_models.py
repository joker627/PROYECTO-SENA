from connection.db import get_connection
from utils.error_handler import error_db

def verificar_usuario(correo, contrasena):
    """
    Retorna un diccionario con el usuario si existe:
    {id_usuario, nombre, correo, id_rol}
    """
    conexion = get_connection()
    usuario = None
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id_usuario, nombre, correo, id_rol FROM usuarios WHERE correo=%s AND contrasena=%s"
            cursor.execute(sql, (correo, contrasena))
            usuario = cursor.fetchone()
    except Exception as e:
        print("Error DB:", e)
        try:
            error_db('verificar_usuario', f'Error consulta login: {str(e)}', 'models/login_models.py')
        except Exception:
            pass
    finally:
        conexion.close()
    return usuario
