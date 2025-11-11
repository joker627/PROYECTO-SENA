"""Model: roles"""
from connection.db import get_connection
from pymysql.cursors import DictCursor


def get_all_roles():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT id_rol, nombre_rol FROM roles ORDER BY id_rol")
            return cursor.fetchall()
    finally:
        conn.close()


def get_role_by_id(id_rol):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT id_rol, nombre_rol FROM roles WHERE id_rol = %s", (id_rol,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_role(nombre_rol):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO roles (nombre_rol) VALUES (%s)", (nombre_rol,))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_role(id_rol, nombre_rol):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE roles SET nombre_rol = %s WHERE id_rol = %s", (nombre_rol, id_rol))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_role(id_rol):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM roles WHERE id_rol = %s", (id_rol,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()
