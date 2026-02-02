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
    access_token: str
    token_type: str = "bearer"
    user: UserInfoSchema
