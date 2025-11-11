"""Model: reportes_errores"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_all_reportes(limit=100, offset=0):
    conn = get_connection()
    if not conn:
        return {'reportes': [], 'total': 0}
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM reportes_errores ORDER BY fecha_reporte DESC LIMIT %s OFFSET %s", (limit, offset))
            rows = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as total FROM reportes_errores")
            total = cursor.fetchone().get('total', 0)
            return {'reportes': rows, 'total': total}
    finally:
        conn.close()


def get_reporte_by_id(id_reporte):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_reporte(data):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO reportes_errores (id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    data.get('id_traduccion'),
                    data.get('tipo_traduccion'),
                    data.get('descripcion_error'),
                    data.get('evidencia_url'),
                    data.get('prioridad', 'media'),
                    data.get('estado', 'pendiente'),
                )
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_reporte(id_reporte, data):
    conn = get_connection()
    if not conn:
        return False
    try:
        fields = []
        params = []
        for key in ('id_traduccion', 'tipo_traduccion', 'descripcion_error', 'evidencia_url', 'prioridad', 'estado'):
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(id_reporte)
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE reportes_errores SET {', '.join(fields)} WHERE id_reporte = %s", tuple(params))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_reporte(id_reporte):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM reportes_errores WHERE id_reporte = %s", (id_reporte,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()