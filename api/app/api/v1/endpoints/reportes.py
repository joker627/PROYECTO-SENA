from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.schemas.reportes import ReporteResponse, ReportePaginated
from app.services import reportes as reporte_service

router = APIRouter()

@router.get("/stats")
def get_report_stats():
    return reporte_service.obtener_stats_reportes()

@router.get("/", response_model=ReportePaginated)
def get_reportes(
    estado: Optional[str] = None, 
    prioridad: Optional[str] = None,
    query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    result = reporte_service.obtener_reportes(estado, prioridad, query, skip, limit)
    return {
        "total": result["total"],
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "limit": limit,
        "data": result["data"]
    }

@router.put("/{id_reporte}/gestion")
def update_report_gestion(id_reporte: int, estado: str = None, prioridad: str = None):
    """Actualiza el estado y/o prioridad de un reporte.
    
    El servicio lanza HTTPException si hay errores,
    retorna None si no se encuentra, o True si es exitoso.
    """
    resultado = reporte_service.actualizar_gestion_reporte(id_reporte, estado, prioridad)
    
    if resultado is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    return {"message": "Reporte actualizado exitosamente"}

@router.delete("/{id_reporte}")
def resolver_reporte(id_reporte: int):
    """Resuelve un reporte eliminándolo de la base de datos.
    
    El servicio lanza HTTPException si hay errores,
    retorna None si no se encuentra, o True si es exitoso.
    """
    resultado = reporte_service.eliminar_reporte(id_reporte)
    
    if resultado is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    return {"message": "Reporte resuelto y eliminado exitosamente"}
