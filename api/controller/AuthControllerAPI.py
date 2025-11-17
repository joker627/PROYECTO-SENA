from shared.models.usuario_model import UsuarioModel
from shared.utils.jwt_utils import JWTUtils

class AuthControllerAPI:

    @staticmethod
    def login(data):
        correo = data.get("correo")
        contrasena = data.get("contrasena")

        if not correo or not contrasena:
            return {"status": 400, "error": "Datos incompletos o inválidos"}

        usuario = UsuarioModel.login(correo, contrasena)

        if not usuario:
            return {"status": 400, "error": "Credenciales inválidas"}

        # Crear TOKEN
        token = JWTUtils.generar_token({
            "id": usuario["id_usuario"],
            "correo": usuario["correo"],
            "rol": usuario["id_rol"]
        })
        print("=== LOGIN API ===")

        return {
            "status": 200,
            "message": "Login exitoso",
            "token": token,
            "usuario": {
                "id": usuario["id_usuario"],
                "nombre": usuario["nombre_completo"],
                "correo": usuario["correo"],
                "rol": usuario["id_rol"],
                "estado": usuario["estado"]
            }
        }
