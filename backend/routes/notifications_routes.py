"""
Rutas para el manejo de notificaciones del sistema
"""
from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for, flash
from functools import wraps
from controllers.notifications_controller import NotificationController
from utils.error_handler import ErrorHandler

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
    """Endpoint: Obtener todas las alertas del sistema"""
    try:
        result = NotificationController.get_all_notifications()
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
    except Exception as e:
        ErrorHandler.error_generico('get_all_notifications', f'Error en ruta /all: {str(e)}', 'alto', 'routes/notifications_routes.py', 'Error en API Notificaciones')
        return jsonify({'success': False, 'error': 'Error al cargar notificaciones'}), 500

@notifications_bp.route('/unread')
@login_required
def get_unread_notifications():
    """Endpoint: Obtener solo alertas NO resueltas"""
    result = NotificationController.get_unread_notifications(limit=10)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@notifications_bp.route('/count')
@login_required
def get_unread_count():
    """Endpoint: Obtener el conteo de alertas pendientes"""
    result = NotificationController.get_unread_count()
    return jsonify(result)

@notifications_bp.route('/preview')
@login_required
def get_notifications_preview():
    """Endpoint: Obtener vista previa de alertas para navbar/dashboard"""
    result = NotificationController.get_notifications_preview(limit=5)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@notifications_bp.route('/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    """Endpoint: Eliminar una alerta"""
    result = NotificationController.delete_notification(notification_id)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/change-status/<int:notification_id>', methods=['POST'])
@login_required
def change_alert_status(notification_id):
    """Endpoint: Cambiar el estado de una alerta"""
    new_status = request.form.get('estado')
    
    result = NotificationController.change_notification_status(notification_id, new_status)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/mark-all-resolved', methods=['POST'])
@login_required
def mark_all_as_resolved():
    """Endpoint: Marcar todas las alertas pendientes como resueltas"""
    result = NotificationController.mark_all_as_resolved()
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/delete-all', methods=['POST'])
@login_required
def delete_all_notifications():
    """Endpoint: Eliminar todas las alertas del sistema"""
    result = NotificationController.delete_all_notifications()
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/delete-all-resolved', methods=['POST'])
@login_required
def delete_all_resolved():
    """Endpoint: Eliminar todas las alertas resueltas"""
    result = NotificationController.delete_all_resolved()
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('notifications_bp.notifications_page'))

@notifications_bp.route('/page')
@login_required
def notifications_page():
    """Página: Ver todas las notificaciones"""
    try:
        data = NotificationController.get_page_data()
        
        return render_template('notifications.html', 
                             alertas=data['alertas'], 
                             unread_count=data['unread_count'])
    except Exception as e:
        ErrorHandler.error_generico('notifications_page', f'Error al cargar página: {str(e)}', 'alto', 'routes/notifications_routes.py', 'Error en Página Notificaciones')
        flash('Error al cargar notificaciones', 'error')
        return redirect(url_for('admin_bp.dashboard'))

