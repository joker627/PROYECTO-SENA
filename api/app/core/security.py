"""Módulo de seguridad para autenticación y encriptación.

Maneja:
- Encriptación de contraseñas con bcrypt
- Generación y validación de tokens JWT
"""

from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones para manejo de contraseñas

def hash_password(password: str) -> str:
    """Encripta una contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano.
        
    Returns:
        Hash encriptado de la contraseña.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash.
    
    Args:
        plain_password: Contraseña en texto plano.
        hashed_password: Hash almacenado en la base de datos.
        
    Returns:
        True si la contraseña es correcta, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Funciones para manejo de tokens JWT

def create_access_token(data: dict) -> str:
    """Genera un token JWT para autenticación.
    
    Según mejores prácticas de seguridad, el token solo debe contener
    datos mínimos necesarios para identificación (sub, email, role).
    El perfil completo se obtiene mediante endpoint protegido.
    
    Args:
        data: Datos mínimos (sub: user_id, email, role).
        
    Returns:
        Token JWT codificado con tiempo de expiración.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decodifica y valida un token JWT.
    
    Args:
        token: Token JWT a decodificar.
        
    Returns:
        Datos contenidos en el token.
        
    Raises:
        Exception: Si el token está expirado o es inválido.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")
