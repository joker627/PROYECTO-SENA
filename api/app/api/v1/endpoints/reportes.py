from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.schemas.reportes import ReporteResponse, ReportePaginated
from app.services import reportes as reporte_service
from app.core.dependencies import get_current_user_id

router = APIRouter()

@router.get("/stats")
def get_report_stats(current_user_id: int = Depends(get_current_user_id)):
    """Obtiene estadísticas de reportes (requiere autenticación)."""
    return reporte_service.obtener_stats_reportes()

@router.get("/", response_model=ReportePaginated)
def get_reportes(
    estado: Optional[str] = None, 
    prioridad: Optional[str] = None,
    query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user_id: int = Depends(get_current_user_id)
):
    """Obtiene lista de reportes (requiere autenticación)."""
    result = reporte_service.obtener_reportes(estado, prioridad, query, skip, limit)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.put("/{id_reporte}/gestion")
def update_report_gestion(
    id_reporte: int, 
    estado: str = None, 
    prioridad: str = None,
    current_user_id: int = Depends(get_current_user_id)
):
    """Actualiza la gestión de un reporte (requiere autenticación)."""
    exito = reporte_service.actualizar_gestion_reporte(id_reporte, estado, prioridad)
    if not exito:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return {"message": "Reporte actualizado exitosamente"}
