"""Endpoints de gestión de contribuciones."""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.schemas.contribuciones import ContribucionResponse, ContribucionPaginated
from app.services import contribuciones as contrib_service
from app.core.dependencies import get_current_user_id, require_role

router = APIRouter()

@router.get("/stats")
def get_contribution_stats(user_id: int = Depends(get_current_user_id)):
    """Estadísticas de contribuciones."""
    return contrib_service.obtener_stats_contribuciones()

@router.get("/", response_model=ContribucionPaginated)
def get_contribuciones(
    estado: Optional[str] = None, 
    query: Optional[str] = None, 
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000),
    user_id: int = Depends(get_current_user_id)
):
    """Lista paginada de contribuciones."""
    result = contrib_service.obtener_contribuciones(estado, query, skip, limit)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.put("/{id_contribucion}/estado")
def update_contribution_status(id_contribucion: int, estado: str, observaciones: Optional[str] = None, user_id: int = Depends(require_role(1))):
    """Actualiza estado de una contribución."""
    exito = contrib_service.actualizar_estado_contribucion(id_contribucion, estado, observaciones)
    if not exito:
        raise HTTPException(status_code=404, detail="Contribución no encontrada")
    return {"message": "Estado actualizado exitosamente"}
