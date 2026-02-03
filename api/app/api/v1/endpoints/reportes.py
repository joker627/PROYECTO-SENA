"""Endpoints de gestión de reportes."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.schemas.reportes import ReporteResponse, ReportePaginated
from app.services import reportes as reporte_service
from app.core.dependencies import get_current_user_id, require_role

router = APIRouter()

@router.get("/stats")
def get_report_stats(user_id: int = Depends(get_current_user_id)):
    """Estadísticas de reportes."""
    return reporte_service.obtener_stats_reportes()

@router.get("/", response_model=ReportePaginated)
def get_reportes(
    estado: Optional[str] = None, 
    prioridad: Optional[str] = None,
    query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    user_id: int = Depends(get_current_user_id)
):
    """Lista paginada de reportes."""
    result = reporte_service.obtener_reportes(estado, prioridad, query, skip, limit)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.put("/{id_reporte}/gestion")
def update_report_gestion(id_reporte: int, estado: str = None, prioridad: str = None, user_id: int = Depends(require_role(1))):
    """Actualiza estado y/o prioridad de un reporte."""
    resultado = reporte_service.actualizar_gestion_reporte(id_reporte, estado, prioridad)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"message": "Reporte actualizado exitosamente"}

@router.delete("/{id_reporte}")
def resolver_reporte(id_reporte: int, user_id: int = Depends(require_role(1))):
    """Elimina un reporte resuelto."""
    resultado = reporte_service.eliminar_reporte(id_reporte)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"message": "Reporte resuelto y eliminado exitosamente"}
