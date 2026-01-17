import pymysql
from pymysql.cursors import DictCursor
from app.core.config import settings

def get_connection():
    try:
        return pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            cursorclass=DictCursor,
            autocommit=True
        )
    except pymysql.MySQLError as e:
        print("Error conectando a MySQL:", e)
        raise
