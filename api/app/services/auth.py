"""Servicio de autenticación de usuarios."""

from app.core.database import get_connection
from app.core.security import verify_password, create_access_token


def authenticate_user(correo: str, contrasena: str):
    """Autentica un usuario validando sus credenciales.
    
    Busca el usuario por correo, verifica la contraseña y genera un token JWT.
    
    Args:
        correo: Correo electrónico del usuario.
        contrasena: Contraseña en texto plano.
        
    Returns:
        tuple: (token, user_info) si la autenticación es exitosa.
        None: Si las credenciales son incorrectas.
    """
    conn = get_connection()
    
    try:
        with conn.cursor() as cursor:
            # Buscar usuario y su rol
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

        # Verificar contraseña
        if not verify_password(contrasena, user["contrasena"]):
            return None

        # Generar token JWT
        token = create_access_token({
            "token": user["correo"], 
            "user_id": user["id_usuario"]
        })

        # Preparar información del usuario (sin la contraseña)
        user_info = {
            "id_usuario": user.get("id_usuario"),
            "nombre_completo": user.get("nombre_completo"),
            "correo": user.get("correo"),
            "id_rol": user.get("id_rol"),
            "nombre_rol": user.get("nombre_rol"),
            "estado": user.get("estado"),
            "fecha_registro": str(user.get("fecha_registro")),
            "tipo_documento": user.get("tipo_documento"),
            "numero_documento": user.get("numero_documento"),
            "imagen_perfil": user.get("imagen_perfil") or "user.svg"
        }

        return token, user_info
        
    except Exception as e:
        print(f"Error autenticando usuario: {e}")
        return None
        
    finally:
        conn.close()
