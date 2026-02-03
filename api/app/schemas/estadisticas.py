"""Schemas de estadísticas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EstadisticaSchema(BaseModel):
    total_traducciones: int = 0
    total_contribuciones: int = 0
    contribuciones_pendientes: int = 0
    contribuciones_aprobadas: int = 0
    senas_oficiales: int = 0
    reportes_activos: int = 0
    precision_modelo: float = 0.0
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
