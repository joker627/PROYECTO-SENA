# backend/routes/profile_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.auth_controller import AuthController
from controllers.profile_controller import ProfileController


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


def require_login():
    if not AuthController.require_login():
        flash('Debes iniciar sesión para acceder al perfil', 'danger')
        return redirect(url_for('auth.login'))
    return None


@profile_bp.route('/')
def index():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    user = ProfileController.get_user_profile()
    return render_template('auth/profile/index.html', user=user)


@profile_bp.route('/update-username', methods=['POST'])
def update_username():
    """Actualizar nombre de usuario"""
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    new_username = request.form.get('new_username', '')
    success, message = ProfileController.update_username(new_username)
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('profile.index'))


@profile_bp.route('/update-email', methods=['POST'])
def update_email():
    """Actualizar correo electrónico"""
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    new_email = request.form.get('new_email', '')
    success, message = ProfileController.update_email(new_email)
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('profile.index'))


@profile_bp.route('/change-password', methods=['POST'])
def change_password():
    """Cambiar contraseña"""
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    success, message = ProfileController.change_password(
        current_password, new_password, confirm_password
    )
    
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('profile.index'))


@profile_bp.route('/delete-account', methods=['POST'])
def delete_account():
    """Eliminar cuenta"""
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    confirm_text = request.form.get('confirm_delete', '')
    success, message = ProfileController.delete_account(confirm_text)
    
    if success:
        flash(message, 'info')
        return redirect(url_for('auth.login'))
    else:
        flash(message, 'danger')
        return redirect(url_for('profile.index'))