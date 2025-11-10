from models.usuario_anonimo_models import (
    crear_usuario_anonimo as model_crear_usuario_anonimo,
    obtener_por_uuid as model_obtener_por_uuid,
    obtener_por_id as model_obtener_por_id,
    obtener_todos as model_obtener_todos,
    obtener_estadisticas as model_obtener_estadisticas
)
from flask import request
from utils.error_handler import capturar_error


@capturar_error(modulo='usuario_anonimo', severidad='alto')
def crear_usuario_anonimo():
    """Crear nuevo usuario anónimo"""
    # Obtener IP del usuario
    ip_usuario = request.remote_addr
    # Crear usuario anónimo
    resultado = model_crear_usuario_anonimo(ip_usuario)
    return resultado


@capturar_error(modulo='usuario_anonimo', severidad='medio')
def obtener_usuario_por_uuid(uuid_transaccion):
    """Obtener usuario anónimo por UUID"""
    usuario = model_obtener_por_uuid(uuid_transaccion)
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


@capturar_error(modulo='usuario_anonimo', severidad='medio')
def obtener_usuario_por_id(id_anonimo):
    """Obtener usuario anónimo por ID"""
    usuario = model_obtener_por_id(id_anonimo)
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


@capturar_error(modulo='usuario_anonimo', severidad='medio')
def listar_usuarios_anonimos(pagina=1, por_pagina=50):
    """Listar usuarios anónimos con paginación"""
    offset = (pagina - 1) * por_pagina
    resultado = model_obtener_todos(limite=por_pagina, offset=offset)
    return {
        'success': True,
        'usuarios': resultado['usuarios'],
        'total': resultado['total'],
        'pagina': pagina,
        'por_pagina': por_pagina,
        'total_paginas': (resultado['total'] + por_pagina - 1) // por_pagina
    }


@capturar_error(modulo='usuario_anonimo', severidad='medio')
def obtener_estadisticas():
    """Obtener estadísticas de usuarios anónimos"""
    stats = model_obtener_estadisticas()
    return {
        'success': True,
        'estadisticas': stats
    }

