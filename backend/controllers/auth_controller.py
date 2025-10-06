# backend/controllers/auth_controller.py
"""
Controlador de autenticación
Maneja todas las operaciones relacionadas con login, registro y sesiones
"""
from flask import session, flash, redirect, url_for
from models.user_model import validate_user, register_user, get_user_by_email, get_all_roles
import re


class AuthController:
    
    @staticmethod
    def login_user(correo, contrasena):
        if not correo or not contrasena:
            return False, 'Correo y contraseña son obligatorios'
        
        user = validate_user(correo, contrasena)
        if user:
            session['user'] = user
            return True, '¡Bienvenido!'
        else:
            return False, 'Correo o contraseña incorrectos'
    
    @staticmethod
    def logout_user():
        session.pop('user', None)
        return True, 'Has cerrado sesión'
    
    @staticmethod
    def register_new_user(nombre, correo, contrasena, id_rol):
        # Validaciones
        if not all([nombre, correo, contrasena, id_rol]):
            return False, 'Todos los campos son obligatorios'
        
        if len(nombre) < 3:
            return False, 'El nombre debe tener al menos 3 caracteres'
        
        if len(contrasena) < 6:
            return False, 'La contraseña debe tener al menos 6 caracteres'
        
        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, correo):
            return False, 'El formato del correo no es válido'
        
        # Verificar si el email ya existe
        if get_user_by_email(correo):
            return False, 'El correo ya está registrado'
        
        # Registrar usuario
        try:
            success = register_user(nombre, correo, contrasena, id_rol)
            if success:
                return True, 'Usuario registrado con éxito'
            else:
                return False, 'Error al registrar usuario'
        except Exception as e:
            return False, f'Error al registrar usuario: {e}'
    
    @staticmethod
    def require_login():
        return 'user' in session
    
    @staticmethod
    def get_current_user():
        return session.get('user')