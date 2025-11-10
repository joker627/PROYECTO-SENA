"""
Controlador para el Dashboard - Lógica de negocio
"""

from models.dashboard_models import (
    get_total_users as model_get_total_users,
    get_users_growth as model_get_users_growth,
    get_total_contributions as model_get_total_contributions,
    get_contributions_growth as model_get_contributions_growth,
    get_pending_reports as model_get_pending_reports,
    get_reports_growth as model_get_reports_growth,
    get_system_alerts as model_get_system_alerts,
    get_pending_solicitudes as model_get_pending_solicitudes,
    get_total_translations as model_get_total_translations,
    get_translations_growth as model_get_translations_growth,
    get_total_anonymous_users as model_get_total_anonymous_users,
    get_average_precision as model_get_average_precision,
    get_colaboradores_count as model_get_colaboradores_count,
    get_recent_activity as model_get_recent_activity,
    calculate_time_ago as model_calculate_time_ago,
    get_weekly_stats as model_get_weekly_stats,
    get_recent_projects as model_get_recent_projects
)
from utils.error_handler import error_generico
from utils.error_handler import capturar_error


@capturar_error(modulo='dashboard', severidad='alto')
def get_dashboard_metrics():
    """Obtener todas las métricas principales del dashboard"""
    try:
        # Métricas de usuarios
        total_users = model_get_total_users()
        users_growth = model_get_users_growth()

        # Métricas de contribuciones (proyectos)
        total_contributions = model_get_total_contributions()
        contributions_growth = model_get_contributions_growth()

        # Métricas de reportes
        pending_reports = model_get_pending_reports()
        reports_change = model_get_reports_growth()

        # Métricas de alertas del sistema
        system_alerts = model_get_system_alerts()

        # Métricas de solicitudes pendientes
        pending_solicitudes = model_get_pending_solicitudes()

        # Métricas de traducciones
        total_translations = model_get_total_translations()
        translations_growth = model_get_translations_growth()

        # Métricas de usuarios anónimos
        total_anonymous = model_get_total_anonymous_users()

        # Métricas de precisión del modelo
        average_precision = model_get_average_precision()

        # Métricas de colaboradores
        total_colaboradores = model_get_colaboradores_count()
    except Exception as e:
        error_generico('get_dashboard_metrics', f'Error al obtener métricas: {str(e)}', 'alto', 'controllers/dashboard_controller.py', 'Error en Dashboard')
        # Retornar valores por defecto en caso de error
        return {
            'users': {'total': 0, 'growth': 0, 'trend': 'neutral'},
            'projects': {'total': 0, 'growth': 0, 'trend': 'neutral'},
            'reports': {'total': 0, 'change': 0, 'trend': 'neutral'},
            'alerts': {'total': 0, 'status': 'error'},
            'solicitudes': {'total': 0, 'status': 'neutral'},
            'translations': {'total': 0, 'growth': 0, 'trend': 'neutral'},
            'anonymous': {'total': 0},
            'precision': {'average': 0},
            'colaboradores': {'total': 0}
        }
        
    return {
        'users': {
            'total': total_users,
            'growth': users_growth,
            'trend': 'positive' if users_growth >= 0 else 'negative'
        },
        'projects': {
            'total': total_contributions,
            'growth': contributions_growth,
            'trend': 'positive' if contributions_growth >= 0 else 'negative'
        },
        'reports': {
            'total': pending_reports,
            'change': reports_change,
            'trend': 'negative' if reports_change > 0 else 'positive'  # Más reportes es negativo
        },
        'alerts': {
            'total': system_alerts,
            'status': 'critical' if system_alerts > 5 else 'warning' if system_alerts > 0 else 'good'
        },
        'solicitudes': {
            'total': pending_solicitudes,
            'status': 'pending' if pending_solicitudes > 0 else 'completed'
        },
        'translations': {
            'total': total_translations,
            'growth': translations_growth,
            'trend': 'positive' if translations_growth >= 0 else 'negative'
        },
        'anonymous': {
            'total': total_anonymous,
            'status': 'active'
        },
        'precision': {
            'average': average_precision,
            'status': 'excellent' if average_precision >= 90 else 'good' if average_precision >= 75 else 'warning'
        },
        'colaboradores': {
            'total': total_colaboradores,
            'status': 'active'
        }
    }
    
@capturar_error(modulo='dashboard', severidad='medio')
def get_recent_activity(limit=5):
    """Obtener actividad reciente del sistema formateada"""
    activities = model_get_recent_activity(limit)
    
    # Formatear tiempos
    for activity in activities:
        activity['time_ago'] = model_calculate_time_ago(activity['fecha'])
    
    return activities


@capturar_error(modulo='dashboard', severidad='medio')
def get_weekly_chart_data():
    """Obtener datos para el gráfico semanal"""
    stats = model_get_weekly_stats()
    
    # Calcular altura porcentual para las barras
    max_value = max(stats['values']) if stats['values'] else 1
    if max_value == 0:
        max_value = 1
    
    chart_data = []
    for i, label in enumerate(stats['labels']):
        value = stats['values'][i] if i < len(stats['values']) else 0
        height = (value / max_value) * 100 if max_value > 0 else 0
        chart_data.append({
            'label': label,
            'value': value,
            'height': max(height, 5)  # Mínimo 5% para que sea visible
        })
    
    return chart_data


@capturar_error(modulo='dashboard', severidad='medio')
def get_recent_projects():
    """Obtener proyectos recientes"""
    return model_get_recent_projects()


@capturar_error(modulo='dashboard', severidad='medio')
def get_dashboard_data():
    """Obtener todos los datos necesarios para el dashboard"""
    return {
        'metrics': get_dashboard_metrics(),
        'activity': get_recent_activity(5),
        'chart': get_weekly_chart_data(),
        'projects': get_recent_projects()
    }
