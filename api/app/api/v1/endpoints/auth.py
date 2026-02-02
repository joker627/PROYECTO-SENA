"""Endpoints de autenticación de usuarios."""

from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserLoginSchema, TokenResponse
from app.services.auth import authenticate_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(form_data: UserLoginSchema):
    """Procesa el inicio de sesión del usuario.
    
    Verifica las credenciales y genera un token de acceso JWT.
    
    Args:
        form_data: Credenciales del usuario (correo y contraseña).
        
    Returns:
        Token de acceso y datos del usuario autenticado.
        
    Raises:
        HTTPException 401: Si las credenciales son incorrectas.
    """
    result = authenticate_user(form_data.correo, form_data.contrasena)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrecta"
        )

    token, user_info = result
    
    return {
        "access_token": token,
        "user": user_info
    }

