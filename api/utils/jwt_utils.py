import jwt
from datetime import datetime, timedelta

class JWTUtils:
    SECRET_KEY = "ESTA_CLAVE_CAMBIALA_POR_UNA_MUY_SEGURA"
    ALGORITHM = "HS256"
    EXPIRES_IN_MINUTES = 60 * 24  # 24 horas

    @staticmethod
    def generar_token(payload: dict) -> str:
        """
        Genera un JWT válido con expiración.
        """
        data = payload.copy()
        data["exp"] = datetime.utcnow() + timedelta(minutes=JWTUtils.EXPIRES_IN_MINUTES)
        token = jwt.encode(data, JWTUtils.SECRET_KEY, algorithm=JWTUtils.ALGORITHM)
        return token

    @staticmethod
    def verificar_token(token: str):
        """
        Verifica que el token sea válido y no esté expirado.
        Devuelve el payload si está bien.
        """
        try:
            decoded = jwt.decode(token, JWTUtils.SECRET_KEY, algorithms=[JWTUtils.ALGORITHM])
            return {"status": True, "data": decoded}
        except jwt.ExpiredSignatureError:
            return {"status": False, "error": "Token expirado"}
        except jwt.InvalidTokenError:
            return {"status": False, "error": "Token inválido"}

    @staticmethod
    def extraer_token(headers):
        """
        Extrae el token del header Authorization: Bearer <token>.
        """
        auth = headers.get("Authorization", None)
        if not auth:
            return None

        partes = auth.split()
        if len(partes) != 2 or partes[0].lower() != "bearer":
            return None

        return partes[1]
