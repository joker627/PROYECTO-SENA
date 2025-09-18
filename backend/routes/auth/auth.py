# backend/routes/auth/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import validate_user, register_user, get_user_by_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        user = validate_user(correo, contrasena)
        if user:
            session['user'] = user['nombre']
            flash('¡Bienvenido', 'success')
            return redirect(url_for('main.inicio'))
        else:
            flash('correo o contraseña incorrectos', 'danger')
            return render_template('auth/login.html', user=session.get('user'))
    return render_template('auth/login.html', user=session.get('user'))

# logout route
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión', 'danger')
    return redirect(url_for('auth.login'))

# register route
@auth_bp.route('/register', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        # Validar si el correo ya está registrado
        if get_user_by_email(correo):
            flash('El correo ya está registrado. Usa otro.', 'danger')
            return render_template('auth/register.html', user=session.get('user'))
        try:
            # Registrar usuario con los campos correctos
            registro_exitoso = register_user(nombre, correo, contrasena)
            if registro_exitoso:
                flash('Usuario registrado con éxito', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Error al registrar usuario.', 'danger')
                return render_template('auth/register.html', user=session.get('user'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('auth/register.html', user=session.get('user'))
    return render_template('auth/register.html', user=session.get('user'))

# Ruta para el perfil de usuario
@auth_bp.route('/profile')
def profile():
    from flask import session
    user = session.get('user')
    return render_template('auth/profile.html', user=user)