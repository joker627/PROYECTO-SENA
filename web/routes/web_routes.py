"""Rutas públicas de la aplicación web (Jinja).

Este módulo expone endpoints que usan controladores web (no la API).
Por ejemplo, manejo de usuarios anónimos y páginas estáticas.
"""

from flask import Blueprint, render_template, make_response, request, redirect
from web.controller.anonimo_controller_web import AnonimoControllerWeb

web_bp = Blueprint("web_bp", __name__)

@web_bp.route('/anonimo/generar', methods=['POST', 'GET'])
def generar_anonimo_web():
    """Genera un UUID en servidor para usuarios web y fija la cookie.
    Redirige a la página anterior o al inicio.
    """
    response = AnonimoControllerWeb.generar_anonimo()
    if not response or not response.get('uuid'):
        # Fallo: redirigir al inicio con flash no disponible aquí
        return redirect(request.referrer or '/')

    resp = make_response(redirect(request.referrer or '/'))
    resp.set_cookie('uuid_anonimo', response['uuid'], max_age=3600*24*365, httponly=True, samesite='Lax')
    return resp


@web_bp.route("/")
def inicio():
    return render_template("index.html")

# FORMULARIO
@web_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("admin/login.html")

