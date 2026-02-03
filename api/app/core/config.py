from pydantic_settings import BaseSettings

# Creamos clase Settings que hereda de BaseSettings
class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int 
    ALGORITHM: str

    # CORS
    CORS_ORIGINS: str

    class Config:
        env_file = ".env"


settings = Settings()
