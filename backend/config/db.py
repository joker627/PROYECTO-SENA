# ===== CONFIGURACIÓN DE LA BASE DE DATOS =====
# Función para obtener conexión a la base de datos MySQL
import pymysql
from .conexion import MYSQLHOST, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE, MYSQLPORT, MYSQLCHARSET

def get_db_connection():
	return pymysql.connect(
		host=MYSQLHOST,
		user=MYSQLUSER,
		password=MYSQLPASSWORD,
		db=MYSQLDATABASE,
		port=MYSQLPORT,
		charset=MYSQLCHARSET,
		cursorclass=pymysql.cursors.DictCursor
	)
