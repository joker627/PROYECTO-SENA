from web.config.db import get_db_connection
from web.utils.password_utils import verify_password


class UsuarioModel:
	"""Modelo para operaciones sobre la tabla `usuarios`.
	Provee métodos para obtener usuarios y verificar credenciales.
	"""

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

	@staticmethod
	def eliminar(id_usuario):
		"""Elimina (o desactiva) un usuario por su id.
		Retorna True si se eliminó correctamente, False en caso contrario.
		"""
		conn = get_db_connection()
		try:
			with conn.cursor() as cursor:
				cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
				conn.commit()
				return cursor.rowcount > 0
		finally:
			conn.close()

	@staticmethod
	def listar(limit=100, search=None):
		"""Lista usuarios. Si `search` está presente realiza búsqueda por id, nombre o correo.
		Devuelve una lista de dicts.
		"""
		conn = get_db_connection()
		try:
			with conn.cursor() as cursor:
				if search and search.strip():
					term = search.strip()
					# Si es numérico, buscar por id además de nombre/correo
					params = []
					where_clauses = []
					if term.isdigit():
						where_clauses.append("id_usuario = %s")
						params.append(int(term))
					# case-insensitive LIKE for name and email
					where_clauses.append("LOWER(nombre_completo) LIKE %s")
					params.append(f"%{term.lower()}%")
					where_clauses.append("LOWER(correo) LIKE %s")
					params.append(f"%{term.lower()}%")
					where_sql = " OR ".join(where_clauses)
					sql = (
						"SELECT id_usuario, nombre_completo, correo, id_rol, estado "
						"FROM usuarios WHERE (" + where_sql + ") "
						"ORDER BY fecha_registro DESC LIMIT %s"
					)
					params.append(limit)
					cursor.execute(sql, tuple(params))
				else:
					cursor.execute("SELECT id_usuario, nombre_completo, correo, id_rol, estado FROM usuarios ORDER BY fecha_registro DESC LIMIT %s", (limit,))
				rows = cursor.fetchall()
				return rows
		finally:
			conn.close()

	@staticmethod
	def obtener_por_id(id_usuario):
		"""Devuelve un usuario por su id (sin contraseña)."""
		conn = get_db_connection()
		try:
			with conn.cursor() as cursor:
				cursor.execute("SELECT id_usuario, nombre_completo, correo, id_rol, estado FROM usuarios WHERE id_usuario = %s", (id_usuario,))
				return cursor.fetchone()
		finally:
			conn.close()