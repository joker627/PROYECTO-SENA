"""Servicio de autenticación de usuarios."""

import pymysql
from fastapi import HTTPException, status
from app.core.database import get_connection
from app.core.logger import logger
from app.core.security import verify_password, create_access_token

def authenticate_user(correo: str, contrasena: str):
    """Valida credenciales y genera token JWT. Retorna token o None."""
    conn = None
    
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT u.id_usuario, u.correo, u.contrasena, u.id_rol "
                "FROM usuarios u WHERE u.correo=%s",
                (correo,)
            )
            user = cursor.fetchone()

        if not user:
            logger.warning(f"Login fallido: correo inexistente {correo}")
            return None

        if not verify_password(contrasena, user["contrasena"]):
            logger.warning(f"Login fallido: contraseña incorrecta {correo}")
            return None

        token = create_access_token({
            "sub": user["id_usuario"],
            "email": user["correo"],
            "role": user["id_rol"]
        })

        logger.info(f"Login exitoso: {correo}")
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
