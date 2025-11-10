# keep flask imports
from flask import Flask, session
from datetime import timedelta
from routes.login_routes import login_bp
from routes.admin_routes import admin_bp
from routes.general_route import general_bp
from routes.notifications_routes import notifications_bp
from routes.solicitudes_routes import solicitudes_bp
from routes.reportes_routes import reportes_bp
from routes.usuarios_routes import usuarios_bp
from routes.usuario_anonimo_routes import usuario_anonimo_bp
from controllers.notifications_controller import contar_pendientes
from controllers.reportes_controller import get_pending_count
from utils.error_handler import error_generico

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'clave_super_segura'


app.permanent_session_lifetime = timedelta(days=30)

app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(general_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(solicitudes_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(usuario_anonimo_bp)


@app.before_request
def refresh_session():
    if session.get('usuario') or session.get('user_id'):
        session.permanent = True


@app.context_processor
def inject_global_counts():
    """
    Inyecta `notification_count` y `reportes_count` en el contexto de todas las plantillas.
    Esto permite renderizar badges con Jinja sin tener que pasar las variables manualmente
    en cada render_template.
    """
    notif_count = 0
    reportes_count = 0
    try:
        resultado = contar_pendientes()
        if isinstance(resultado, dict):
            notif_count = int(resultado.get('count', 0) or 0)
    except Exception:
        notif_count = 0

    try:
        reportes_count = int(get_pending_count() or 0)
    except Exception:
        reportes_count = 0

    return dict(notification_count=notif_count, reportes_count=reportes_count)



@app.errorhandler(Exception)
def handle_unhandled_exception(error):
    try:
        error_generico(
            funcion='unhandled_exception',
            detalle=f'Unhandled exception: {str(error)}',
            severidad='critico',
            archivo='app.py',
            tipo_especifico='UnhandledException'
        )
    except Exception:
        pass


    return ("Internal Server Error", 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
