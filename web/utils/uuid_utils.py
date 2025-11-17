# utils/uuid_utils.py
import uuid

def generar_uuid_anonimo():
    """
    Genera un UUID con prefijo 'uuid_' para un usuario anónimo.
    """
    return f"uuid_{uuid.uuid4()}"
