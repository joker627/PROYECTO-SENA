"""Model: contribuciones"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_all_contribuciones(limit=100, offset=0):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM contribuciones ORDER BY fecha_envio DESC LIMIT %s OFFSET %s", (limit, offset))
            return cursor.fetchall()
    finally:
        conn.close()


def get_contribucion_by_id(id_contribucion):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM contribuciones WHERE id_contribucion = %s", (id_contribucion,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_contribucion(data):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO contribuciones (id_usuario, descripcion, archivo_prueba, estado) VALUES (%s,%s,%s,%s)",
                (data.get('id_usuario'), data.get('descripcion'), data.get('archivo_prueba'), data.get('estado', 'pendiente'))
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_contribucion(id_contribucion, data):
    conn = get_connection()
    if not conn:
        return False
    try:
        fields = []
        params = []
        for key in ('id_usuario', 'descripcion', 'archivo_prueba', 'estado'):
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(id_contribucion)
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE contribuciones SET {', '.join(fields)} WHERE id_contribucion = %s", tuple(params))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_contribucion(id_contribucion):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM contribuciones WHERE id_contribucion = %s", (id_contribucion,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
