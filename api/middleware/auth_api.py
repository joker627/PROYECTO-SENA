# api/middleware/auth_api.py
from functools import wraps
from flask import request, jsonify
from api.middleware.auth_api import JWTUtils

def token_required():

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Extraer token del header
            token = JWTUtils.extraer_token(request.headers)
            if not token:
                return jsonify({"status": 401, "error": "Token faltante"}), 401

            # Verificar token
            verificacion = JWTUtils.verificar_token(token)
            if not verificacion["status"]:
                return jsonify({"status": 401, "error": verificacion["error"]}), 401

            # Guardar datos del usuario logueado
            request.user = verificacion["data"]

            return f(*args, **kwargs)
        return decorated
    return decorator
