"""Model: rendimiento_modelo"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_latest_rendimiento():
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM rendimiento_modelo ORDER BY ultima_actualizacion DESC LIMIT 1")
            return cursor.fetchone()
    finally:
        conn.close()


def create_rendimiento(precision_actual, observaciones=None):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO rendimiento_modelo (precision_actual, observaciones) VALUES (%s, %s)", (precision_actual, observaciones))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_rendimiento(id_rendimiento, precision_actual=None, observaciones=None):
    conn = get_connection()
    if not conn:
        return False
    try:
        fields = []
        params = []
        if precision_actual is not None:
            fields.append('precision_actual = %s')
            params.append(precision_actual)
        if observaciones is not None:
            fields.append('observaciones = %s')
            params.append(observaciones)
        if not fields:
            return False
        params.append(id_rendimiento)
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE rendimiento_modelo SET {', '.join(fields)} WHERE id_rendimiento = %s", tuple(params))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_rendimiento(id_rendimiento):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM rendimiento_modelo WHERE id_rendimiento = %s", (id_rendimiento,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
