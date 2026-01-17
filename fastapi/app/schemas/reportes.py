from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReporteBase(BaseModel):
    descripcion_error: str
    evidencia_url: str
    prioridad: str = "media"
    tipo_traduccion: Optional[str] = None

class ReporteCreate(ReporteBase):
    pass

class ReporteUpdate(BaseModel):
    estado: Optional[str] = None
    prioridad: Optional[str] = None

class ReporteResponse(ReporteBase):
    id_reporte: int
    estado: str
    fecha_reporte: datetime
    nombre_usuario: Optional[str] = None

    class Config:
        from_attributes = True

from typing import List
class ReportePaginated(BaseModel):
    total: int
    page: int
    limit: int
    data: List[ReporteResponse]
