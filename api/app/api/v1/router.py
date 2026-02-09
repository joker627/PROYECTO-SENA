# Definición del Router Principal de la API v1
from fastapi import APIRouter
from app.api.v1.endpoints import usuarios, contribuciones, reportes, estadisticas, auth, ia

router = APIRouter()

# Registro de rutas de Autenticación
router.include_router(auth.router,
    prefix="/auth",
    tags=["Autenticación"]
)

# Registro de rutas de Estadísticas del Sistema
router.include_router(estadisticas.router, 
    prefix="/estadisticas",
    tags=["Estadísticas"]
)

# Registro de rutas de Gestión de Usuarios
router.include_router(usuarios.router, 
    prefix="/usuarios",
    tags=["Usuarios"]
)

# Registro de rutas de Contribuciones de Señas
router.include_router(contribuciones.router, 
    prefix="/contribuciones", 
    tags=["Contribuciones"]
)

# Registro de rutas de Reportes de Errores
router.include_router(reportes.router, 
    prefix="/reportes", 
    tags=["Reportes"]
)

router.include_router(ia.router, 
    prefix="/ia", 
    tags=["Inteligencia Artificial"]
)
