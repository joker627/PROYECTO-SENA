"""Router principal API v1."""
from fastapi import APIRouter
from app.api.v1.endpoints import usuarios, contribuciones, reportes, estadisticas, auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
router.include_router(estadisticas.router, prefix="/estadisticas", tags=["Estadísticas"])
router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
router.include_router(contribuciones.router, prefix="/contribuciones", tags=["Contribuciones"])
router.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])
