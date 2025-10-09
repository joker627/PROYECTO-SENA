from flask import Flask, session, request
from routes.auth.auth import auth_bp
from routes.routes import main_bp
from routes.profile_routes import profile_bp
from controllers.auth_controller import AuthController
from models.user_model import create_anonymous_session, validate_anonymous_session

def create_app():
    app = Flask(__name__, 
        static_folder="../frontend/static", 
        template_folder="../frontend/templates")
    
    app.secret_key = 'manuel'
    
    # Middleware para manejar sesiones anónimas
    @app.before_request
    def handle_anonymous_session():
        # Solo aplicar en rutas que no sean de archivos estáticos
        if request.endpoint and not request.endpoint.startswith('static'):
            # Si el usuario no está logueado
            if not AuthController.get_current_user():
                # Verificar si ya tiene una sesión anónima
                anonymous_session_id = session.get('anonymous_session_id')
                
                if anonymous_session_id:
                    # Validar que la sesión anónima existe y está activa
                    if not validate_anonymous_session(anonymous_session_id):
                        # Si no es válida, crear una nueva
                        anonymous_session_id = create_anonymous_session()
                        session['anonymous_session_id'] = anonymous_session_id
                else:
                    # Si no tiene sesión anónima, crear una
                    anonymous_session_id = create_anonymous_session()
                    if anonymous_session_id:
                        session['anonymous_session_id'] = anonymous_session_id
    
    # Context processor global
    @app.context_processor
    def inject_user():
        return dict(user=AuthController.get_current_user())
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    
    
    return app

app = create_app()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
