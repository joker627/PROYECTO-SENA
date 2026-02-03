"""Schemas de autenticación."""

from pydantic import BaseModel, EmailStr

class UserLoginSchema(BaseModel):
    correo: EmailStr
    contrasena: str

class TokenResponse(BaseModel):
    """Respuesta con token JWT."""
    access_token: str
    token_type: str = "bearer"
