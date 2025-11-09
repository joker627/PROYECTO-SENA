"""
Rutas del panel de administración
"""

from flask import Blueprint, render_template, jsonify, send_file
from controllers.dashboard_controller import DashboardController
from utils.error_handler import ErrorHandler
from utils.pdf_generator import PDFGenerator
from datetime import datetime


admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin')
def dashboard():
    """Ruta: Panel de control del administrador"""
    try:
        # Obtener todos los datos del dashboard
        dashboard_data = DashboardController.get_dashboard_data()
        
        return render_template(
            'admin/dashboard.html',
            metrics=dashboard_data['metrics'],
            activities=dashboard_data['activity'],
            chart_data=dashboard_data['chart'],
            projects=dashboard_data['projects']
        )
    except Exception as e:
        ErrorHandler.error_generico('dashboard', f'Error al cargar dashboard: {str(e)}', 'crítico', 'routes/admin_routes.py', 'Error Dashboard Admin')
        return render_template('admin/dashboard.html', 
                             metrics={}, 
                             activities=[], 
                             chart_data=[], 
                             projects=[])


@admin_bp.route('/admin/api/dashboard-data')
def get_dashboard_data():
    """API: Obtener datos del dashboard en formato JSON para actualización AJAX"""
    try:
        dashboard_data = DashboardController.get_dashboard_data()
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
    except Exception as e:
        ErrorHandler.error_generico('get_dashboard_data', f'Error en API dashboard: {str(e)}', 'alto', 'routes/admin_routes.py', 'Error API Dashboard')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/admin/toast-test')
def toast_test():
    """Ruta: Página de prueba del sistema de toasts"""
    return render_template('admin/toast_test.html')


@admin_bp.route('/admin/descargar-metricas-pdf')
def descargar_metricas_pdf():
    """Ruta: Descargar reporte de métricas en formato PDF"""
    try:
        # Obtener datos del dashboard
        dashboard_data = DashboardController.get_dashboard_data()
        
        # Preparar datos para el PDF
        metricas_data = {
            'total_users': dashboard_data['metrics'].get('total_users', 0),
            'users_growth': dashboard_data['metrics'].get('users_growth', 0),
            'total_translations': dashboard_data['metrics'].get('total_translations', 0),
            'translations_growth': dashboard_data['metrics'].get('translations_growth', 0),
            'pending_reports': dashboard_data['metrics'].get('pending_reports', 0),
            'reports_growth': dashboard_data['metrics'].get('reports_growth', 0),
            'total_anonymous_users': dashboard_data['metrics'].get('total_anonymous_users', 0),
            'system_alerts': dashboard_data['metrics'].get('system_alerts', 0),
            'pending_solicitudes': dashboard_data['metrics'].get('pending_solicitudes', 0),
            'average_precision': dashboard_data['metrics'].get('average_precision', 0),
            'colaboradores_count': dashboard_data['metrics'].get('colaboradores_count', 0),
        }
        
        # Generar PDF
        pdf_buffer = PDFGenerator.generar_reporte_metricas(metricas_data)
        
        # Nombre del archivo con fecha
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metricas_dashboard_{fecha_actual}.pdf"
        
        # Enviar PDF como descarga
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        ErrorHandler.error_generico('descargar_metricas_pdf', f'Error al generar PDF: {str(e)}', 'alto', 'routes/admin_routes.py', 'Error Generar PDF Métricas')
        return jsonify({
            'success': False,
            'error': 'Error al generar el reporte PDF'
        }), 500
