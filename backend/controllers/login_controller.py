from flask import request, redirect, url_for, flash, session
from models.login_models import verificar_usuario
from utils.error_handler import ErrorHandler

def iniciar_sesion():
    try:
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        usuario = verificar_usuario(correo, contrasena)

        if usuario:
            session['usuario'] = usuario
            session['user_id'] = usuario.get('id_usuario') or usuario.get('id')
            session['user_name'] = usuario.get('nombre') or usuario.get('name')
            session['id_rol'] = usuario.get('id_rol')
            session.permanent = True
            flash(f"Bienvenido {session['user_name']} 👋", "success")

            if session.get('id_rol') == 1:
                return redirect(url_for('admin_bp.dashboard'))
            elif session.get('id_rol') == 2:
                return redirect(url_for('general_bp.inicio'))
            else:
                flash("Rol desconocido", "warning")
                return redirect(url_for('login_bp.login'))
        else:
            flash("Correo o contraseña incorrectos ❌", "danger")
            return redirect(url_for('login_bp.login'))
    except Exception as e:
        ErrorHandler.error_auth('iniciar_sesion', f'Error en proceso de login: {str(e)}', 'controllers/login_controller.py')
        flash("Error en el sistema de autenticación", "danger")
        return redirect(url_for('login_bp.login'))
