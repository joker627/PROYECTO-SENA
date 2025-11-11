import os
import sys
from datetime import timedelta

# When this module is executed as a script (python e:/PROYECTO-SENA/backend/app.py)
# the top-level package `backend` may not be importable. Ensure the repository
# root is on sys.path so absolute imports like `from backend.routes...` work
# regardless of the current working directory or how Python was invoked.
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

from flask import Flask, session
from backend.routes.general_route import general_bp
from backend.routes.auth_routes import auth_bp
from backend.routes.solicitudes_routes import solicitudes_bp
from backend.routes.reportes_routes import reportes_bp
from backend.routes.roles_routes import roles_bp
from backend.routes.contribuciones_routes import contribuciones_bp
from backend.routes.rendimiento_routes import rendimiento_bp
from backend.routes.traducciones_routes import traducciones_bp
from backend.routes.usuarios_routes import usuarios_bp
from backend.controllers.reportes_controller import list_reportes


app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'clave_super_segura'

# Duración de la sesión
app.permanent_session_lifetime = timedelta(days=30)


@app.before_request
def refresh_session():
    """Mantiene viva la sesión mientras el usuario esté activo."""
    if session.get('usuario') or session.get('user_id'):
        session.permanent = True


# Registro de blueprints
app.register_blueprint(roles_bp)
app.register_blueprint(traducciones_bp)
app.register_blueprint(contribuciones_bp)
app.register_blueprint(rendimiento_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(general_bp)
app.register_blueprint(solicitudes_bp)
app.register_blueprint(usuarios_bp)


@app.context_processor
def inject_global_counts():
    """
    Inyecta `notification_count` y `reportes_count` en el contexto de todas las plantillas.
    Esto permite renderizar badges con Jinja sin tener que pasar las variables manualmente
    en cada render_template.
    """
    # We no longer provide notification counts globally; only report counts and basic stats.
    try:
        reportes_count = len(list_reportes(limit=1000) or [])
    except Exception:
        reportes_count = 0


    class _PaginationDefault:
        page = 1
        per_page = 0
        total = 0
        pages = 1
        has_prev = False
        has_next = False
        prev_num = None
        next_num = None

        def iter_pages(self, *args, **kwargs):
            return []

        @property
        def total_pages(self):

            return self.pages

    stats = {
        'total': 0,
        'activos': 0,
        'administradores': 0,
        'gestores': 0,
        'pendientes': 0,
        'en_revision': 0,
        'resueltos': 0,
    }


    return dict(
        reportes_count=reportes_count,
        pagination=_PaginationDefault(),
        stats=stats,
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
