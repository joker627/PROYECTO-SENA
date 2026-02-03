"""Schemas de contribuciones."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContribucionBase(BaseModel):
    palabra_asociada: str
    descripcion: str
    archivo_video: str

class ContribucionCreate(ContribucionBase):
    pass

class ContribucionUpdate(BaseModel):
    estado: Optional[str] = None
    observaciones_gestion: Optional[str] = None

class ContribucionResponse(ContribucionBase):
    id_contribucion: int
    estado: str
    fecha_contribucion: datetime
    fecha_gestion: Optional[datetime] = None
    observaciones_gestion: Optional[str] = None
    nombre_usuario: Optional[str] = None

    class Config:
        from_attributes = True

class ContribucionPaginated(BaseModel):
    total: int
    page: int
    limit: int
    data: List[ContribucionResponse]
