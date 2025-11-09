from models.usuario_anonimo_models import UsuarioAnonimoModel
from flask import request


class UsuarioAnonimoController:
    
    @staticmethod
    def crear_usuario_anonimo():
        """Crear nuevo usuario anónimo"""
        # Obtener IP del usuario
        ip_usuario = request.remote_addr
        
        # Crear usuario anónimo
        resultado = UsuarioAnonimoModel.crear_usuario_anonimo(ip_usuario)
        
        return resultado
    
    
    @staticmethod
    def obtener_usuario_por_uuid(uuid_transaccion):
        """Obtener usuario anónimo por UUID"""
        usuario = UsuarioAnonimoModel.obtener_por_uuid(uuid_transaccion)
        
        if usuario:
            return {
                'success': True,
                'usuario': usuario
            }
        else:
            return {
                'success': False,
                'error': 'Usuario anónimo no encontrado'
            }
    
    
    @staticmethod
    def obtener_usuario_por_id(id_anonimo):
        """Obtener usuario anónimo por ID"""
        usuario = UsuarioAnonimoModel.obtener_por_id(id_anonimo)
        
        if usuario:
            return {
                'success': True,
                'usuario': usuario
            }
        else:
            return {
                'success': False,
                'error': 'Usuario anónimo no encontrado'
            }
    
    
    @staticmethod
    def listar_usuarios_anonimos(pagina=1, por_pagina=50):
        """Listar usuarios anónimos con paginación"""
        offset = (pagina - 1) * por_pagina
        
        resultado = UsuarioAnonimoModel.obtener_todos(limite=por_pagina, offset=offset)
        
        return {
            'success': True,
            'usuarios': resultado['usuarios'],
            'total': resultado['total'],
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': (resultado['total'] + por_pagina - 1) // por_pagina
        }
    
    
    @staticmethod
    def obtener_estadisticas():
        """Obtener estadísticas de usuarios anónimos"""
        stats = UsuarioAnonimoModel.obtener_estadisticas()
        
        return {
            'success': True,
            'estadisticas': stats
        }
