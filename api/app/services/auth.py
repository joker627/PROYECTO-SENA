"""Servicio de autenticación de usuarios con manejo robusto de errores."""

import pymysql
from fastapi import HTTPException, status
from app.core.database import get_connection
from app.core.logger import logger
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
    conn = None
    
    try:
        conn = get_connection()
        
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
            logger.warning(f"Intento de login con correo inexistente: {correo}")
            return None

        # Verificar contraseña
        if not verify_password(contrasena, user["contrasena"]):
            logger.warning(f"Intento de login con contraseña incorrecta para: {correo}")
            return None

        # Generar token JWT solo con datos mínimos (mejores prácticas de seguridad)
        token = create_access_token({
            "sub": user["id_usuario"],  # subject (ID del usuario)
            "email": user["correo"],
            "role": user["id_rol"]
        })

        logger.info(f"Login exitoso para usuario: {correo}")
        return token
        
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en authenticate_user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al autenticar usuario"
        )
    except Exception as e:
        logger.error(f"Error inesperado en authenticate_user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")
