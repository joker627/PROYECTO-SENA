import bcrypt

def hash_password(password: str) -> str:
    """Convierte una contraseña en texto plano a hash bcrypt"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(password_plain: str, password_hash: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    try:
        return bcrypt.checkpw(password_plain.encode('utf-8'), password_hash.encode('utf-8'))
    except:
        return False

# Ejemplo de uso
if __name__ == "__main__":
    # Contraseña original
    password = "miguel"
    
    # Hashear la contraseña
    hashed_password = hash_password(password)
    print(f"Contraseña hasheada: {hashed_password}")
    
    # Verificar contraseña correcta
    is_correct = verify_password("miguel", hashed_password)
    print(f"Contraseña correcta: {is_correct}")
    
    # Verificar contraseña incorrecta
    is_correct_wrong = verify_password("contraseña_equivocada", hashed_password)
    print(f"Contraseña incorrecta: {is_correct_wrong}")
    
    # Ejemplo práctico de registro y login
    print("\n--- Simulación de registro y login ---")
    
    # Registro: el usuario crea una cuenta
    user_password = "clave_super_segura"
    stored_hash = hash_password(user_password)
    print(f"Registro: Hash almacenado en BD -> {stored_hash[:50]}...")
    
    # Login: el usuario intenta acceder
    login_attempt = "clave_super_segura"
    if verify_password(login_attempt, stored_hash):
        print("✅ Login exitoso!")
    else:
        print("❌ Contraseña incorrecta")