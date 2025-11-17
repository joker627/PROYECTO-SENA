from web.models.anonimo_model import UsuarioAnonimoModel
from web.utils.uuid_utils import generar_uuid_anonimo
import re


class AnonimoControllerWeb:
    """Maneja la creación y recuperación de usuarios anónimos. La API web
    utiliza estos métodos para generar o validar `uuid_anonimo` y delega en el
    modelo `UsuarioAnonimoModel` para la persistencia.
    """

    @staticmethod
    def crear_o_obtener_anonimo(uuid=None, auto_generate=True):
        # Normalizar y decidir generación
        if not uuid:
            if auto_generate:
                uuid = generar_uuid_anonimo()
            else:
                return {"status": 400, "error": "UUID requerido"}

        uuid = str(uuid).strip()[:50]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", uuid):
            return {"status": 400, "error": "UUID inválido"}

        try:
            existente = UsuarioAnonimoModel.obtener_por_uuid(uuid)
            if existente:
                return {
                    "status": 200,
                    "message": "Usuario anónimo existente",
                    "id_anonimo": existente.get("id_anonimo") if isinstance(existente, dict) else existente["id_anonimo"],
                    "uuid": uuid,
                }

            creado = UsuarioAnonimoModel.crear_con_uuid(uuid)
            return {
                "status": 201,
                "message": "Usuario anónimo creado (web)",
                "id_anonimo": creado.get("id_anonimo"),
                "uuid": creado.get("uuid"),
            }
        except Exception as e:
            return {"status": 500, "error": "Error al crear anonimo (web)", "details": str(e)}

    @staticmethod
    def generar_anonimo():
        # Generar UUID y crear registro usando el modelo directamente
        try:
            creado = UsuarioAnonimoModel.crear_anonimo()
            return {"status": 201, "message": "Usuario anónimo creado (web)", "id_anonimo": creado.get("id_anonimo"), "uuid": creado.get("uuid")}
        except Exception as e:
            return {"status": 500, "error": "Error al generar anonimo (web)", "details": str(e)}
