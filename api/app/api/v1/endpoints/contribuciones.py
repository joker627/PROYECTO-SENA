from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.contribuciones import ContribucionResponse, ContribucionPaginated
from app.services import contribuciones as contrib_service

router = APIRouter()

@router.get("/stats")
def get_contribution_stats():
    return contrib_service.obtener_stats_contribuciones()

@router.get("/", response_model=ContribucionPaginated)
def get_contribuciones(
    estado: Optional[str] = None, 
    query: Optional[str] = None, 
    skip: int = Query(0, ge=0, description="Número de registros a saltar"), 
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar")
):
    result = contrib_service.obtener_contribuciones(estado, query, skip, limit)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.put("/{id_contribucion}/estado")
def update_contribution_status(id_contribucion: int, estado: str, observaciones: Optional[str] = None):
    exito = contrib_service.actualizar_estado_contribucion(id_contribucion, estado, observaciones)
    if not exito:
        raise HTTPException(status_code=404, detail="Contribución no encontrada")
    return {"message": "Estado actualizado exitosamente"}
