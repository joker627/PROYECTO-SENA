# middleware/anonimo_middleware.py
from flask import request, g, current_app
from web.controller.anonimo_controller_web import AnonimoControllerWeb


def anonimo_middleware(app):
    @app.before_request
    def gestionar_anonimo():

        # 1) Preferir cookie (solo para web)
        uuid_cookie = request.cookies.get("uuid_anonimo")

        # 2) Si no hay cookie, intentar leer uuid enviado por el cliente (header/query/body)
        client_uuid = None
        if not uuid_cookie:
            client_uuid = request.headers.get("X-UUID-ANONIMO")
            if not client_uuid:
                client_uuid = request.args.get("uuid")
            if not client_uuid and request.is_json:
                data = request.get_json(silent=True) or {}
                client_uuid = data.get("uuid")

        # Decidir cuál UUID usar (cookie tiene preferencia)
        chosen_uuid = uuid_cookie or client_uuid

        controller = AnonimoControllerWeb
        auto_flag = current_app.config.get('ANONIMO_WEB_AUTO_GENERATE', True)

        # Si no hay uuid elegido y no está permitido autogenerar, no hacemos nada
        if not chosen_uuid and not auto_flag:
            return None

        # Obtener o crear el anonimo en contexto web
        try:
            result = controller.crear_o_obtener_anonimo(chosen_uuid, auto_flag)
        except Exception:
            # No queremos que un error en la gestión de anonimos rompa la app web
            g.uuid_anonimo = None
            return None

        if isinstance(result, dict) and result.get('status') in (200, 201):
            g.uuid_anonimo = result.get('uuid')
            # Si no había cookie, indicamos que debe crearse en la respuesta
            if not uuid_cookie and result.get('uuid'):
                g._anonimo_cookie_to_set = result.get('uuid')
        else:
            g.uuid_anonimo = None

    @app.after_request
    def _set_anonimo_cookie(response):

        cookie_val = getattr(g, '_anonimo_cookie_to_set', None)
        if cookie_val:
            response.set_cookie('uuid_anonimo', cookie_val, max_age=3600*24*365, httponly=True, samesite='Lax', path='/')
            # limpiar para evitar reuso accidental
            try:
                delattr(g, '_anonimo_cookie_to_set')
            except Exception:
                pass

        return response


