"""Dependencias de FastAPI para autenticación y autorización.

Proporciona funciones reutilizables para proteger endpoints
y obtener el usuario actual del token JWT.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.core.logger import logger

security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Extrae y valida el ID del usuario desde el token JWT.
    
    Args:
        credentials: Credenciales Bearer del header Authorization.
        
    Returns:
        ID del usuario autenticado.
        
    Raises:
        HTTPException 401: Si el token es inválido o expirado.
    """
    try:
        token = credentials.credentials
        payload = decode_token(token)
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta subject"
            )
            
        return int(user_id)
        
    except Exception as e:
        logger.warning(f"Token inválido: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )


def require_role(required_role: int):
    """Crea una dependencia que valida el rol del usuario.
    
    Args:
        required_role: ID del rol requerido (1=Admin, 2=Colaborador).
        
    Returns:
        Función de dependencia que valida el rol.
    """
    def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
        try:
            token = credentials.credentials
            payload = decode_token(token)
            
            user_role = payload.get("role")
            if user_role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para realizar esta acción"
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
