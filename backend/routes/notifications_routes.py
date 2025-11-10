"""
RUTAS DE NOTIFICACIONES - Versión Simplificada
===============================================
Este archivo define las URLs (rutas) para las notificaciones.
Cada ruta es como una "dirección web" que hace algo específico.
"""
from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for, flash
from functools import wraps
from controllers.notifications_controller import (
    obtener_todas, obtener_pendientes, contar_pendientes, obtener_vista_previa,
    eliminar, cambiar_estado, marcar_todas_resueltas, eliminar_todas,
    eliminar_resueltas, obtener_datos_para_pagina
)
from utils.error_handler import error_db, error_traduccion, error_auth, error_generico, registrar_error, capturar_error

notifications_bp = Blueprint('notifications_bp', __name__, url_prefix='/notifications')

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

@notifications_bp.route('/all')
@login_required
def get_all_notifications():
    """
    Ruta: /notifications/all
    Obtiene TODAS las notificaciones del sistema.
    """
    try:
        resultado = obtener_todas()
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as error:
        error_generico('get_all_notifications', f'Error en ruta /all: {str(error)}', 'alto', 'routes/notifications_routes.py', 'Error en API Notificaciones')
        return jsonify({'success': False, 'error': 'Error al cargar notificaciones'}), 500

@notifications_bp.route('/unread')
@login_required
def get_unread_notifications():
    """
    Ruta: /notifications/unread
    Obtiene solo las notificaciones que NO están resueltas.
    """
    resultado = obtener_pendientes()
    
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 500

@notifications_bp.route('/count')
@login_required
def get_unread_count():
    """
    Ruta: /notifications/count
    Cuenta cuántas notificaciones están pendientes.
    Este número se muestra en el badge rojo.
    """
    resultado = contar_pendientes()
    return jsonify(resultado)

@notifications_bp.route('/preview')
@login_required
def get_notifications_preview():
    """
    Ruta: /notifications/preview
    Obtiene las últimas 5 notificaciones para mostrar en el menú.
    """
    resultado = obtener_vista_previa(limite=5)
    
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 500

@notifications_bp.route('/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    """
    Ruta: /notifications/delete/123
    Elimina una notificación específica por su ID.
    """
    resultado = eliminar(notification_id)
    
    if resultado['success']:
        flash(resultado['message'], 'success')
    else:
        flash(resultado['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/change-status/<int:notification_id>', methods=['POST'])
@login_required
def change_alert_status(notification_id):
    """
    Ruta: /notifications/change-status/123
    Cambia el estado de una notificación.
    Por ejemplo: 'pendiente' → 'en revisión' → 'resuelto'
    """
    nuevo_estado = request.form.get('estado')
    
    resultado = cambiar_estado(notification_id, nuevo_estado)
    
    if resultado['success']:
        flash(resultado['message'], 'success')
    else:
        flash(resultado['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/mark-all-resolved', methods=['POST'])
@login_required
def mark_all_as_resolved():
    """
    Ruta: /notifications/mark-all-resolved
    Marca TODAS las notificaciones como resueltas de una vez.
    """
    resultado = marcar_todas_resueltas()
    
    if resultado['success']:
        flash(resultado['message'], 'success')
    else:
        flash(resultado['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/delete-all', methods=['POST'])
@login_required
def delete_all_notifications():
    """
    Ruta: /notifications/delete-all
    Elimina TODAS las notificaciones del sistema.
    ⚠️ Cuidado: Esta acción no se puede deshacer.
    """
    resultado = eliminar_todas()
    
    if resultado['success']:
        flash(resultado['message'], 'success')
    else:
        flash(resultado['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/delete-all-resolved', methods=['POST'])
@login_required
def delete_all_resolved():
    """
    Ruta: /notifications/delete-all-resolved
    Elimina solo las notificaciones que ya están resueltas.
    Sirve para limpiar el historial sin perder las pendientes.
    """
    resultado = eliminar_resueltas()
    
    if resultado['success']:
        flash(resultado['message'], 'success')
    else:
        flash(resultado['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/page')
@login_required
def notifications_page():
    """
    Ruta: /notifications/page
    Muestra la página HTML con todas las notificaciones.
    """
    try:
        datos = obtener_datos_para_pagina()
        
        return render_template('notifications.html', 
                             alertas=datos['alertas'], 
                             unread_count=datos['unread_count'])
    except Exception as error:
        error_generico('notifications_page', f'Error al cargar página: {str(error)}', 'alto', 'routes/notifications_routes.py', 'Error en Página Notificaciones')
        flash('Error al cargar notificaciones', 'error')
        return redirect(url_for('admin_bp.dashboard'))

