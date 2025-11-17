# api/config/db.py
import pymysql
from pymysql import Error
from api.config.conexion import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def get_db_api_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

def test_connection():
    try:
        conn = get_db_api_connection()
        conn.close()
        print("Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print("Error conectando a la DB:", e)
        return False