"""
Controlador para la gestión de usuarios del sistema
"""
from models.usuarios_models import (
    get_all_usuarios as model_get_all_usuarios,
    get_usuario_by_id as model_get_usuario_by_id,
    create_usuario as model_create_usuario,
    update_usuario as model_update_usuario,
    delete_usuario as model_delete_usuario,
    count_by_rol as model_count_by_rol,
    count_by_estado as model_count_by_estado,
)
import hashlib
from utils.error_handler import capturar_error


@capturar_error(modulo='usuarios', severidad='medio')
def get_all_usuarios():
    """Obtener todos los usuarios"""
    return model_get_all_usuarios()


@capturar_error(modulo='usuarios', severidad='medio')
def get_usuario_by_id(id_usuario):
    """Obtener un usuario específico"""
    return model_get_usuario_by_id(id_usuario)


@capturar_error(modulo='usuarios', severidad='alto')
def create_usuario(nombre, correo, contrasena, id_rol):
    """Crear un nuevo usuario"""
    # Hash de la contraseña
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
    
    # Validar datos
    if not nombre or not correo or not contrasena:
        return {'success': False, 'message': 'Todos los campos son requeridos'}
    
    if len(contrasena) < 6:
        return {'success': False, 'message': 'La contraseña debe tener al menos 6 caracteres'}
    
    # Validar que el id_rol sea 1 (ADMINISTRADOR) o 2 (GESTOR)
    try:
        id_rol = int(id_rol)
        if id_rol not in [1, 2]:
            return {'success': False, 'message': 'Rol no válido'}
    except (ValueError, TypeError):
        return {'success': False, 'message': 'Rol no válido'}
    
    # Crear usuario
    id_usuario = model_create_usuario(nombre, correo, contrasena_hash, id_rol)
    
    if id_usuario:
        rol_nombre = 'Administrador' if id_rol == 1 else 'Gestor'
        return {'success': True, 'message': f'Usuario creado correctamente con rol {rol_nombre}', 'id': id_usuario}
    else:
        return {'success': False, 'message': 'Error al crear usuario. El correo puede estar duplicado.'}


@capturar_error(modulo='usuarios', severidad='alto')
def update_usuario(id_usuario, nombre=None, correo=None, rol=None, estado=None):
    """Actualizar un usuario"""
    success = model_update_usuario(id_usuario, nombre, correo, rol, estado)
    
    if success:
        return {'success': True, 'message': 'Usuario actualizado correctamente'}
    else:
        return {'success': False, 'message': 'Error al actualizar usuario'}


@capturar_error(modulo='usuarios', severidad='alto')
def delete_usuario(id_usuario):
    """Eliminar un usuario"""
    success = model_delete_usuario(id_usuario)
    
    if success:
        return {'success': True, 'message': 'Usuario eliminado correctamente'}
    else:
        return {'success': False, 'message': 'Error al eliminar usuario'}


@capturar_error(modulo='usuarios', severidad='alto')
def change_estado(id_usuario, nuevo_estado):
    """Cambiar estado de un usuario"""
    # Validar que sea un estado válido (uppercase)
    if nuevo_estado not in ['ACTIVO', 'INACTIVO', 'ELIMINADO']:
        return {'success': False, 'message': 'Estado no válido'}
    
    success = model_update_usuario(id_usuario, estado=nuevo_estado)
    
    if success:
        return {'success': True, 'message': f'Usuario marcado como {nuevo_estado}'}
    else:
        return {'success': False, 'message': 'Error al cambiar estado'}


@capturar_error(modulo='usuarios', severidad='alto')
def change_rol(id_usuario, nuevo_rol):
    """Cambiar rol de un usuario"""
    # Validar que sea id_rol válido (1 o 2)
    try:
        nuevo_rol = int(nuevo_rol)
        if nuevo_rol not in [1, 2]:
            return {'success': False, 'message': 'Rol no válido'}
    except (ValueError, TypeError):
        return {'success': False, 'message': 'Rol no válido'}
    
    success = model_update_usuario(id_usuario, id_rol=nuevo_rol)
    
    if success:
        rol_nombre = 'Administrador' if nuevo_rol == 1 else 'Gestor'
        return {'success': True, 'message': f'Rol cambiado a {rol_nombre}'}
    else:
        return {'success': False, 'message': 'Error al cambiar rol'}


@capturar_error(modulo='usuarios', severidad='medio')
def get_page_data():
    """Obtener datos para la página de gestión de usuarios"""
    usuarios = get_all_usuarios()
    count_rol = model_count_by_rol()
    count_estado = model_count_by_estado()
    
    return {
        'usuarios': usuarios,
        'stats': {
            'total': len(usuarios),
            'administradores': count_rol.get('ADMINISTRADOR', 0),
            'gestores': count_rol.get('GESTOR', 0),
            'activos': count_estado.get('ACTIVO', 0),
            'inactivos': count_estado.get('INACTIVO', 0)
        }
    }
