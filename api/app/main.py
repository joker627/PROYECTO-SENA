"""Punto de entrada principal de la API SignTechnology.

Gestiona el ciclo de vida de la aplicación, incluyendo:
- Inicialización del pool de conexiones a la base de datos
- Configuración de CORS para permitir peticiones cross-origin
- Registro de rutas bajo el prefijo /api/v1
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.database import init_pool, close_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación.
    
    Startup: Inicializa el pool de conexiones a MySQL.
    Shutdown: Cierra todas las conexiones del pool y libera recursos.
    """
    # Inicializar pool de conexiones al arrancar
    print("Inicializando pool de conexiones...")
    init_pool()
    print("Pool de conexiones inicializado")
    
    yield
    
    # Cerrar pool de conexiones al detener
    print("Cerrando pool de conexiones...")
    close_pool()
    print("Pool cerrado correctamente")

app = FastAPI(
    title="SIGNTECHNOLOGY API",
    version="1.0.0",
    lifespan=lifespan,
    description="API REST para la gestión del sistema SignTechnology - SENA"
)

# Configurar CORS para permitir peticiones desde el frontend
origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "API SIGNTECHNOLOGY funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Incluir el router v1 bajo el prefijo estándar '/api/v1'
app.include_router(v1_router, prefix="/api/v1")

# uvicorn app.main:app --host 192.168.1.40 --port 8000 --reload