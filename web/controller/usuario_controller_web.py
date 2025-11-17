from web.models.usuario_model import UsuarioModel


class UsuarioControllerWeb:
    """Controlador encargado de operaciones relacionadas con usuarios
    (autenticación y consultas básicas). Los métodos devuelven estructuras
    Python simples que las rutas pueden consumir directamente.
    """

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

    @staticmethod
    def eliminar_usuario(id_usuario):
        """Elimina un usuario delegando al modelo. Retorna dict con status."""
        try:
            result = UsuarioModel.eliminar(id_usuario)
            if result:
                return {"status": 200, "message": "Usuario eliminado"}
            return {"status": 404, "error": "Usuario no encontrado"}
        except Exception as e:
            return {"status": 500, "error": "Error al eliminar usuario", "details": str(e)}

    @staticmethod
    def listar_usuarios(limit=100, search=None):
        """Devuelve la lista de usuarios (delegando al modelo). Acepta parámetro opcional `search` para búsqueda."""
        try:
            usuarios = UsuarioModel.listar(limit=limit, search=search)
            return usuarios
        except Exception:
            return []
