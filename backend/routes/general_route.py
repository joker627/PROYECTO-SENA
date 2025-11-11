
from flask import Blueprint, render_template, request, flash, jsonify
from datetime import datetime
from backend.controllers.reportes_controller import list_reportes
from backend.controllers.contribuciones_controller import list_contribuciones
from backend.controllers.solicitudes_controller import list_solicitudes
from backend.models.estadisticas_models import get_latest_estadisticas
from backend.models.usuarios_models import list_users

general_bp = Blueprint('general_bp', __name__)


@general_bp.route('/')
def index():
    return render_template('pages/index.html')


@general_bp.route('/nosotros')
def nosotros():
    return render_template('pages/nosotros.html')


@general_bp.route('/tutoriales')
def tutoriales():
    return render_template('pages/tutoriales.html')


@general_bp.route('/notifications')
def notifications():
    # Notifications page removed; redirect to index and show a flash if needed
    from flask import redirect, url_for
    return redirect(url_for('general_bp.index'))


@general_bp.route('/notifications/page')
def notifications_page():
    # Page removed; redirect to dashboard
    from flask import redirect, url_for
    return redirect(url_for('general_bp.admin_dashboard'))


@general_bp.route('/notifications/<int:notification_id>')
def notifications_detail(notification_id):
    # Detail view removed; redirect to dashboard
    from flask import redirect, url_for
    return redirect(url_for('general_bp.admin_dashboard'))


@general_bp.route('/inicio')
def inicio():
    """Alias for index() kept for backward compatibility with templates
    or code that used the older endpoint name `general_bp.inicio`.
    """
    return index()


# Admin views (static templates already present under frontend/templates/admin)
@general_bp.route('/admin/dashboard')
def admin_dashboard():
    # Try to load real metrics from the `estadisticas` table and fall back
    # to zeros if not available.
    stats_row = None
    try:
        stats_row = get_latest_estadisticas()
    except Exception:
        stats_row = None

    # Only expose metrics that come from the `estadisticas` table.
    metrics = {
        'traducciones': {
            'total': 0,
            'texto_a_senas': 0,
            'senas_a_texto': 0,
        },
        'precision': {'average': 0, 'updated_at': None},
        'reportes': {'total': 0},
        'contribuciones': {'pendientes': 0, 'aprobadas': 0},
        'senas_validadas': 0,
    }

    if stats_row:
        metrics['traducciones']['total'] = int(stats_row.get('total_traducciones') or 0)
        metrics['traducciones']['texto_a_senas'] = int(stats_row.get('traducciones_texto_a_senas') or 0)
        metrics['traducciones']['senas_a_texto'] = int(stats_row.get('traducciones_senas_a_texto') or 0)
        metrics['precision']['average'] = float(stats_row.get('precision_modelo') or 0.0)
        metrics['precision']['updated_at'] = stats_row.get('fecha_actualizacion')
        metrics['reportes']['total'] = int(stats_row.get('errores_reportados') or 0)
        metrics['contribuciones']['pendientes'] = int(stats_row.get('contribuciones_pendientes') or 0)
        metrics['contribuciones']['aprobadas'] = int(stats_row.get('contribuciones_aprobadas') or 0)
        metrics['senas_validadas'] = int(stats_row.get('senas_validadas') or 0)

    # Backward-compatible aliases used by some templates
    metrics['reports'] = metrics.get('reportes', metrics.get('reports', {'total': metrics.get('reportes', {}).get('total', 0)}))
    metrics['translations'] = metrics.get('traducciones', metrics.get('translations', {}))
    activities = []
    chart_data = []
    # Load recent contribuciones to display as 'projects' in the dashboard
    try:
        contribs = list_contribuciones(limit=6, offset=0) or []
    except Exception:
        contribs = []

    projects = []
    for c in contribs:
        projects.append({
            'titulo': (c.get('descripcion') or '')[:80] or 'Contribución',
            'descripcion': c.get('descripcion') or '',
            'fecha': str(c.get('fecha_envio')) if c.get('fecha_envio') else '',
            'colaborador': c.get('id_usuario') or 'Anon',
            'estado': c.get('estado') or 'pendiente',
            'estado_class': 'completed' if c.get('estado') == 'aprobada' else 'pending'
        })
    return render_template('admin/dashboard.html', metrics=metrics, activities=activities, chart_data=chart_data, projects=projects)


