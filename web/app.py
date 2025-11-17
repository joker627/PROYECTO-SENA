import os
import sys
from flask import Flask
from datetime import timedelta

# Ajustar path para shared
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from web.middleware.anonimo_web import anonimo_middleware
from web.routes.web_routes import web_bp
from web.routes.LoginRoutesWeb import web_login
from web.routes.AdminRoutesWeb import web_admin

def create_web_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    
    app.secret_key = "clave_secreta_web"
    app.permanent_session_lifetime = timedelta(days=30)

    # SOLO rutas WEB
    app.register_blueprint(web_bp)
    app.register_blueprint(web_login)
    app.register_blueprint(web_admin)

    # Middleware para web
    anonimo_middleware(app)

    return app

if __name__ == "__main__":
    app = create_web_app()
    app.run(debug=True, host="0.0.0.0", port=5000)