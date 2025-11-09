from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from controllers.reportes_controller import ReportesController
from controllers.notifications_controller import NotificationController
from utils.error_handler import ErrorHandler
from functools import wraps

reportes_bp = Blueprint('reportes_bp', __name__, url_prefix='/reportes')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('login_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@reportes_bp.route('/')
@login_required
def reportes_page():
    """Página principal de gestión de reportes"""
    try:
        # Obtener datos de reportes
        data = ReportesController.get_page_data()
        
        return render_template(
            'admin/reportes.html',
            reportes=data['reportes'],
            stats=data['stats']
        )
    except Exception as e:
        print(f"Error en reportes_page: {e}")
        ErrorHandler.error_generico('reportes_page', f'Error al cargar reportes: {str(e)}', 'alto', 'routes/reportes_routes.py', 'Error Página Reportes')
        flash('Error al cargar los reportes', 'error')
        return redirect(url_for('admin_bp.dashboard'))

@reportes_bp.route('/revision/<int:id_reporte>', methods=['POST'])
@login_required
def marcar_revision(id_reporte):
    """Marca un reporte como 'en revisión'"""
    try:
        success = ReportesController.mark_as_revision(id_reporte)
        if success:
            flash('Reporte marcado como "en revisión"', 'success')
        else:
            flash('Error al actualizar el reporte', 'error')
    except Exception as e:
        print(f"Error al marcar como revisión: {e}")
        ErrorHandler.error_generico('marcar_revision', f'Error: {str(e)}', 'medio', 'routes/reportes_routes.py', 'Error Cambiar Estado Reporte')
        flash('Error al procesar la solicitud', 'error')
    
    return redirect(url_for('reportes_bp.reportes_page'))

@reportes_bp.route('/resolver/<int:id_reporte>', methods=['POST'])
@login_required
def resolver_reporte(id_reporte):
    """Marca un reporte como resuelto"""
    try:
        success = ReportesController.mark_as_resolved(id_reporte)
        if success:
            flash('Reporte marcado como resuelto', 'success')
        else:
            flash('Error al actualizar el reporte', 'error')
    except Exception as e:
        print(f"Error al resolver reporte: {e}")
        ErrorHandler.error_generico('resolver_reporte', f'Error: {str(e)}', 'medio', 'routes/reportes_routes.py', 'Error Resolver Reporte')
        flash('Error al procesar la solicitud', 'error')
    
    return redirect(url_for('reportes_bp.reportes_page'))

@reportes_bp.route('/eliminar/<int:id_reporte>', methods=['POST'])
@login_required
def eliminar_reporte(id_reporte):
    """Elimina un reporte"""
    try:
        success = ReportesController.delete_reporte(id_reporte)
        if success:
            flash('Reporte eliminado correctamente', 'success')
        else:
            flash('Error al eliminar el reporte', 'error')
    except Exception as e:
        print(f"Error al eliminar reporte: {e}")
        ErrorHandler.error_generico('eliminar_reporte', f'Error: {str(e)}', 'medio', 'routes/reportes_routes.py', 'Error Eliminar Reporte')
        flash('Error al procesar la solicitud', 'error')
    
    return redirect(url_for('reportes_bp.reportes_page'))

@reportes_bp.route('/eliminar-resueltos', methods=['POST'])
@login_required
def eliminar_resueltos():
    """Elimina todos los reportes resueltos"""
    try:
        count = ReportesController.delete_all_resolved()
        if count > 0:
            flash(f'Se eliminaron {count} reporte{"s" if count != 1 else ""} resuelto{"s" if count != 1 else ""}', 'success')
        else:
            flash('No hay reportes resueltos para eliminar', 'warning')
    except Exception as e:
        print(f"Error al eliminar reportes resueltos: {e}")
        ErrorHandler.error_generico('eliminar_resueltos', f'Error: {str(e)}', 'medio', 'routes/reportes_routes.py', 'Error Eliminar Resueltos')
        flash('Error al procesar la solicitud', 'error')
    
    return redirect(url_for('reportes_bp.reportes_page'))

@reportes_bp.route('/api/count')
def get_count():
    """API para obtener el conteo de reportes pendientes"""
    try:
        count = ReportesController.get_pending_count()
        return jsonify({'count': count})
    except Exception as e:
        print(f"Error en get_count: {e}")
        ErrorHandler.error_generico('get_count', f'Error al contar reportes: {str(e)}', 'bajo', 'routes/reportes_routes.py', 'Error API Count Reportes')
        return jsonify({'count': 0}), 500
