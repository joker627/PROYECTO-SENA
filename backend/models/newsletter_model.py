# Modelo de newsletter - BD de suscripciones
from config.db import get_db_connection
import pymysql

# Suscribir email al newsletter
def subscribe_to_newsletter(email):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO newsletter_emails (email) VALUES (%s)"
                cursor.execute(query, (email,))
                connection.commit()
                
        return True, "¡Suscripción exitosa! Recibirás nuestras actualizaciones."
        
    except pymysql.IntegrityError:
        return False, "Este email ya está suscrito a nuestro newsletter."
    except Exception as e:
        return False, f"Error al procesar suscripción: {str(e)}"

# Obtener todos los suscriptores
def get_all_subscribers():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT * FROM newsletter_emails ORDER BY created_at DESC"
                cursor.execute(query)
                subscribers = cursor.fetchall()
                
        return subscribers
    except Exception as e:
        print(f"Error obteniendo suscriptores: {e}")
        return []

# Desuscribir email del newsletter
def unsubscribe_from_newsletter(email):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM newsletter_emails WHERE email = %s"
                cursor.execute(query, (email,))
                
                if cursor.rowcount > 0:
                    connection.commit()
                    return True, "Te has desuscrito correctamente."
                else:
                    return False, "Email no encontrado en nuestras suscripciones."
                    
    except Exception as e:
        return False, f"Error al desuscribir: {str(e)}"