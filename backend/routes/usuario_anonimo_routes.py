from flask import Blueprint, jsonify, request, session
from controllers.usuario_anonimo_controller import UsuarioAnonimoController
from utils.error_handler import ErrorHandler


usuario_anonimo_bp = Blueprint('usuario_anonimo_bp', __name__, url_prefix='/api/anonimo')


@usuario_anonimo_bp.route('/registrar', methods=['POST'])
def registrar_usuario_anonimo():
    """API: Registrar nuevo usuario anónimo"""
    try:
        resultado = UsuarioAnonimoController.crear_usuario_anonimo()
        
        if resultado['success']:
            # Guardar UUID en sesión para uso posterior
            session['uuid_anonimo'] = resultado['uuid_transaccion']
            session['id_anonimo'] = resultado['id_anonimo']
            
            return jsonify({
                'success': True,
                'message': 'Usuario anónimo registrado exitosamente',
                'uuid_transaccion': resultado['uuid_transaccion'],
                'id_anonimo': resultado['id_anonimo']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': resultado['error']
            }), 500
            
    except Exception as e:
        ErrorHandler.error_generico('registrar_usuario_anonimo', f'Error: {str(e)}', 'medio', 'routes/usuario_anonimo_routes.py', 'Error en registrar_usuario_anonimo')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@usuario_anonimo_bp.route('/validar/<uuid_transaccion>', methods=['GET'])
def validar_usuario_anonimo(uuid_transaccion):
    """API: Validar si existe un usuario anónimo por UUID"""
    try:
        resultado = UsuarioAnonimoController.obtener_usuario_por_uuid(uuid_transaccion)
        
        if resultado['success']:
            return jsonify({
                'success': True,
                'valido': True,
                'usuario': resultado['usuario']
            }), 200
        else:
            return jsonify({
                'success': True,
                'valido': False,
                'message': 'Usuario anónimo no encontrado'
            }), 404
            
    except Exception as e:
        ErrorHandler.error_generico('validar_usuario_anonimo', f'Error: {str(e)}', 'medio', 'routes/usuario_anonimo_routes.py', 'Error en validar_usuario_anonimo')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@usuario_anonimo_bp.route('/obtener/<int:id_anonimo>', methods=['GET'])
def obtener_usuario_anonimo(id_anonimo):
    """API: Obtener información de usuario anónimo por ID"""
    try:
        resultado = UsuarioAnonimoController.obtener_usuario_por_id(id_anonimo)
        
        if resultado['success']:
            return jsonify({
                'success': True,
                'usuario': resultado['usuario']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': resultado['error']
            }), 404
            
    except Exception as e:
        ErrorHandler.error_generico('obtener_usuario_anonimo', f'Error: {str(e)}', 'medio', 'routes/usuario_anonimo_routes.py', 'Error en obtener_usuario_anonimo')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@usuario_anonimo_bp.route('/listar', methods=['GET'])
def listar_usuarios_anonimos():
    """API: Listar todos los usuarios anónimos (solo admin)"""
    try:
        # Verificar que el usuario esté autenticado y sea admin
        if 'usuario_id' not in session:
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 401
        
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 50, type=int)
        
        resultado = UsuarioAnonimoController.listar_usuarios_anonimos(pagina, por_pagina)
        
        return jsonify(resultado), 200
            
    except Exception as e:
        ErrorHandler.error_generico('listar_usuarios_anonimos', f'Error: {str(e)}', 'medio', 'routes/usuario_anonimo_routes.py', 'Error en listar_usuarios_anonimos')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@usuario_anonimo_bp.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """API: Obtener estadísticas de usuarios anónimos (solo admin)"""
    try:
        # Verificar que el usuario esté autenticado y sea admin
        if 'usuario_id' not in session:
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 401
        
        resultado = UsuarioAnonimoController.obtener_estadisticas()
        
        return jsonify(resultado), 200
            
    except Exception as e:
        ErrorHandler.error_generico('obtener_estadisticas', f'Error: {str(e)}', 'medio', 'routes/usuario_anonimo_routes.py', 'Error en obtener_estadisticas')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@usuario_anonimo_bp.route('/sesion', methods=['GET'])
def obtener_sesion_anonima():
    """API: Obtener UUID de sesión anónima actual"""
    try:
        uuid_anonimo = session.get('uuid_anonimo')
        id_anonimo = session.get('id_anonimo')
        
        if uuid_anonimo and id_anonimo:
            return jsonify({
                'success': True,
                'tiene_sesion': True,
                'uuid_transaccion': uuid_anonimo,
                'id_anonimo': id_anonimo
            }), 200
        else:
            return jsonify({
                'success': True,
                'tiene_sesion': False,
                'message': 'No hay sesión anónima activa'
            }), 200
            
    except Exception as e:
        ErrorHandler.error_generico('obtener_sesion_anonima', f'Error: {str(e)}', 'medio', 'routes/usuario_anonimo_routes.py', 'Error en obtener_sesion_anonima')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
