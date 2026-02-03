"""Dependencias FastAPI para autenticación y autorización."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.core.logger import logger

security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Extrae el ID del usuario desde el token JWT."""
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("user_id")
        if user_id is None:
            logger.warning("Token inválido: falta user_id en el payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta user_id"
            )
        return int(user_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Token inválido: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

def require_role(required_role: int):
    """Valida que el usuario tenga el rol requerido (1=Admin, 2=Colaborador)."""
    def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
        try:
            payload = decode_token(credentials.credentials)
            if payload.get("role") != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para esta acción"
                )
            return payload.get("sub")
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Error validando rol: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )
    return role_checker
