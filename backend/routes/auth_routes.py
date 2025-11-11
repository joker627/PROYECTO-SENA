from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from backend.models.usuarios_models import get_user_by_email
from backend.models.usuarios_models import verify_password

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    """Authentication endpoints (GET shows form, POST authenticates using DB).

    This uses the `usuarios` table defined in `sign_technology.sql`. Passwords
    are expected to be stored hashed (Werkzeug generate_password_hash). The
    model provides a fallback to plaintext for legacy data, but you should
    migrate passwords to hashed values.
    """
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '')

        if not correo or not contrasena:
            flash('Credenciales incompletas', 'error')
            return render_template('auth/login.html')

        user = get_user_by_email(correo)
        if not user:
            flash('Usuario o contraseña inválidos', 'error')
            return render_template('auth/login.html')

        stored = user.get('contrasena')
        if not verify_password(stored, contrasena):
            flash('Usuario o contraseña inválidos', 'error')
            return render_template('auth/login.html')

        # Authentication successful -> populate session
        session['usuario'] = {'correo': user.get('correo')}
        session['user_id'] = user.get('id_usuario')
        # Prefer full name, fallback to local-part of email
        session['user_name'] = user.get('nombre_completo') or user.get('correo', '').split('@', 1)[0]
        session['id_rol'] = user.get('id_rol') or 2

        flash('Inicio de sesión correcto', 'success')
        if session['id_rol'] == 1:
            return redirect(url_for('general_bp.admin_dashboard'))
        return redirect(url_for('general_bp.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('general_bp.index'))
