"""
Controlador para la gestión de usuarios del sistema
"""
from models.usuarios_models import UsuariosModel
import hashlib


class UsuariosController:
    """Controlador para manejar la lógica de negocio de usuarios"""
    
    @staticmethod
    def get_all_usuarios():
        """Obtener todos los usuarios"""
        return UsuariosModel.get_all_usuarios()
    
    @staticmethod
    def get_usuario_by_id(id_usuario):
        """Obtener un usuario específico"""
        return UsuariosModel.get_usuario_by_id(id_usuario)
    
    @staticmethod
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
        id_usuario = UsuariosModel.create_usuario(nombre, correo, contrasena_hash, id_rol)
        
        if id_usuario:
            rol_nombre = 'Administrador' if id_rol == 1 else 'Gestor'
            return {'success': True, 'message': f'Usuario creado correctamente con rol {rol_nombre}', 'id': id_usuario}
        else:
            return {'success': False, 'message': 'Error al crear usuario. El correo puede estar duplicado.'}
    
    @staticmethod
    def update_usuario(id_usuario, nombre=None, correo=None, rol=None, estado=None):
        """Actualizar un usuario"""
        success = UsuariosModel.update_usuario(id_usuario, nombre, correo, rol, estado)
        
        if success:
            return {'success': True, 'message': 'Usuario actualizado correctamente'}
        else:
            return {'success': False, 'message': 'Error al actualizar usuario'}
    
    @staticmethod
    def delete_usuario(id_usuario):
        """Eliminar un usuario"""
        success = UsuariosModel.delete_usuario(id_usuario)
        
        if success:
            return {'success': True, 'message': 'Usuario eliminado correctamente'}
        else:
            return {'success': False, 'message': 'Error al eliminar usuario'}
    
    @staticmethod
    def change_estado(id_usuario, nuevo_estado):
        """Cambiar estado de un usuario"""
        # Validar que sea un estado válido (uppercase)
        if nuevo_estado not in ['ACTIVO', 'INACTIVO', 'ELIMINADO']:
            return {'success': False, 'message': 'Estado no válido'}
        
        success = UsuariosModel.update_usuario(id_usuario, estado=nuevo_estado)
        
        if success:
            return {'success': True, 'message': f'Usuario marcado como {nuevo_estado}'}
        else:
            return {'success': False, 'message': 'Error al cambiar estado'}
    
    @staticmethod
    def change_rol(id_usuario, nuevo_rol):
        """Cambiar rol de un usuario"""
        # Validar que sea id_rol válido (1 o 2)
        try:
            nuevo_rol = int(nuevo_rol)
            if nuevo_rol not in [1, 2]:
                return {'success': False, 'message': 'Rol no válido'}
        except (ValueError, TypeError):
            return {'success': False, 'message': 'Rol no válido'}
        
        success = UsuariosModel.update_usuario(id_usuario, id_rol=nuevo_rol)
        
        if success:
            rol_nombre = 'Administrador' if nuevo_rol == 1 else 'Gestor'
            return {'success': True, 'message': f'Rol cambiado a {rol_nombre}'}
        else:
            return {'success': False, 'message': 'Error al cambiar rol'}
    
    @staticmethod
    def get_page_data():
        """Obtener datos para la página de gestión de usuarios"""
        usuarios = UsuariosModel.get_all_usuarios()
        count_rol = UsuariosModel.count_by_rol()
        count_estado = UsuariosModel.count_by_estado()
        
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
