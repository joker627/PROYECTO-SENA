import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from app.core.config import settings

# Pool de conexiones
db_pool = PooledDB(
    creator=pymysql,
    maxconnections=20,  # Máximo número de conexiones en el pool
    mincached=5,        # Mínimo de conexiones inactivas en el pool
    maxcached=10,       # Máximo de conexiones inactivas en el pool
    maxshared=15,       # Máximo de conexiones compartidas
    blocking=True,      # Bloquear si no hay conexiones disponibles
    maxusage=None,      # Número de reutilizaciones de una conexión (None = ilimitado)
    setsession=[],      # Comandos SQL para ejecutar en cada nueva conexión
    ping=1,             # Verificar conexión antes de usar (0=nunca, 1=default, 2=optimista, 4=pesimista, 7=siempre)
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    port=settings.DB_PORT,
    cursorclass=DictCursor,
    autocommit=True
)

def get_connection():
    """Obtiene una conexión del pool"""
    try:
        return db_pool.connection()
    except pymysql.MySQLError as e:
        print("Error conectando a MySQL:", e)
        raise
