"""
# ===== CONFIGURACIÓN DE LA BASE DE DATOS LOCAL =====
# Función para obtener conexión a la base de datos MySQL


import pymysql
from .conexion import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET, DB_PORT

def get_db_connection():
	return pymysql.connect(
		host=DB_HOST,
		user=DB_USER,
		password=DB_PASSWORD,
		db=DB_NAME,
		port=DB_PORT,
		charset=DB_CHARSET,
		cursorclass=pymysql.cursors.DictCursor
	)

"""
# ===== CONFIGURACIÓN DE LA BASE DE DATOS =====
# Función para obtener conexión a la base de datos MySQL/MariaDB 
import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        port=int(os.environ['DB_PORT']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
