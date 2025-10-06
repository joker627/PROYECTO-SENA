# UTILIDADES PARA CONTRASEÑAS SEGURAS

# Funciones para manejar contraseñas de forma segura:
# - hash_password() -> Convertir contraseña normal a segura
# - verify_password() -> Verificar si contraseña es correcta
# - check_password_format() -> Decir si contraseña es segura o no
# - generate_salt() -> Crear sal aleatoria para seguridad extra
# Usamos bcrypt para hashing seguro

import secrets
import bcrypt

# Convertir contraseña normal a segura
def hash_password(pwd_text):
    
    pwd_bytes = pwd_text.encode('utf-8')
    # Crear sal aleatoria
    salt = bcrypt.gensalt()
    
    # Crear hash seguro combinando contraseña + sal
    secure_hash = bcrypt.hashpw(pwd_bytes, salt)
    # Convertir de vuelta a texto para guardar
    return secure_hash.decode('utf-8')

# Verificar si contraseña es correcta
def verify_password(user_pwd, stored_hash):
    try:
        if not user_pwd or not stored_hash:
            return False
        
        # Verificar si la contraseña está hasheada (segura) o texto plano
        if stored_hash.startswith('$2b$') or stored_hash.startswith('$2a$'):
            
            # Contraseña está hasheada, usar bcrypt para verificar
            pwd_bytes = user_pwd.encode('utf-8')
            hash_bytes = stored_hash.encode('utf-8')
            return bcrypt.checkpw(pwd_bytes, hash_bytes)
        else:
            return user_pwd == stored_hash
            
    except:
        return False

# Generar sal aleatoria
def generate_salt(length=32):
    return secrets.token_hex(length)

# Verificar formato de contraseña almacenada
def check_password_format(stored_pwd):
    if not stored_pwd:
        return 'empty'
    
    if stored_pwd.startswith('$2b$') or stored_pwd.startswith('$2a$'):
        return 'secure'
    else:
        return 'plain'
