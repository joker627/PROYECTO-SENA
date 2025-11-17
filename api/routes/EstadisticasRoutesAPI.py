from flask import Blueprint, jsonify
from api.controller.EstadisticasControllerAPI import EstadisticasControllerAPI
from api.middleware.auth_api import token_required

estadisticas_bp = Blueprint("estadisticas_bp", __name__)


@estadisticas_bp.route("/", methods=["GET"])
@token_required()
def obtener_estadisticas():
    response = EstadisticasControllerAPI.obtener_estadisticas()
    return jsonify(response), response.get("status", 500)
