"""Model: repositorio_senas"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_all_senas(limit=100, offset=0):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM repositorio_senas ORDER BY fecha_registro DESC LIMIT %s OFFSET %s", (limit, offset))
            return cursor.fetchall()
    finally:
        conn.close()


def get_sena_by_id(id_sena):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM repositorio_senas WHERE id_sena = %s", (id_sena,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_sena(data):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO repositorio_senas (palabra_asociada, archivo_video, validada) VALUES (%s,%s,%s)",
                (data.get('palabra_asociada'), data.get('archivo_video'), bool(data.get('validada', False)))
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_sena(id_sena, data):
    conn = get_connection()
    if not conn:
        return False
    try:
        fields = []
        params = []
        for key in ('palabra_asociada', 'archivo_video', 'validada'):
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(id_sena)
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE repositorio_senas SET {', '.join(fields)} WHERE id_sena = %s", tuple(params))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_sena(id_sena):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM repositorio_senas WHERE id_sena = %s", (id_sena,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
