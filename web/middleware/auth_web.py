from flask import session, redirect, url_for, flash

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión primero.", "error")
            return redirect(url_for("web_login.login_post"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def role_required(roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            rol = session.get("rol")

            if not rol:
                flash("Debes iniciar sesión.", "error")
                return redirect(url_for("web_login.login_post"))

            if rol not in roles:
                flash("No tienes permisos para acceder aquí.", "error")
                return redirect(url_for("web_bp.inicio"))

            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

