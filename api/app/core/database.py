"""Gestión del pool de conexiones a MySQL.

Utiliza DBUtils para mantener un pool de conexiones reutilizables,
mejorando el rendimiento y la capacidad de manejar peticiones concurrentes.
"""

import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from app.core.config import settings

connection_pool = None

def init_pool():
    """Inicializa el pool de conexiones a MySQL.
    
    Crea un pool con conexiones prestablecidas que serán reutilizadas.
    """
    global connection_pool
    
    if connection_pool is None:
        connection_pool = PooledDB(
            creator=pymysql,
            maxconnections=settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW,
            mincached=5,
            maxcached=settings.DB_POOL_SIZE,
            maxshared=settings.DB_POOL_SIZE,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=1 if settings.DB_POOL_PRE_PING else 0,
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            cursorclass=DictCursor,
            autocommit=True,
            charset='utf8mb4'
        )
    return connection_pool

def get_connection():
    """Obtiene una conexión del pool.
    
    Returns:
        Connection: Objeto de conexión a MySQL.
        
    Nota:
        Debe cerrarse con conn.close() después de usarla.
    """
    try:
        if connection_pool is None:
            init_pool()
        return connection_pool.connection()
    except pymysql.MySQLError as e:
        print(f"Error conectando a MySQL: {e}")
        raise

def close_pool():
    """Cierra el pool de conexiones.
    
    Libera todos los recursos del pool.
    """
    global connection_pool
    
    if connection_pool is not None:
        connection_pool.close()
        connection_pool = None
