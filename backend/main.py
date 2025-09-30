from flask import Flask
from routes.auth.auth import auth_bp
from routes.routes import main_bp

def create_app():
    app = Flask(__name__, 
        static_folder="../frontend/static", 
        template_folder="../frontend/templates")
    
    # Clave secreta para sesiones
    app.secret_key = 'tu_clave_secreta_super_segura_2025'
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
