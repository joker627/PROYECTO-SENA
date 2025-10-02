# ===== UTILIDADES PARA CONTRASEÑAS SEGURAS =====
#
# Funciones para manejar contraseñas de forma segura:
# - create_hash_pwd() -> Convertir contraseña normal a segura
# - check_pwd() -> Verificar si contraseña es correcta
# - check_pwd_type() -> Decir si contraseña es segura o no
# - gen_random_code() -> Crear códigos aleatorios
#

import hashlib
import secrets
import bcrypt


def create_hash_pwd(pwd_text):
    """
    Convierte contraseña normal en hash seguro
    
    Ejemplo: "mipass123" -> "$2b$12$ABC..."
    
    Args:
        pwd_text: Contraseña que escribió el usuario
        
    Returns:
        Versión segura de la contraseña para base de datos
    """
    # Convertir contraseña a formato de bytes
    pwd_bytes = pwd_text.encode('utf-8')
    
    # Crear sal única para seguridad extra
    salt = bcrypt.gensalt()
    
    # Crear hash seguro combinando contraseña + sal
    secure_hash = bcrypt.hashpw(pwd_bytes, salt)
    
    # Convertir de vuelta a texto para guardar
    return secure_hash.decode('utf-8')


def check_pwd(user_pwd, stored_hash):
    """
    Verificar si la contraseña que escribió el usuario es correcta
    
    Ejemplo: check_pwd("mipass123", "$2b$12$ABC...")
    
    Args:
        user_pwd: Lo que escribió el usuario en el login
        stored_hash: Contraseña segura de la base de datos
        
    Returns:
        True si la contraseña es correcta, False si no
    """
    try:
        # Verificar que tengamos datos para comparar
        if not user_pwd or not stored_hash:
            return False
        
        # Verificar si la contraseña está hasheada (segura) o texto plano
        if stored_hash.startswith('$2b$') or stored_hash.startswith('$2a$'):
            # Contraseña está hasheada con bcrypt (seguro)
            pwd_bytes = user_pwd.encode('utf-8')
            hash_bytes = stored_hash.encode('utf-8')
            return bcrypt.checkpw(pwd_bytes, hash_bytes)
        
        else:
            # Contraseña está en texto plano (no seguro, pero funciona)
            return user_pwd == stored_hash
            
    except:
        # Si algo sale mal, mejor decir que no coincide
        return False


def gen_random_code(length=32):
    """
    Crear código aleatorio para hacer contraseñas más seguras
    
    Args:
        length: Qué tan largo quieres el código (por defecto 32)
        
    Returns:
        Código aleatorio como "a1b2c3d4..."
    """
    return secrets.token_hex(length)


def check_pwd_type(stored_pwd):
    """
    Decir qué tipo de contraseña está guardada en la base de datos
    
    Args:
        stored_pwd: Contraseña de la base de datos
        
    Returns:
        "secure" si está hasheada, "plain" si no, "empty" si no hay nada
    """
    if not stored_pwd:
        return 'empty'
    
    if stored_pwd.startswith('$2b$') or stored_pwd.startswith('$2a$'):
        return 'secure'
    else:
        return 'plain'


# ===== ALIAS CORTOS PARA USO FÁCIL =====
# (Nombres fáciles de recordar)

# Alias cortos y fáciles
hash_password = create_hash_pwd
verify_password = check_pwd  
generate_salt = gen_random_code
check_password_format = check_pwd_type
