# Endpoints para Autenticación de Usuarios
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserLoginSchema, TokenResponse
from app.services.auth import authenticate_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(form_data: UserLoginSchema):
    """
    Procesa el inicio de sesión del usuario.
    Verifica las credenciales y genera un token de acceso si son válidas.
    """
    token = authenticate_user(form_data.correo, form_data.contrasena)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrecta"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

