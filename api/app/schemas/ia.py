"""Schemas para el módulo de IA (traducción de lenguaje de señas)."""
from pydantic import BaseModel


class TraduccionResponse(BaseModel):
    """Respuesta con la palabra detectada en el video."""
    palabra: str
