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


@app.context_processor
def inject_notification_count():
    """Inyectar el conteo de notificaciones y reportes en todas las plantillas"""
    if session.get('user_id'):
        try:
            from models.notification_models import NotificationModel
            from models.reportes_models import ReportesModels
            
            notification_count = NotificationModel.count_unresolved_alerts()
            reportes_count = ReportesModels.count_reportes_pendientes()
            
            return {
                'notification_count': notification_count,
                'reportes_count': reportes_count
            }
        except Exception as e:
            print(f"[ERROR] Error al obtener conteos: {str(e)}")
            return {'notification_count': 0, 'reportes_count': 0}
    return {'notification_count': 0, 'reportes_count': 0}


@app.before_request
def refresh_session():
    if session.get('usuario') or session.get('user_id'):
        session.permanent = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
