from config.db import get_db_connection

# Funciones para interactuar con la tabla de usuarios
def get_user_by_username(username):
    with get_db_connection() as conn:
        with conn.cursor() as cursor: 
            cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
            return cursor.fetchone()


# Validar usuario
def validate_user(username, password):
	user = get_user_by_username(username)
	if user and user['password'] == password:
		return user
	return None

# Registrar nuevo usuario
def register_user(username, password, email):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error registering user: {e}")
                return False
