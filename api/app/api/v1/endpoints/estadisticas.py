"""Endpoints de estadísticas del sistema."""

from fastapi import APIRouter, Depends
from app.services.estadisticas import obtener_estadisticas
from app.schemas.estadisticas import EstadisticaSchema
from app.core.dependencies import get_current_user_id

router = APIRouter()

@router.get("/", response_model=EstadisticaSchema)
def estadisticas(user_id: int = Depends(get_current_user_id)):
    """Obtiene estadísticas generales."""
    return obtener_estadisticas()
