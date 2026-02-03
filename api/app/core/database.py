"""Gestión del pool de conexiones MySQL con DBUtils."""

import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from app.core.config import settings
from app.core.logger import logger

connection_pool = None

def init_pool():
    """Inicializa el pool de conexiones MySQL."""
    global connection_pool
    
    if connection_pool is None:
        max_conn = settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW
        connection_pool = PooledDB(
            creator=pymysql,
            maxconnections=max_conn,
            mincached=10,
            maxcached=max_conn,
            maxshared=0,
            blocking=True,
            maxusage=1000,
            setsession=[],
            ping=1 if settings.DB_POOL_PRE_PING else 0,
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT,
            cursorclass=DictCursor,
            autocommit=False,
            charset='utf8mb4'
        )
        logger.info(f"Pool inicializado: max={max_conn}, cached=10")
    return connection_pool

def get_connection():
    """Obtiene una conexión del pool. Debe cerrarse con conn.close()."""
    try:
        if connection_pool is None:
            init_pool()
        return connection_pool.connection()
    except pymysql.MySQLError as e:
        logger.error(f"Error conectando a MySQL: {e}", exc_info=True)
        raise

def close_pool():
    """Cierra el pool y libera recursos."""
    global connection_pool
    
    if connection_pool is not None:
        try:
            connection_pool.close()
            connection_pool = None
            logger.info("Pool cerrado correctamente")
        except Exception as e:
            logger.error(f"Error cerrando pool: {e}", exc_info=True)
