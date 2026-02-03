"""Configuración de la aplicación desde variables de entorno."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración cargada desde .env"""
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_PRE_PING: bool = True

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int
    ALGORITHM: str

    CORS_ORIGINS: str

    class Config:
        env_file = ".env"

settings = Settings()
