# app/api/v1/endpoints/estadisticas.py
from fastapi import APIRouter
from app.services.estadisticas import obtener_estadisticas
from app.schemas.estadisticas import EstadisticaSchema

router = APIRouter()

@router.get("/", response_model=EstadisticaSchema)
def estadisticas():
    return obtener_estadisticas()
