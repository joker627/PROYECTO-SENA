"""
Rutas para la gestión de usuarios/colaboradores del sistema
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.usuarios_controller import (
    get_page_data, create_usuario, update_usuario,
    change_estado, change_rol, delete_usuario
)
from utils.error_handler import error_generico
from functools import wraps

usuarios_bp = Blueprint('usuarios_bp', __name__, url_prefix='/usuarios')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('login_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('login_bp.login'))
        
        # Verificar si el usuario es administrador (id_rol == 1)
        if session.get('id_rol') != 1:
            flash('No tienes permisos para acceder a esta sección', 'error')
            return redirect(url_for('admin_bp.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

@usuarios_bp.route('/')
@admin_required
def usuarios_page():
    """Página principal de gestión de usuarios"""
    try:
        data = get_page_data()
        
        return render_template(
            'admin/usuarios.html',
            usuarios=data['usuarios'],
            stats=data['stats']
        )
    except Exception as e:
        print(f"Error en usuarios_page: {e}")
        error_generico('usuarios_page', f'Error: {str(e)}', 'alto', 'routes/usuarios_routes.py', 'Error Página Usuarios')
        flash('Error al cargar usuarios', 'error')
        return redirect(url_for('admin_bp.dashboard'))

@usuarios_bp.route('/crear', methods=['POST'])
@admin_required
def crear_usuario():
    """Crear un nuevo usuario"""
    try:
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol', 'colaborador')
        
        result = create_usuario(nombre, correo, contrasena, rol)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        error_generico('crear_usuario', f'Error: {str(e)}', 'medio', 'routes/usuarios_routes.py', 'Error Crear Usuario')
        flash('Error al crear usuario', 'error')
    
    return redirect(url_for('usuarios_bp.usuarios_page'))

@usuarios_bp.route('/editar/<int:id_usuario>', methods=['POST'])
@admin_required
def editar_usuario(id_usuario):
    """Editar un usuario existente"""
    try:
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        rol = request.form.get('rol')
        
        result = update_usuario(id_usuario, nombre, correo, rol)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
    except Exception as e:
        print(f"Error al editar usuario: {e}")
        error_generico('editar_usuario', f'Error: {str(e)}', 'medio', 'routes/usuarios_routes.py', 'Error Editar Usuario')
        flash('Error al editar usuario', 'error')
    
    return redirect(url_for('usuarios_bp.usuarios_page'))

@usuarios_bp.route('/cambiar-estado/<int:id_usuario>', methods=['POST'])
@admin_required
def cambiar_estado(id_usuario):
    """Cambiar estado de un usuario"""
    try:
        nuevo_estado = request.form.get('estado')
        
        result = change_estado(id_usuario, nuevo_estado)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
    except Exception as e:
        print(f"Error al cambiar estado: {e}")
        error_generico('cambiar_estado', f'Error: {str(e)}', 'medio', 'routes/usuarios_routes.py', 'Error Cambiar Estado Usuario')
        flash('Error al cambiar estado', 'error')
    
    return redirect(url_for('usuarios_bp.usuarios_page'))

@usuarios_bp.route('/cambiar-rol/<int:id_usuario>', methods=['POST'])
@admin_required
def cambiar_rol(id_usuario):
    """Cambiar rol de un usuario"""
    try:
        nuevo_rol = request.form.get('rol')
        
        result = change_rol(id_usuario, nuevo_rol)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
    except Exception as e:
        print(f"Error al cambiar rol: {e}")
        error_generico('cambiar_rol', f'Error: {str(e)}', 'medio', 'routes/usuarios_routes.py', 'Error Cambiar Rol Usuario')
        flash('Error al cambiar rol', 'error')
    
    return redirect(url_for('usuarios_bp.usuarios_page'))

@usuarios_bp.route('/eliminar/<int:id_usuario>', methods=['POST'])
@admin_required
def eliminar_usuario(id_usuario):
    """Eliminar un usuario"""
    try:
        # No permitir eliminar al usuario actual
        if id_usuario == session.get('user_id'):
            flash('No puedes eliminar tu propia cuenta', 'error')
            return redirect(url_for('usuarios_bp.usuarios_page'))
        
        result = delete_usuario(id_usuario)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        error_generico('eliminar_usuario', f'Error: {str(e)}', 'medio', 'routes/usuarios_routes.py', 'Error Eliminar Usuario')
        flash('Error al eliminar usuario', 'error')
    
    return redirect(url_for('usuarios_bp.usuarios_page'))

@usuarios_bp.route('/eliminar-por-email', methods=['POST'])
@admin_required
def eliminar_por_email():
    """Eliminar usuario por correo electrónico con motivo"""
    try:
        email = request.form.get('email_usuario', '').strip()
        motivo = request.form.get('motivo_eliminacion', '').strip()
        
        if not email or not motivo:
            flash('Correo y motivo son requeridos', 'error')
            return redirect(url_for('usuarios_bp.usuarios_page'))
        
        # Buscar usuario por email
        from models.usuarios_models import get_all_usuarios as model_get_all_usuarios
        usuarios = model_get_all_usuarios()
        usuario = next((u for u in usuarios if u['correo'] == email), None)
        
        if not usuario:
            flash(f'No se encontró ningún usuario con el correo: {email}', 'error')
            return redirect(url_for('usuarios_bp.usuarios_page'))
        
        # No permitir eliminar al usuario actual
        if usuario['id_usuario'] == session.get('user_id'):
            flash('No puedes eliminar tu propia cuenta', 'error')
            return redirect(url_for('usuarios_bp.usuarios_page'))
        
        # Registrar el motivo en logs antes de eliminar
        print(f"🚨 ELIMINACIÓN DE CUENTA: Usuario {usuario['nombre']} ({email})")
        print(f"   Motivo: {motivo}")
        print(f"   Eliminado por: Admin ID {session.get('user_id')}")
        
        # Eliminar usuario
        result = delete_usuario(usuario['id_usuario'])
        
        if result['success']:
            flash(f'✅ Usuario {usuario["nombre"]} eliminado. Motivo: {motivo}', 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        print(f"Error al eliminar usuario por email: {e}")
        error_generico('eliminar_por_email', f'Error: {str(e)}', 'alto', 'routes/usuarios_routes.py', 'Error Eliminar Usuario por Email')
        flash('Error al procesar la eliminación', 'error')
    
    return redirect(url_for('usuarios_bp.usuarios_page'))
