# ===== CONFIGURACIÓN DE LA BASE DE DATOS =====
# Función para obtener conexión a la base de datos MySQL
# ===== CONFIGURACIÓN DE LA BASE DE DATOS =====
import pymysql
import os

def get_db_connection():
    # Obtener valores DIRECTAMENTE de Railway
    return pymysql.connect(
        host=os.environ['MYSQLHOST'],
        user=os.environ['MYSQLUSER'],
        password=os.environ['MYSQLPASSWORD'],
        db=os.environ['MYSQLDATABASE'],
        port=int(os.environ['MYSQLPORT']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
