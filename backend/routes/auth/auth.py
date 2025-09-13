# backend/routes/auth/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import validate_user, register_user, get_user_by_username

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = validate_user(username, password)
        if user:
            session['user'] = user['username']
            flash('¡Bienvenido', 'success')
            return redirect(url_for('main.inicio'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return render_template('auth/login.html', user=session.get('user'))
    return render_template('auth/login.html', user=session.get('user'))

# logout route
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('auth.login'))

# register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if get_user_by_username(username):
            flash('El nombre de usuario ya existe. Elige otro.', 'error')
            return render_template('auth/register.html', user=session.get('user'))
        try:
            register_user(username, password, email)
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'error')
            return render_template('auth/register.html', user=session.get('user'))
    return render_template('auth/register.html', user=session.get('user'))