# backend/controllers/profile_controller.py
"""
Controlador de perfil de usuario
Maneja todas las operaciones relacionadas con la gestión del perfil
"""
from flask import session, flash
from models.user_model import (
    update_user_username, update_user_email, 
    verify_current_password, change_user_password,
    delete_user_account, get_user_by_id
)
import re


class ProfileController:
    
    @staticmethod
    def update_username(new_username):
        user = session.get('user')
        if not user:
            return False, 'Debes iniciar sesión'
        
        # Validaciones
        if not new_username or not new_username.strip():
            return False, 'El nombre de usuario es obligatorio'
        
        new_username = new_username.strip()
        
        if len(new_username) < 3:
            return False, 'El nombre debe tener al menos 3 caracteres'
        
        if len(new_username) > 50:
            return False, 'El nombre no puede tener más de 50 caracteres'
        
        # Actualizar en base de datos
        try:
            success = update_user_username(user['id_usuario'], new_username)
            if success:
                # Actualizar sesión
                session['user']['nombre'] = new_username
                return True, 'Nombre de usuario actualizado correctamente'
            else:
                return False, 'Error al actualizar el nombre de usuario'
        except Exception as e:
            return False, f'Error: {e}'
    
    @staticmethod
    def update_email(new_email):
        user = session.get('user')
        if not user:
            return False, 'Debes iniciar sesión'
        
        # Validaciones
        if not new_email or not new_email.strip():
            return False, 'El correo electrónico es obligatorio'
        
        new_email = new_email.strip().lower()
        
        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, new_email):
            return False, 'El formato del correo electrónico no es válido'
        
        # Actualizar en base de datos
        try:
            success = update_user_email(user['id_usuario'], new_email)
            if success:
                # Actualizar sesión
                session['user']['correo'] = new_email
                return True, 'Correo electrónico actualizado correctamente'
            else:
                return False, 'Error al actualizar el correo electrónico'
        except Exception as e:
            return False, f'Error: {e}'
    
    @staticmethod
    def change_password(current_password, new_password, confirm_password):
        user = session.get('user')
        if not user:
            return False, 'Debes iniciar sesión'
        
        # Validaciones básicas
        if not all([current_password, new_password, confirm_password]):
            return False, 'Todos los campos son obligatorios'
        
        if new_password != confirm_password:
            return False, 'Las contraseñas nuevas no coinciden'
        
        if len(new_password) < 6:
            return False, 'La nueva contraseña debe tener al menos 6 caracteres'
        
        # Verificar contraseña actual
        if not verify_current_password(user['id_usuario'], current_password):
            return False, 'La contraseña actual es incorrecta'
        
        # Cambiar contraseña
        try:
            success = change_user_password(user['id_usuario'], new_password)
            if success:
                return True, 'Contraseña cambiada exitosamente'
            else:
                return False, 'Error al cambiar la contraseña'
        except Exception as e:
            return False, f'Error: {e}'
    
    @staticmethod
    def delete_account(confirm_text):
        user = session.get('user')
        if not user:
            return False, 'Debes iniciar sesión'
        
        # Validar confirmación
        if confirm_text.upper().strip() != 'ELIMINAR':
            return False, 'Debes escribir "ELIMINAR" para confirmar'
        
        # Eliminar cuenta
        try:
            success = delete_user_account(user['id_usuario'])
            if success:
                session.clear()
                return True, 'Tu cuenta ha sido eliminada permanentemente'
            else:
                return False, 'Error al eliminar la cuenta'
        except Exception as e:
            return False, f'Error: {e}'
    
    @staticmethod
    def get_user_profile():
        user = session.get('user')
        if not user:
            return None
        
        # Obtener datos actualizados de la base de datos
        updated_user = get_user_by_id(user['id_usuario'])
        if updated_user:
            # Actualizar sesión con datos frescos
            session['user'] = updated_user
            return updated_user
        
        return user