"""Model: solicitudes_colaborador"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_all_solicitudes(limit=100, offset=0):
    conn = get_connection()
    if not conn:
        return {'solicitudes': [], 'total': 0}
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM solicitudes_colaborador ORDER BY fecha_solicitud DESC LIMIT %s OFFSET %s", (limit, offset))
            rows = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as total FROM solicitudes_colaborador")
            total = cursor.fetchone().get('total', 0)
            return {'solicitudes': rows, 'total': total}
    finally:
        conn.close()


def get_solicitud_by_id(id_solicitud):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM solicitudes_colaborador WHERE id_solicitud = %s", (id_solicitud,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_solicitud(data):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO solicitudes_colaborador (nombre_completo, correo, mensaje, estado) VALUES (%s,%s,%s,%s)",
                (data.get('nombre_completo'), data.get('correo'), data.get('mensaje'), data.get('estado', 'pendiente'))
            )
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_solicitud(id_solicitud, data):
    conn = get_connection()
    if not conn:
        return False
    try:
        fields = []
        params = []
        for key in ('nombre_completo', 'correo', 'mensaje', 'estado'):
            if key in data:
                fields.append(f"{key} = %s")
                params.append(data[key])
        if not fields:
            return False
        params.append(id_solicitud)
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE solicitudes_colaborador SET {', '.join(fields)} WHERE id_solicitud = %s", tuple(params))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_solicitud(id_solicitud):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM solicitudes_colaborador WHERE id_solicitud = %s", (id_solicitud,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
