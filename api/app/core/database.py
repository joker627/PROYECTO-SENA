"""Gestión del pool de conexiones a MySQL.

Utiliza DBUtils para mantener un pool de conexiones reutilizables,
mejorando el rendimiento y la capacidad de manejar peticiones concurrentes.
"""

import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from app.core.config import settings
from app.core.logger import logger

connection_pool = None

def init_pool():
    """Inicializa el pool de conexiones a MySQL.
    
    Crea un pool con conexiones prestablecidas que serán reutilizadas.
    """
    global connection_pool
    
    if connection_pool is None:
        max_conn = settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW
        connection_pool = PooledDB(
            creator=pymysql,
            maxconnections=max_conn,
            mincached=10,                # Más conexiones en cache para picos de tráfico
            maxcached=max_conn,          # Cachear todas las conexiones creadas
            maxshared=0,                 # No compartir conexiones entre threads (más seguro)
            blocking=True,
            maxusage=1000,               # Reciclar conexión después de 1000 usos
            setsession=[],
            ping=1 if settings.DB_POOL_PRE_PING else 0,
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            cursorclass=DictCursor,
            autocommit=False,            # Usar transacciones manuales para control ACID
            charset='utf8mb4'
        )
        logger.info(f"Pool de conexiones inicializado: max={max_conn}, cached={10}")
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
        logger.error(f"Error conectando a MySQL: {e}", exc_info=True)
        raise

def close_pool():
    """Cierra el pool de conexiones.
    
    Libera todos los recursos del pool.
    """
    global connection_pool
    
    if connection_pool is not None:
        try:
            connection_pool.close()
            connection_pool = None
            logger.info("Pool de conexiones cerrado correctamente")
        except Exception as e:
            logger.error(f"Error cerrando pool de conexiones: {e}", exc_info=True)
