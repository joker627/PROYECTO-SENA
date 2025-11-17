"""Rutas relacionadas con autenticación (login/logout) en la parte web.

Estas rutas delegan la lógica de autenticación en `UsuarioControllerWeb`.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from web.controller.usuario_controller_web import UsuarioControllerWeb


web_login = Blueprint("web_login", __name__)


@web_login.route("/login", methods=["POST"])
def login_post():
    correo = request.form.get("correo")
    contrasena = request.form.get("contrasena")
    # Usar el controlador web específico para login y manejo de sesión
    result = UsuarioControllerWeb.login_web(correo, contrasena, session)

    if result.get("status") != 200:
        flash(result.get("error", "Correo o contraseña incorrectos"), "error")
        return redirect(url_for("web_login.login_post"))

    flash(result.get("message", "Inicio de sesión exitoso"), "success")
    return redirect(url_for("web_bp.inicio")) 


@web_login.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for("web_bp.inicio"))
