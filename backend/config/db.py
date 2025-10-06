# ===== CONFIGURACIÓN DE LA BASE DE DATOS =====
# Función para obtener conexión a la base de datos MySQL
import pymysql
from .conexion import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET

def get_db_connection():
	return pymysql.connect(
		host=DB_HOST,
		user=DB_USER,
		password=DB_PASSWORD,
		db=DB_NAME,
		port=3306,
		charset=DB_CHARSET,
		cursorclass=pymysql.cursors.DictCursor
	)
