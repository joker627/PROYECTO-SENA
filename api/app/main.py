"""API SignTechnology - Sistema de gestión para Lengua de Señas Colombiana."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.database import init_pool, close_pool
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja inicio y cierre de la aplicación."""
    logger.info("Iniciando aplicación SignTechnology...")
    init_pool()
    logger.info("Pool de conexiones inicializado")
    
    yield
    
    logger.info("Cerrando aplicación...")
    close_pool()
    logger.info("Aplicación cerrada")

app = FastAPI(
    title="SIGNTECHNOLOGY API",
    version="1.0.0",
    lifespan=lifespan,
    description="API REST para la gestión del sistema SignTechnology - SENA"
)

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

app.include_router(v1_router, prefix="/api/v1")

# uvicorn app.main:app --host 192.168.1.40 --port 8000 --reload