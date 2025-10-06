from flask import Flask
from routes.auth.auth import auth_bp
from routes.routes import main_bp
from routes.profile_routes import profile_bp
from controllers.auth_controller import AuthController

def create_app():
    app = Flask(__name__, 
        static_folder="../frontend/static", 
        template_folder="../frontend/templates")
    
    app.secret_key = 'manuel'
    
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
    app.run(debug=True, host='0.0.0.0')
