"""Model: estadisticas (global admin statistics)"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_latest_estadisticas():
    """Return the most recent row from `estadisticas` as a dict.

    If no row exists or DB is unavailable, return None.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM estadisticas ORDER BY fecha_actualizacion DESC LIMIT 1")
            return cursor.fetchone()
    finally:
        conn.close()
