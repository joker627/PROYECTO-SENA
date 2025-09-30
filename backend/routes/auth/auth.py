# backend/routes/auth/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from backend.models.user_model import validate_user, register_user, get_user_by_email, get_all_roles


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        user = validate_user(correo, contrasena)
        if user:
            session['user'] = user
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
    roles = get_all_roles()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        id_rol = request.form.get('rol')
        # Validar si el correo ya está registrado
        if get_user_by_email(correo):
            flash('El correo ya está registrado. Usa otro.', 'danger')
            return render_template('auth/register.html', user=session.get('user'), roles=roles)
        try:
            # Registrar usuario con los campos correctos
            registro_exitoso = register_user(nombre, correo, contrasena, id_rol)
            if registro_exitoso:
                flash('Usuario registrado con éxito', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Error al registrar usuario.', 'danger')
                return render_template('auth/register.html', user=session.get('user'), roles=roles)
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('auth/register.html', user=session.get('user'), roles=roles)
    return render_template('auth/register.html', user=session.get('user'), roles=roles)

# Ruta para el perfil de usuario
@auth_bp.route('/profile')
def profile():
    user = session.get('user')
    return render_template('auth/profile.html', user=user)
