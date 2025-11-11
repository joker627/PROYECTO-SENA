"""Model: usuarios - access to usuarios table and helpers for auth
"""
from connection.db import get_connection
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash


def get_user_by_email(correo):
    """Return a dict with user record or None. Quietly returns None on DB errors."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return None
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT id_usuario, nombre_completo, correo, contrasena, id_rol, estado FROM usuarios WHERE correo = %s", (correo,))
            return cursor.fetchone()
    except Exception:
        # Don't raise in model layer for simple auth flows; caller can treat None as not found.
        return None
    finally:
        if conn:
            conn.close()


def create_user(nombre_completo, correo, contrasena_plain, id_rol=2):
    """Create a new user with hashed password. Returns new id or None on error."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return None
        hashed = generate_password_hash(contrasena_plain)
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (nombre_completo, correo, contrasena, id_rol) VALUES (%s, %s, %s, %s)",
                           (nombre_completo, correo, hashed, id_rol))
            conn.commit()
            return cursor.lastrowid
    except Exception:
        return None
    finally:
        if conn:
            conn.close()


def verify_password(hashed_or_plain, candidate_password):
    """Verify password: supports hashed values (check_password_hash) and as fallback plain equality.
    Returns True if match, False otherwise."""
    try:
        # If stored value looks like a Werkzeug hash (starts with 'pbkdf2:' or 'sha256:'), use check_password_hash
        if isinstance(hashed_or_plain, str) and (hashed_or_plain.startswith('pbkdf2:') or hashed_or_plain.startswith('sha256:') or hashed_or_plain.startswith('argon2:')):
            return check_password_hash(hashed_or_plain, candidate_password)
        # fallback to direct comparison (for legacy plaintext passwords)
        return hashed_or_plain == candidate_password
    except Exception:
        return False


def update_user_role(id_usuario, id_rol):
    """Update the role of a user. Returns True on success."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return False
        with conn.cursor() as cursor:
            cursor.execute("UPDATE usuarios SET id_rol = %s WHERE id_usuario = %s", (id_rol, id_usuario))
            conn.commit()
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def update_user_estado(id_usuario, estado):
    """Update the estado (activo/inactivo) of a user. Returns True on success."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return False
        with conn.cursor() as cursor:
            cursor.execute("UPDATE usuarios SET estado = %s WHERE id_usuario = %s", (estado, id_usuario))
            conn.commit()
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def delete_user_by_id(id_usuario):
    """Delete a user by id. Returns True on success."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return False
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def delete_user_by_email(correo):
    """Delete users by email. Returns number of deleted rows or None on error."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return None
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE correo = %s", (correo,))
            affected = cursor.rowcount
            conn.commit()
            return affected
    except Exception:
        return None
    finally:
        if conn:
            conn.close()


def list_users(limit=None, offset=0):
    """Return a list of usuarios as dicts for templates.

    Each returned dict contains keys expected by the templates:
    - id_usuario, nombre, correo, id_rol, rol, estado, tiempo_registro, tiempo_ultimo_acceso
    """
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return []
        with conn.cursor(DictCursor) as cursor:
            # `fecha_ultimo_acceso` does not exist in the schema; select only available columns
            sql = "SELECT id_usuario, nombre_completo, correo, id_rol, estado, fecha_registro FROM usuarios"
            params = []
            if limit:
                sql = sql + " LIMIT %s OFFSET %s"
                params = [limit, offset]
            cursor.execute(sql, tuple(params) if params else None)
            rows = cursor.fetchall() or []

            usuarios = []
            for r in rows:
                nombre = r.get('nombre_completo') or r.get('nombre') or ''
                estado = (r.get('estado') or '').upper()
                id_rol = r.get('id_rol') or 2
                rol = 'Administrador' if int(id_rol) == 1 else 'Gestor'
                # Simple human-friendly times (templates expect preformatted strings). Keep raw DB values too.
                tiempo_registro = ''
                tiempo_ultimo_acceso = ''
                fr = r.get('fecha_registro')
                fa = r.get('fecha_ultimo_acceso')
                if fr:
                    tiempo_registro = str(fr)
                if fa:
                    tiempo_ultimo_acceso = str(fa)

                usuarios.append({
                    'id_usuario': r.get('id_usuario'),
                    'nombre': nombre,
                    'correo': r.get('correo'),
                    'id_rol': id_rol,
                    'rol': rol,
                    'estado': estado,
                    'tiempo_registro': tiempo_registro,
                    'tiempo_ultimo_acceso': tiempo_ultimo_acceso,
                })
            return usuarios
    except Exception:
        # Return None on error so callers can distinguish "no rows" from "DB error"
        return None
    finally:
        if conn:
            conn.close()
