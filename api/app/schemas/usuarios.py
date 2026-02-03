"""Schemas de usuarios."""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre_completo: str
    correo: EmailStr
    tipo_documento: str
    numero_documento: str
    id_rol: int = 2
    estado: str = "activo"
    
class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    imagen_perfil: Optional[str] = None
    id_rol: Optional[int] = None
    estado: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    imagen_perfil: Optional[str] = None
    fecha_registro: datetime
    nombre_rol: Optional[str] = None

    class Config:
        from_attributes = True

class UsuarioPaginated(BaseModel):
    total: int
    page: int
    limit: int
    data: List[UsuarioResponse]
