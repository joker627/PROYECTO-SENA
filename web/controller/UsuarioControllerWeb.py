from shared.models.usuario_model import UsuarioModel

class UsuarioControllerWeb:

    @staticmethod
    def obtener_por_correo(correo):
        return UsuarioModel.obtener_por_correo(correo)

    @staticmethod
    def login(correo, contrasena):
        return UsuarioModel.login(correo, contrasena)

    @staticmethod
    def login_web(correo, contrasena, session):
        usuario = UsuarioModel.login(correo, contrasena)
        if not usuario:
            return {"status": 400, "error": "Credenciales inválidas"}

        # Establecer sesión
        session["user_id"] = usuario.get("id_usuario")
        session["username"] = usuario.get("nombre_completo")
        session["rol"] = usuario.get("id_rol")
        session["correo"] = usuario.get("correo")

        return {
            "status": 200,
            "message": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario.get("id_usuario"),
                "nombre": usuario.get("nombre_completo"),
                "correo": usuario.get("correo"),
                "rol": usuario.get("id_rol"),
                "estado": usuario.get("estado")
            }
        }
