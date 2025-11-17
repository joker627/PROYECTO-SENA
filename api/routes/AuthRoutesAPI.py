from flask import Blueprint, request, jsonify
from api.controller.AuthControllerAPI import AuthControllerAPI

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": 400, "error": "JSON no enviado"}), 400

    response = AuthControllerAPI.login(data)
    return jsonify(response), response.get("status", 500)
