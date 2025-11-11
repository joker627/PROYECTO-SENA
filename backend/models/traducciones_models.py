"""Model: traducciones"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_all_traducciones(limit=100, offset=0):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM traducciones ORDER BY fecha_traduccion DESC LIMIT %s OFFSET %s", (limit, offset))
            return cursor.fetchall()
    finally:
        conn.close()


def get_traduccion_by_id(id_traduccion):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM traducciones WHERE id_traduccion = %s", (id_traduccion,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_traduccion(data):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO traducciones (tipo_traduccion, texto_entrada, enlace_sena_entrada, resultado_salida, fallo)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data.get('tipo_traduccion'),
                data.get('texto_entrada'),
                data.get('enlace_sena_entrada'),
                data.get('resultado_salida'),
                bool(data.get('fallo', False)),
            ))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_traduccion(id_traduccion, data):
    conn = get_connection()
    if not conn:
        return False
    try:
        fields = []
        params = []
        for key in ('tipo_traduccion', 'texto_entrada', 'enlace_sena_entrada', 'resultado_salida', 'fallo'):
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(id_traduccion)
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE traducciones SET {', '.join(fields)} WHERE id_traduccion = %s", tuple(params))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_traduccion(id_traduccion):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM traducciones WHERE id_traduccion = %s", (id_traduccion,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
