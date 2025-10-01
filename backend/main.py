from flask import Flask, session
from routes.auth.auth import auth_bp
from routes.routes import main_bp
from error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__, 
        static_folder="../frontend/static", 
        template_folder="../frontend/templates")
    
    # Clave secreta para sesiones
    app.secret_key = 'tu_clave_secreta_super_segura_2025'
    
    # Context processor para hacer 'user' disponible en todos los templates
    @app.context_processor
    def inject_user():
        return dict(user=session.get('user'))
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
