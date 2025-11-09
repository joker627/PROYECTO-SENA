"""
🔥 RUTAS DE PRUEBA PARA GENERAR ERRORES
Estas rutas permiten probar el sistema de registro automático de errores
"""

from flask import Blueprint, jsonify, flash, redirect, url_for
from utils.error_handler import ErrorHandler
from functools import wraps
from flask import session

test_errors_bp = Blueprint('test_errors_bp', __name__, url_prefix='/test-errors')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

@test_errors_bp.route('/division-cero')
@login_required
def test_division_cero():
    """Generar error de división por cero"""
    try:
        resultado = 10 / 0
    except Exception as e:
        ErrorHandler.error_generico(
            funcion='test_division_cero',
            detalle=f'ERROR DE PRUEBA - División por cero: {str(e)}',
            severidad='medio'
        )
        flash('✅ Error generado y guardado en alertas_sistema', 'success')
        return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/indice-fuera-rango')
@login_required
def test_indice():
    """Generar error de índice fuera de rango"""
    try:
        lista = [1, 2, 3]
        valor = lista[99]
    except Exception as e:
        ErrorHandler.error_generico(
            funcion='test_indice',
            detalle=f'ERROR DE PRUEBA - Índice fuera de rango: {str(e)}',
            severidad='bajo'
        )
        flash('✅ Error generado y guardado en alertas_sistema', 'success')
        return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/clave-no-existe')
@login_required
def test_clave():
    """Generar error de clave no encontrada"""
    try:
        datos = {'nombre': 'Juan'}
        valor = datos['apellido_inexistente']
    except Exception as e:
        ErrorHandler.error_generico(
            funcion='test_clave',
            detalle=f'ERROR DE PRUEBA - Clave no encontrada: {str(e)}',
            severidad='medio'
        )
        flash('✅ Error generado y guardado en alertas_sistema', 'success')
        return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/conversion-tipo')
@login_required
def test_conversion():
    """Generar error de conversión de tipo"""
    try:
        numero = int("esto_no_es_numero")
    except Exception as e:
        ErrorHandler.error_generico(
            funcion='test_conversion',
            detalle=f'ERROR DE PRUEBA - Error de conversión: {str(e)}',
            severidad='bajo'
        )
        flash('✅ Error generado y guardado en alertas_sistema', 'success')
        return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/error-critico')
@login_required
def test_critico():
    """Generar error crítico de archivo"""
    try:
        with open('archivo_que_no_existe_123456.txt', 'r') as f:
            contenido = f.read()
    except Exception as e:
        ErrorHandler.error_generico(
            funcion='test_critico',
            detalle=f'ERROR DE PRUEBA - Archivo no encontrado: {str(e)}',
            severidad='crítico'
        )
        flash('✅ Error CRÍTICO generado y guardado en alertas_sistema', 'warning')
        return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/db-error')
@login_required
def test_db_error():
    """Simular error de base de datos"""
    ErrorHandler.error_db(
        funcion='test_db_error',
        detalle='ERROR DE PRUEBA - Simulación de fallo en conexión a base de datos'
    )
    flash('✅ Error de BD generado y guardado en alertas_sistema', 'success')
    return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/auth-error')
@login_required
def test_auth_error():
    """Simular error de autenticación"""
    ErrorHandler.error_auth(
        funcion='test_auth_error',
        detalle='ERROR DE PRUEBA - Simulación de fallo en autenticación'
    )
    flash('✅ Error de AUTH generado y guardado en alertas_sistema', 'success')
    return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/traduccion-error')
@login_required
def test_traduccion_error():
    """Simular error de traducción"""
    ErrorHandler.error_traduccion(
        funcion='test_traduccion_error',
        detalle='ERROR DE PRUEBA - Simulación de fallo en servicio de traducción'
    )
    flash('✅ Error de TRADUCCIÓN generado y guardado en alertas_sistema', 'success')
    return redirect(url_for('notifications_bp.notifications_page'))

@test_errors_bp.route('/menu')
@login_required
def menu_pruebas():
    """Menú para probar errores fácilmente"""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔥 Prueba de Errores</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 800px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                text-align: center;
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }
            .btn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: block;
                text-align: center;
            }
            .btn:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            .btn-success {
                background: linear-gradient(135deg, #11998e, #38ef7d);
            }
            .btn-danger {
                background: linear-gradient(135deg, #eb3349, #f45c43);
            }
            .btn-warning {
                background: linear-gradient(135deg, #f093fb, #f5576c);
            }
            .info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            .info h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .info ul {
                margin-left: 20px;
                color: #666;
            }
            .info li {
                margin-bottom: 8px;
            }
            .emoji {
                font-size: 1.5em;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Generador de Errores</h1>
            <p class="subtitle">Haz clic en cualquier botón para generar un error y ver cómo se guarda automáticamente</p>
            
            <div class="grid">
                <a href="/test-errors/division-cero" class="btn">
                    <span class="emoji">➗</span>División por Cero
                </a>
                <a href="/test-errors/indice-fuera-rango" class="btn">
                    <span class="emoji">📋</span>Índice Inválido
                </a>
                <a href="/test-errors/clave-no-existe" class="btn">
                    <span class="emoji">🔑</span>Clave No Existe
                </a>
                <a href="/test-errors/conversion-tipo" class="btn">
                    <span class="emoji">🔄</span>Error de Conversión
                </a>
                <a href="/test-errors/error-critico" class="btn btn-danger">
                    <span class="emoji">💥</span>Error CRÍTICO
                </a>
                <a href="/test-errors/db-error" class="btn btn-warning">
                    <span class="emoji">🗄️</span>Error Base Datos
                </a>
                <a href="/test-errors/auth-error" class="btn btn-warning">
                    <span class="emoji">🔐</span>Error Autenticación
                </a>
                <a href="/test-errors/traduccion-error" class="btn btn-warning">
                    <span class="emoji">🌐</span>Error Traducción
                </a>
            </div>
            
            <a href="/notifications/page" class="btn btn-success" style="margin-bottom: 20px;">
                <span class="emoji">👀</span>Ver Notificaciones
            </a>
            
            <div class="info">
                <h3>📊 ¿Cómo funciona?</h3>
                <ul>
                    <li><strong>Haz clic</strong> en cualquier botón de error</li>
                    <li>El sistema <strong>captura el error</strong> automáticamente</li>
                    <li>Se <strong>guarda en alertas_sistema</strong> de tu base de datos</li>
                    <li>Si repites el mismo error, <strong>incrementa el contador</strong> (no duplica)</li>
                    <li>Ve a <strong>Notificaciones</strong> para ver todos los errores registrados</li>
                </ul>
            </div>
            
            <div class="info" style="margin-top: 15px;">
                <h3>🎯 Integración Real</h3>
                <ul>
                    <li>Este sistema ya está integrado en: <strong>Login</strong>, <strong>Dashboard</strong>, <strong>Conexión DB</strong></li>
                    <li>Cualquier error en tu aplicación se guardará automáticamente</li>
                    <li>No necesitas hacer nada, solo usa tu aplicación normal</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return html
