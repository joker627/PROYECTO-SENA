"""Configuración centralizada de la aplicación.

Las variables se cargan desde el archivo .env y nunca deben
incluir valores hardcodeados para credenciales sensibles.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""
    
    # Configuración de base de datos
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Pool de conexiones
    DB_POOL_SIZE: int = 20          # Conexiones activas en el pool
    DB_MAX_OVERFLOW: int = 10       # Conexiones extra permitidas
    DB_POOL_RECYCLE: int = 3600     # Segundos antes de reciclar conexión
    DB_POOL_PRE_PING: bool = True   # Verificar conexión antes de usar

    # JWT (JSON Web Tokens)
    SECRET_KEY: str                 # Clave para firmar tokens
    ACCESS_TOKEN_EXPIRE: int        # Minutos de expiración del token
    ALGORITHM: str                  # Algoritmo de encriptación

    # CORS (Cross-Origin Resource Sharing)
    CORS_ORIGINS: str               # Dominios permitidos separados por comas

    class Config:
        env_file = ".env"


settings = Settings()
