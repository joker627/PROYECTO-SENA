import pymysql

from connection.config import DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME


def get_connection():
    """Obtener conexión directa a la base de datos"""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
