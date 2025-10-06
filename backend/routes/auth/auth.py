# backend/routes/auth/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController
from models.user_model import get_all_roles


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Ruta de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        
        success, message = AuthController.login_user(correo, contrasena)
        if success:
            flash(message, 'success')
            return redirect(url_for('main.inicio'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/login.html', user=AuthController.get_current_user())

# Ruta de logout
@auth_bp.route('/logout')
def logout():
    success, message = AuthController.logout_user()
    flash(message, 'info')
    return redirect(url_for('auth.login'))

# Ruta de registro
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    roles = get_all_roles()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        id_rol = request.form.get('rol')
        
        success, message = AuthController.register_new_user(nombre, correo, contrasena, id_rol)
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/register.html', 
                        user=AuthController.get_current_user(), 
                        roles=roles)

