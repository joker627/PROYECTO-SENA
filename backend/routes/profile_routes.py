# backend/routes/profile_routes.py
# Rutas relacionadas con el perfil de usuario

from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.auth_controller import AuthController
from controllers.profile_controller import ProfileController


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# Página de perfil
@profile_bp.route('/')
def index():
    if not AuthController.require_login():
        flash('Debes iniciar sesión para acceder al perfil', 'danger')
        return redirect(url_for('auth.login'))
    
    user = ProfileController.get_user_profile()
    return render_template('auth/profile/index.html', user=user)

# Cambiar nombre del usuario
@profile_bp.route('/update-username', methods=['POST'])
def update_username():
    if not AuthController.require_login():
        flash('Debes iniciar sesión para acceder al perfil', 'danger')
        return redirect(url_for('auth.login'))
    
    new_username = request.form.get('new_username', '')
    success, message = ProfileController.update_username(new_username)
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('profile.index'))

# Cambiar email
@profile_bp.route('/update-email', methods=['POST'])
def update_email():
    if not AuthController.require_login():
        flash('Debes iniciar sesión para acceder al perfil', 'danger')
        return redirect(url_for('auth.login'))
    
    new_email = request.form.get('new_email', '')
    success, message = ProfileController.update_email(new_email)
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('profile.index'))

# Cambiar contraseña
@profile_bp.route('/change-password', methods=['POST'])
def change_password():
    if not AuthController.require_login():
        flash('Debes iniciar sesión para acceder al perfil', 'danger')
        return redirect(url_for('auth.login'))
    
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    success, message = ProfileController.change_password(
        current_password, new_password, confirm_password
    )
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('profile.index'))

# Eliminar cuenta
@profile_bp.route('/delete-account', methods=['POST'])
def delete_account():
    if not AuthController.require_login():
        flash('Debes iniciar sesión para acceder al perfil', 'danger')
        return redirect(url_for('auth.login'))
    
    confirm_text = request.form.get('confirm_delete', '')
    success, message = ProfileController.delete_account(confirm_text)
    
    if success:
        flash(message, 'info')
        return redirect(url_for('auth.login'))
    else:
        flash(message, 'danger')
        return redirect(url_for('profile.index'))