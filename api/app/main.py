# Punto de entrada FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
from app.core.config import settings

default_description = "api para la gestión de SIGNTECHNOLOGY"
app = FastAPI(title="SIGNTECHNOLOGY API", version="1.0.0", description=default_description)


# Configurar CORS para permitir conexiones desde el frontend
origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "API SIGNTECHNOLOGY funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a la API de SIGNTECHNOLOGY",
        "version": "1.0.0",
        "description": default_description,
        "endpoints": {
            "health": "/health",
            "api_v1": "/api/v1",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Router v1
app.include_router(v1_router, prefix="/api/v1")

#uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload