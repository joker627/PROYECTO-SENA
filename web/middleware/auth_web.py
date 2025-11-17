from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Debes iniciar sesión primero.", "error")
            return redirect(url_for("web_login.login_post"))
        return func(*args, **kwargs)
    return wrapper


def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = session.get("rol")

            if not role:
                flash("Debes iniciar sesión.", "error")
                return redirect(url_for("web_login.login_post"))

            if role not in roles:
                flash("No tienes permisos para acceder aquí.", "error")
                return redirect(url_for("web_bp.inicio"))

            return func(*args, **kwargs)
        return wrapper
    return decorator

