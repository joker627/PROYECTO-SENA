from app.core.database import get_connection
from app.core.security import verify_password, create_access_token


def authenticate_user(correo: str, contrasena: str):
    """Autentica al usuario leyendo directamente de la base de datos."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT u.id_usuario, u.nombre_completo, u.correo, u.contrasena, u.tipo_documento, "
                "u.numero_documento, u.imagen_perfil, u.id_rol, u.estado, u.fecha_registro, r.nombre_rol "
                "FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol "
                "WHERE u.correo=%s",
                (correo,)
            )
            user = cursor.fetchone()

        if not user:
            return None

        if not verify_password(contrasena, user["contrasena"]):
            return None

        # Token solo con información mínima necesaria
        token = create_access_token({
            "sub": user["correo"],
            "user_id": user["id_usuario"]
        })

        return token
    except Exception as e:
        print("Error autenticando usuario:", e)
        return None
    finally:
        conn.close()
