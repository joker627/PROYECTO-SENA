# UserCreate, UserOut, UserLogin
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLoginSchema(BaseModel):
    correo: EmailStr
    contrasena: str


class UserInfoSchema(BaseModel):
    id_usuario: int
    nombre_completo: str
    correo: EmailStr
    tipo_documento: str
    numero_documento: str
    imagen_perfil: Optional[str] = None
    id_rol: int
    nombre_rol: str
    estado: str
    fecha_registro: str


class TokenResponse(BaseModel):
    """Respuesta del login con token JWT.
    
    Según mejores prácticas, solo retorna el token.
    El perfil completo se obtiene con GET /usuarios/me usando el token.
    """
    access_token: str
    token_type: str = "bearer"
