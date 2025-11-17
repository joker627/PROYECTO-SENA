from web.config.db import get_db_connection
from shared.utils.password_utils import hash_password, verify_password


class UsuarioModel:

    # 
	@staticmethod
	def obtener_por_correo(correo):
		conn = get_db_connection()
		with conn.cursor() as cursor:
			cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
			return cursor.fetchone()


    # verificar contrasena y correo 
	@staticmethod
	def login(correo, contrasena):
		usuario = UsuarioModel.obtener_por_correo(correo)
		if not usuario:
			return None
		if verify_password(contrasena, usuario["contrasena"]):
			return usuario
		return None