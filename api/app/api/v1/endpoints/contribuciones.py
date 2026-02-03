from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.schemas.contribuciones import ContribucionResponse, ContribucionPaginated
from app.services import contribuciones as contrib_service
from app.core.dependencies import get_current_user_id

router = APIRouter()

@router.get("/stats")
def get_contribution_stats(current_user_id: int = Depends(get_current_user_id)):
    """Obtiene estadísticas de contribuciones (requiere autenticación)."""
    return contrib_service.obtener_stats_contribuciones()

@router.get("/", response_model=ContribucionPaginated)
def get_contribuciones(
    estado: Optional[str] = None, 
    query: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100,
    current_user_id: int = Depends(get_current_user_id)
):
    """Obtiene lista de contribuciones (requiere autenticación)."""
    result = contrib_service.obtener_contribuciones(estado, query, skip, limit)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.put("/{id_contribucion}/estado")
def update_contribution_status(
    id_contribucion: int, 
    estado: str, 
    observaciones: Optional[str] = None,
    current_user_id: int = Depends(get_current_user_id)
):
    """Actualiza el estado de una contribución (requiere autenticación)."""
    exito = contrib_service.actualizar_estado_contribucion(id_contribucion, estado, observaciones)
    if not exito:
        raise HTTPException(status_code=404, detail="Contribución no encontrada")
    return {"message": "Estado actualizado exitosamente"}
