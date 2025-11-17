from shared.models.usuario_model import UsuarioModel
from api.config.db import get_db_api_connection
from shared.utils.password_utils import hash_password
import datetime


class UsuarioControllerAPI:
    @staticmethod
    def obtener_por_correo(correo):
        return UsuarioModel.obtener_por_correo(correo)

    @staticmethod
    def crear_administrador(data, creador_id=None):
        # Esperamos: nombre_completo, correo, contrasena, opcional id_rol
        nombre = data.get('nombre') or data.get('nombre_completo')
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        id_rol = data.get('id_rol', 2)  # por defecto 2 (admin) si no se especifica

        if not nombre or not correo or not contrasena:
            return {"status": 400, "error": "Faltan campos requeridos"}

        hashed = hash_password(contrasena)

        conn = get_db_api_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre_completo, correo, contrasena, id_rol, fecha_registro, creado_por) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nombre, correo, hashed, id_rol, datetime.datetime.now(), creador_id)
                )
                conn.commit()
                user_id = cursor.lastrowid
        except Exception as e:
            conn.close()
            return {"status": 500, "error": "Error creando administrador", "details": str(e)}

        conn.close()
        return {"status": 201, "message": "Administrador creado", "id_usuario": user_id}