@general_bp.route('/admin/reportes')
def admin_reportes():
    # Read optional filters and pagination from query params
    estado = request.args.get('estado')
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    try:
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        per_page = 10

    offset = (page - 1) * per_page

    # Fetch reportes via controller which now returns {'reportes': [...], 'total': N}
    try:
        result = list_reportes(limit=per_page, offset=offset) or {'reportes': [], 'total': 0}
    except Exception:
        result = {'reportes': [], 'total': 0}

    reportes_raw = result.get('reportes', [])
    total = int(result.get('total', 0))

    # Map DB rows to the template-friendly shape and compute time ago string
    reportes = []
    now = datetime.utcnow()
    for r in reportes_raw:
        fecha = r.get('fecha_reporte')
        if isinstance(fecha, str):
            try:
                fecha_dt = datetime.fromisoformat(fecha)
            except Exception:
                fecha_dt = None
        else:
            fecha_dt = fecha

        # simple human-friendly elapsed time
        if fecha_dt:
            delta = now - fecha_dt
            days = delta.days
            hours = delta.seconds // 3600
            if days > 0:
                tiempo = f"{days}d"
            elif hours > 0:
                tiempo = f"{hours}h"
            else:
                minutos = max(1, delta.seconds // 60)
                tiempo = f"{minutos}m"
        else:
            tiempo = ''

        reportes.append({
            'id_reporte': r.get('id_reporte'),
            'estado': r.get('estado'),
            'uuid_transaccion': r.get('uuid_transaccion'),
            'tipo_error': r.get('tipo_traduccion') or r.get('tipo_traduccion') or r.get('tipo_traduccion'),
            'tiempo_transcurrido': tiempo,
            'id_traduccion': r.get('id_traduccion'),
            'origen': r.get('origen'),
            'descripcion': r.get('descripcion_error'),
            'evidencia_url': r.get('evidencia_url'),
            'fecha_resolucion': r.get('fecha_resolucion'),
            'nombre_responsable': r.get('nombre_responsable'),
        })

    # Build a minimal pagination object expected by the template
    class _P:
        def __init__(self, current_page, per_page, total):
            self.current_page = current_page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page if per_page else 1

        @property
        def total_pages(self):
            return self.pages

    pagination = _P(page, per_page, total)

    return render_template('admin/reportes.html', reportes=reportes, current_filter=estado, pagination=pagination)


@general_bp.route('/admin/solicitudes')
def admin_solicitudes():
    return render_template('admin/solicitudes.html')


@general_bp.route('/admin/usuarios')
def admin_usuarios():
    # Load users to show in the admin users page
    usuarios = list_users(limit=1000)
    if usuarios is None:
        # DB error occurred when fetching users
        flash('No se pudo conectar a la base de datos de usuarios. Revisa la configuración y el servicio.', 'danger')
        usuarios = []

    # Compute simple stats expected by the template
    stats = {
        'total': 0,
        'activos': 0,
        'administradores': 0,
        'gestores': 0,
        'pendientes': 0,
        'en_revision': 0,
        'resueltos': 0,
    }

    stats['total'] = len(usuarios)
    for u in usuarios:
        est = (u.get('estado') or '').upper()
        if est == 'ACTIVO':
            stats['activos'] += 1
        if u.get('id_rol') and int(u.get('id_rol')) == 1:
            stats['administradores'] += 1
        else:
            stats['gestores'] += 1

    return render_template('admin/usuarios.html', usuarios=usuarios, stats=stats)



@general_bp.route('/admin/api/dashboard-data')
def api_dashboard_data():
    """Return JSON with minimal dashboard data for the frontend updater.

    This is a compatibility endpoint used by `refreshDashboard()` in the
    frontend. It returns a `data` object with keys: metrics, activity,
    chart, projects. Values are best-effort and fall back to safe defaults.
    """
    try:
        stats_row = get_latest_estadisticas() or {}
    except Exception:
        stats_row = {}

    # basic metrics mapping
    metrics = {
        'users': {'total': 0, 'growth': 0, 'trend': 'neutral'},
        'translations': {'total': 0, 'growth': 0, 'trend': 'neutral'},
        'precision': {'average': 0.0, 'status': 'neutral'},
        'projects': {'total': 0, 'growth': 0, 'trend': 'neutral'},
        'anonymous': {'total': 0},
        'reports': {'total': 0, 'change': 0, 'trend': 'neutral'},
        'solicitudes': {'total': 0},
        'colaboradores': {'total': 0},
    }

    try:
        metrics['translations']['total'] = int(stats_row.get('total_traducciones') or 0)
        metrics['precision']['average'] = float(stats_row.get('precision_modelo') or 0.0)
        metrics['reports']['total'] = int(stats_row.get('errores_reportados') or 0)
        metrics['projects']['total'] = int(stats_row.get('contribuciones_aprobadas') or 0)
        metrics['projects']['growth'] = int(stats_row.get('contribuciones_pendientes') or 0)
    except Exception:
        pass

    # recent activity: use recent contribuciones as simple activity feed
    try:
        contribs = list_contribuciones(limit=6) or []
    except Exception:
        contribs = []

    activity = []
    for c in contribs:
        activity.append({
            'icon': 'fa-file-alt',
            'descripcion': (c.get('descripcion') or '')[:140],
            'time_ago': str(c.get('fecha_envio') or '')
        })

    # chart data: create simple placeholders from contribs
    chart = []
    for i in range(7):
        chart.append({'label': f'D{i+1}', 'value': 0, 'height': 10})

    # projects: map recent contribuciones to project shape
    projects = []
    for c in contribs:
        projects.append({
            'titulo': (c.get('descripcion') or '')[:60] or 'Contribución',
            'descripcion': c.get('descripcion') or '',
            'fecha': str(c.get('fecha_envio') or ''),
            'colaborador': c.get('id_usuario') or 'Anon',
            'estado': c.get('estado') or 'pendiente',
            'estado_class': 'completed' if c.get('estado') == 'aprobada' else 'pending'
        })

    # solicitudes count
    try:
        sol = list_solicitudes(limit=100) or []
        metrics['solicitudes']['total'] = len(sol)
    except Exception:
        metrics['solicitudes']['total'] = 0

    data = {
        'metrics': metrics,
        'activity': activity,
        'chart': chart,
        'projects': projects,
    }

    return jsonify({'success': True, 'data': data})
