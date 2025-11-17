import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Ajustar path para shared
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from api.routes.AuthRoutesAPI import auth_bp
from api.routes.UsuarioRoutesAPI import usuario_bp
from api.routes.EstadisticasRoutesAPI import estadisticas_bp

def create_api_app():
    app = Flask(__name__)
    app.secret_key = "clave_secreta_api"
    
    CORS(app, supports_credentials=True)

    # Rutas API
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(usuario_bp, url_prefix="/api/usuarios")
    app.register_blueprint(estadisticas_bp, url_prefix="/api/estadisticas")
    #
    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({"status": 200,
                        "message": "la api esta funcionando correctamente",
                        "service": "funcional",
                        }), 200
    return app

if __name__ == "__main__":
    app = create_api_app()
    app.run(debug=True, host="0.0.0.0", port=5001)  