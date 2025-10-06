# Controlador de newsletter - suscripciones y desuscripciones
import re
from models.newsletter_model import subscribe_to_newsletter, unsubscribe_from_newsletter
from services.email_service import EmailService

class NewsletterController:
    
    # Suscribir email al newsletter
    @staticmethod
    def subscribe_user(email):
        if not email or not email.strip():
            return False, 'El correo electrónico es obligatorio'
        
        email = email.strip().lower()
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, 'El formato del correo electrónico no es válido'
        
        success, message = subscribe_to_newsletter(email)
        
        if success:
            try:
                EmailService.send_newsletter_confirmation(email)
            except:
                pass
        
        return success, message
    
    # Desuscribir email del newsletter
    @staticmethod
    def unsubscribe_user(email):
        
        if not email or not email.strip():
            return False, 'El correo electrónico es obligatorio'
        
        email = email.strip().lower()
        
        return unsubscribe_from_newsletter(email)