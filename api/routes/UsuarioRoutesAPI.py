from flask import Blueprint, request, jsonify
from api.controller.UsuarioControllerAPI import UsuarioControllerAPI
from api.middleware.auth_api import token_required

usuario_bp = Blueprint("usuario_bp", __name__)


@usuario_bp.route("/crear-admin", methods=["POST"])
@token_required()
def crear_admin():
    # Verifica que el usuario logueado sea SuperAdmin
    if request.user["rol"] != 3:
        return jsonify({"status": 403, "error": "No tienes permisos para crear administradores"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": 400, "error": "JSON no enviado"}), 400

    response = UsuarioControllerAPI.crear_administrador(data, request.user["id"])
    return jsonify(response), response.get("status", 500)


# Obtener usuario por correo

@usuario_bp.route("/correo/<correo>", methods=["GET"])
@token_required()
def obtener_usuario_por_correo(correo):
    usuario = UsuarioControllerAPI.obtener_por_correo(correo)

    if not usuario:
        return jsonify({"status": 404, "error": "Usuario no encontrado"}), 404

    # Retornamos solo los datos necesarios, sin la contraseña
    return jsonify({
        "status": 200,
        "usuario": {
            "id": usuario["id_usuario"],
            "nombre": usuario["nombre_completo"],
            "correo": usuario["correo"],
            "rol": usuario["id_rol"],
            "estado": usuario["estado"]
        }
    }), 200
