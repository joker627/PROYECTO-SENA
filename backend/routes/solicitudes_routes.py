from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from controllers.solicitudes_controller import SolicitudesController
from utils.error_handler import ErrorHandler


solicitudes_bp = Blueprint('solicitudes_bp', __name__, url_prefix='/solicitudes')


@solicitudes_bp.route('/')
def solicitudes_page():
    # Verificar sesión activa
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder', 'error')
        return redirect(url_for('login_bp.login'))
    
    # Parámetros: página, items por página, filtro estado, orden
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    estado_filter = request.args.get('estado', None)
    orden = request.args.get('orden', 'reciente')
    
    data = SolicitudesController.get_page_data(page, per_page, estado_filter, orden)
    
    return render_template(
        'admin/solicitudes.html',
        solicitudes=data['solicitudes'],
        pending_count=data['pending_count'],
        pagination=data['pagination'],
        estado_filter=estado_filter,
        orden=orden
    )


@solicitudes_bp.route('/aceptar/<int:id_solicitud>', methods=['POST'])
def accept_solicitud(id_solicitud):
    # Aceptar solicitud y crear usuario GESTOR
    if 'user_id' not in session:
        return redirect(url_for('login_bp.login'))
    
    id_revisor = session.get('user_id')
    
    if SolicitudesController.accept_solicitud(id_solicitud, id_revisor):
        flash('✅ Solicitud aceptada. Se ha creado una cuenta de usuario con rol GESTOR automáticamente.', 'success')
    else:
        flash('Error al aceptar la solicitud', 'error')
    
    return redirect(url_for('solicitudes_bp.solicitudes_page'))


@solicitudes_bp.route('/rechazar/<int:id_solicitud>', methods=['POST'])
def reject_solicitud(id_solicitud):
    # Rechazar solicitud con motivo obligatorio
    if 'user_id' not in session:
        return redirect(url_for('login_bp.login'))
    
    id_revisor = session.get('user_id')
    motivo_rechazo = request.form.get('motivo_rechazo', '').strip()
    
    if not motivo_rechazo:
        flash('Debes proporcionar un motivo de rechazo', 'error')
        return redirect(url_for('solicitudes_bp.solicitudes_page'))
    
    if SolicitudesController.reject_solicitud(id_solicitud, id_revisor, motivo_rechazo):
        flash(f'Solicitud rechazada. Motivo: {motivo_rechazo}', 'info')
    else:
        flash('Error al rechazar la solicitud', 'error')
    
    return redirect(url_for('solicitudes_bp.solicitudes_page'))


@solicitudes_bp.route('/eliminar/<int:id_solicitud>', methods=['POST'])
def delete_solicitud(id_solicitud):
    # Eliminar solicitud manualmente
    if 'user_id' not in session:
        return redirect(url_for('login_bp.login'))
    
    if SolicitudesController.delete_solicitud(id_solicitud):
        flash('Solicitud eliminada correctamente', 'success')
    else:
        flash('Error al eliminar la solicitud', 'error')
    
    return redirect(url_for('solicitudes_bp.solicitudes_page'))


@solicitudes_bp.route('/api/count')
def get_count():
    # API: Contador de solicitudes pendientes
    try:
        count = SolicitudesController.get_pending_count()
        return jsonify({
            'success': True,
            'count': count
        })
    except Exception as e:
        ErrorHandler.error_generico('get_count', f'Error al contar solicitudes: {str(e)}', 'bajo', 'routes/solicitudes_routes.py', 'Error API Count Solicitudes')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
