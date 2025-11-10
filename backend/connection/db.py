import pymysql

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'manueldev.55'
DB_PORT = 3306
DB_NAME = 'sign_technology'

def get_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        # Registrar error en alertas_sistema
        try:
            from utils.error_handler import error_db
            error_db('get_connection', f'Error al conectar: {str(e)}', 'connection/db.py')
        except:
            pass  # Si falla el registro, no detener el flujo
        raise  # Re-lanzar el error original
