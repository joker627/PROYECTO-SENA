# Servicio de email SMTP para PROYECTO-SENA
# Envía emails de bienvenida, cambio de contraseña, etc.
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime

try:
    from config.settings import (
        SMTP_SERVER, SMTP_PORT, SMTP_USE_TLS,
        SMTP_USERNAME, SMTP_PASSWORD,
        MAIL_DEFAULT_SENDER, MAIL_DEFAULT_SENDER_NAME,
        DEBUG
    )
except ImportError:
    # Configuración por defecto
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USE_TLS = True
    SMTP_USERNAME = None
    SMTP_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    MAIL_DEFAULT_SENDER_NAME = 'PROYECTO-SENA'
    DEBUG = True

class SMTPEmailService:
    # Servicio base de SMTP
    
    @staticmethod
    def _validate_config():
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            return False, "Configuración SMTP incompleta. Revisa SMTP_USERNAME y SMTP_PASSWORD en settings.py"
        
        if SMTP_PASSWORD == 'tu_contraseña_de_aplicacion':
            return False, "Debes configurar tu contraseña real en SMTP_PASSWORD"
            
        return True, "Configuración OK"
    
    # Método base para enviar emails
    @staticmethod
    def _send_email(to_email, to_name, subject, html_content, text_content=None):
        config_ok, config_msg = SMTPEmailService._validate_config()
        if not config_ok:
            return False, config_msg
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = formataddr((MAIL_DEFAULT_SENDER_NAME, MAIL_DEFAULT_SENDER))
            msg['To'] = formataddr((to_name, to_email))
            msg['Reply-To'] = MAIL_DEFAULT_SENDER
            
            if text_content:
                part1 = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part2)
            
            if SMTP_USE_TLS:
                context = ssl.create_default_context()
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls(context=context)
            else:
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(MAIL_DEFAULT_SENDER, to_email, msg.as_string())
            server.quit()
            
            return True, "¡Correo enviado exitosamente!"
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "Error de autenticación SMTP. Verifica username/password o usa contraseña de aplicación"
            return False, error_msg
            
        except smtplib.SMTPRecipientsRefused:
            error_msg = f"Dirección de correo rechazada: {to_email}"
            return False, error_msg
            
        except smtplib.SMTPServerDisconnected:
            error_msg = "Desconectado del servidor SMTP. Verifica configuración de servidor/puerto"
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Error enviando correo: {str(e)}"
            return False, error_msg
    
    # Email de bienvenida personalizado
    @staticmethod
    def send_welcome_email(user_name, user_email):
        subject = "¡Bienvenido a PROYECTO-SENA!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bienvenido a PROYECTO-SENA</title>
        </head>
        <body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                        🌟 ¡Bienvenido a PROYECTO-SENA!
                    </h1>
                    <p style="margin: 15px 0 0; font-size: 18px; opacity: 0.95; font-weight: 300;">
                        Tu plataforma de tecnología de señas
                    </p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h2 style="color: #2d3748; font-size: 24px; margin: 0 0 10px;">
                            ¡Hola {user_name}! 👋
                        </h2>
                        <p style="color: #718096; font-size: 16px; margin: 0;">
                            {datetime.now().strftime('%d de %B de %Y')}
                        </p>
                    </div>
                    
                    <p style="color: #4a5568; font-size: 16px; line-height: 1.7; margin: 0 0 25px; text-align: center;">
                        Soy <strong>Manuel</strong>, administrador de <strong>PROYECTO-SENA</strong>. 
                        Es un placer darte la bienvenida personalmente a nuestra plataforma 
                        de tecnología de señas. ¡Estamos emocionados de tenerte con nosotros!
                    </p>
                    
                    <!-- Features Box -->
                    <div style="background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); border-radius: 12px; padding: 25px; margin: 30px 0; border-left: 4px solid #667eea;">
                        <h3 style="color: #2d3748; font-size: 18px; margin: 0 0 20px; display: flex; align-items: center;">
                            🚀 ¿Qué puedes hacer en PROYECTO-SENA?
                        </h3>
                        <div style="display: grid; gap: 12px;">
                            <div style="display: flex; align-items: center; color: #4a5568;">
                                <span style="margin-right: 12px; font-size: 18px;">🤟</span>
                                <span>Traducción avanzada de señas</span>
                            </div>
                            <div style="display: flex; align-items: center; color: #4a5568;">
                                <span style="margin-right: 12px; font-size: 18px;">💬</span>
                                <span>Comunicación inclusiva y accesible</span>
                            </div>
                            <div style="display: flex; align-items: center; color: #4a5568;">
                                <span style="margin-right: 12px; font-size: 18px;">🎓</span>
                                <span>Aprendizaje interactivo personalizado</span>
                            </div>
                            <div style="display: flex; align-items: center; color: #4a5568;">
                                <span style="margin-right: 12px; font-size: 18px;">🌐</span>
                                <span>Herramientas tecnológicas innovadoras</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Call to Action -->
                    <div style="text-align: center; margin: 35px 0;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; display: inline-block;">
                            <h4 style="margin: 0 0 10px; font-size: 16px;">¡Comienza tu experiencia!</h4>
                            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Explora todas las funcionalidades disponibles</p>
                        </div>
                    </div>
                    
                    <!-- Personal Message -->
                    <div style="background: #f0fff4; border: 1px solid #9ae6b4; border-radius: 8px; padding: 20px; margin: 25px 0;">
                        <p style="color: #22543d; margin: 0; font-size: 14px; line-height: 1.6; text-align: center;">
                            💡 <strong>¿Tienes alguna pregunta o sugerencia?</strong><br>
                            No dudes en responder este correo. Como administrador, 
                            personalmente me encargo de ayudar a todos nuestros usuarios.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #f8fafc; padding: 25px 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 13px; margin: 0 0 8px;">
                        © 2024 PROYECTO-SENA • Enviado con ❤️ por Manuel Admin
                    </p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">
                        📧 Enviado a: {user_email} • Responde para contacto directo
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        ¡Bienvenido a PROYECTO-SENA, {user_name}!
        
        Soy Manuel, administrador de PROYECTO-SENA, y es un placer darte 
        la bienvenida personalmente a nuestra plataforma de tecnología de señas.
        
        ¿Qué puedes hacer en PROYECTO-SENA?
        🤟 Traducción avanzada de señas
        💬 Comunicación inclusiva y accesible  
        🎓 Aprendizaje interactivo personalizado
        🌐 Herramientas tecnológicas innovadoras
        
        ¡Comienza a explorar todas las funcionalidades!
        
        Si tienes alguna pregunta o sugerencia, no dudes en responder 
        este correo. Como administrador, personalmente me encargo de 
        ayudar a todos nuestros usuarios.
        
        ¡Bienvenido a bordo!
        
        Saludos cordiales,
        Manuel - Administrador de PROYECTO-SENA
        
        ---
        © 2024 PROYECTO-SENA
        Enviado a: {user_email}
        """
        
        return SMTPEmailService._send_email(user_email, user_name, subject, html_content, text_content)
    
    @staticmethod
    def send_password_change_notification(user_name, user_email):
        """Envía notificación de cambio de contraseña"""
        
        subject = "Contraseña actualizada - PROYECTO-SENA"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                
                <div style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 600;">🔒 Contraseña Actualizada</h1>
                    <p style="margin: 10px 0 0; opacity: 0.9;">PROYECTO-SENA</p>
                </div>
                
                <div style="padding: 35px 30px;">
                    <h2 style="color: #2d3748; font-size: 22px; margin: 0 0 20px;">Hola {user_name},</h2>
                    
                    <p style="color: #4a5568; line-height: 1.7; font-size: 16px; margin: 0 0 25px;">
                        Tu contraseña ha sido <strong>actualizada exitosamente</strong> en PROYECTO-SENA 
                        el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}.
                    </p>
                    
                    <div style="background: #f0fff4; border-left: 4px solid #48bb78; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <p style="color: #22543d; margin: 0; font-weight: 600;">
                            ✅ Tu cuenta está segura y protegida
                        </p>
                        <p style="color: #276749; margin: 8px 0 0; font-size: 14px;">
                            Puedes acceder normalmente con tu nueva contraseña.
                        </p>
                    </div>
                    
                    <div style="background: #fff5f5; border-left: 4px solid #f56565; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <p style="color: #742a2a; margin: 0; font-weight: 600;">
                            ⚠️ ¿No fuiste tú?
                        </p>
                        <p style="color: #9b2c2c; margin: 8px 0 0; font-size: 14px;">
                            Si NO realizaste este cambio, contacta inmediatamente 
                            respondiendo este correo o contactando al administrador.
                        </p>
                    </div>
                </div>
                
                <div style="background: #f8fafc; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 12px; margin: 0;">
                        © 2024 PROYECTO-SENA • Enviado a {user_email}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Contraseña Actualizada - PROYECTO-SENA
        
        Hola {user_name},
        
        Tu contraseña ha sido actualizada exitosamente en PROYECTO-SENA 
        el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}.
        
        ✅ Tu cuenta está segura y protegida.
        Puedes acceder normalmente con tu nueva contraseña.
        
        ⚠️ ¿No fuiste tú?
        Si NO realizaste este cambio, contacta inmediatamente 
        respondiendo este correo.
        
        Saludos,
        Manuel - Admin PROYECTO-SENA
        """
        
        return SMTPEmailService._send_email(user_email, user_name, subject, html_content, text_content)
    
    @staticmethod
    def send_account_deleted_notification(user_name, user_email):
        """Envía notificación de cuenta eliminada"""
        
        subject = "Cuenta eliminada - PROYECTO-SENA"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                
                <div style="background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%); color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 600;">👋 Hasta pronto</h1>
                    <p style="margin: 10px 0 0; opacity: 0.9;">PROYECTO-SENA</p>
                </div>
                
                <div style="padding: 35px 30px;">
                    <h2 style="color: #2d3748; font-size: 22px; margin: 0 0 20px;">Hasta pronto, {user_name}</h2>
                    
                    <p style="color: #4a5568; line-height: 1.7; font-size: 16px; margin: 0 0 25px;">
                        Tu cuenta en <strong>PROYECTO-SENA</strong> ha sido eliminada exitosamente 
                        el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}.
                    </p>
                    
                    <p style="color: #4a5568; line-height: 1.7; font-size: 16px; margin: 0 0 25px;">
                        Lamentamos verte partir. Ha sido un placer tenerte como parte 
                        de nuestra comunidad de tecnología de señas.
                    </p>
                    
                    <div style="background: #fff5f5; border-left: 4px solid #f56565; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <p style="color: #742a2a; margin: 0 0 10px; font-weight: 600;">
                            🗑️ Datos eliminados de forma segura
                        </p>
                        <p style="color: #9b2c2c; margin: 0; font-size: 14px;">
                            Todos tus datos personales han sido eliminados permanentemente 
                            de nuestros servidores siguiendo las mejores prácticas de privacidad.
                        </p>
                    </div>
                    
                    <div style="background: #f0fff4; border-left: 4px solid #48bb78; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <p style="color: #22543d; margin: 0 0 10px; font-weight: 600;">
                            🚪 ¿Cambias de opinión?
                        </p>
                        <p style="color: #276749; margin: 0; font-size: 14px;">
                            Si en el futuro deseas volver, siempre serás bienvenido. 
                            Puedes registrarte nuevamente cuando gustes.
                        </p>
                    </div>
                </div>
                
                <div style="background: #f8fafc; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 12px; margin: 0 0 5px;">
                        Gracias por haber sido parte de PROYECTO-SENA
                    </p>
                    <p style="color: #a0aec0; font-size: 11px; margin: 0;">
                        © 2024 PROYECTO-SENA
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Cuenta Eliminada - PROYECTO-SENA
        
        Hasta pronto, {user_name}
        
        Tu cuenta en PROYECTO-SENA ha sido eliminada exitosamente 
        el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}.
        
        Lamentamos verte partir. Ha sido un placer tenerte como parte 
        de nuestra comunidad de tecnología de señas.
        
        🗑️ Datos eliminados de forma segura
        Todos tus datos personales han sido eliminados permanentemente 
        siguiendo las mejores prácticas de privacidad.
        
        🚪 ¿Cambias de opinión?
        Si en el futuro deseas volver, siempre serás bienvenido. 
        Puedes registrarte nuevamente cuando gustes.
        
        Gracias por haber sido parte de PROYECTO-SENA.
        
        Hasta pronto,
        Manuel - Admin PROYECTO-SENA
        """
        
        return SMTPEmailService._send_email(user_email, user_name, subject, html_content, text_content)
    
    @staticmethod
    def send_newsletter_confirmation(user_email):
        """Envía confirmación de suscripción al newsletter"""
        
        subject = "¡Bienvenido al Newsletter de PROYECTO-SENA!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 600;">📧 ¡Suscripción Confirmada!</h1>
                    <p style="margin: 10px 0 0; opacity: 0.9;">PROYECTO-SENA Newsletter</p>
                </div>
                
                <div style="padding: 35px 30px;">
                    <h2 style="color: #2d3748; font-size: 22px; margin: 0 0 20px;">¡Gracias por suscribirte!</h2>
                    
                    <p style="color: #4a5568; line-height: 1.7; font-size: 16px; margin: 0 0 25px;">
                        Te has suscrito exitosamente al newsletter de <strong>PROYECTO-SENA</strong>. 
                        Recibirás nuestras últimas noticias, actualizaciones y contenido exclusivo.
                    </p>
                    
                    <div style="background: #f0fff4; border-left: 4px solid #48bb78; padding: 20px; margin: 25px 0; border-radius: 4px;">
                        <h3 style="color: #22543d; margin: 0 0 15px; font-size: 16px;">📬 ¿Qué recibirás?</h3>
                        <ul style="color: #276749; margin: 0; padding-left: 20px;">
                            <li>Actualizaciones del software</li>
                            <li>Nuevas funcionalidades</li>
                            <li>Tips de accesibilidad</li>
                            <li>Noticias de tecnología inclusiva</li>
                        </ul>
                    </div>
                    
                    <div style="background: #fff5f5; border-left: 4px solid #f56565; padding: 15px; margin: 25px 0; border-radius: 4px;">
                        <p style="color: #742a2a; margin: 0; font-size: 14px;">
                            💡 <strong>Nota:</strong> Puedes desuscribirte en cualquier momento 
                            respondiendo este correo con "DESUSCRIBIR".
                        </p>
                    </div>
                </div>
                
                <div style="background: #f8fafc; padding: 20px 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 12px; margin: 0 0 5px;">
                        © 2024 PROYECTO-SENA • Enviado a {user_email}
                    </p>
                    <p style="color: #a0aec0; font-size: 11px; margin: 0;">
                        Manuel - Admin PROYECTO-SENA
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        ¡Suscripción Confirmada! - PROYECTO-SENA Newsletter
        
        ¡Gracias por suscribirte!
        
        Te has suscrito exitosamente al newsletter de PROYECTO-SENA. 
        Recibirás nuestras últimas noticias, actualizaciones y contenido exclusivo.
        
        📬 ¿Qué recibirás?
        - Actualizaciones del software
        - Nuevas funcionalidades  
        - Tips de accesibilidad
        - Noticias de tecnología inclusiva
        
        💡 Nota: Puedes desuscribirte en cualquier momento 
        respondiendo este correo con "DESUSCRIBIR".
        
        Saludos,
        Manuel - Admin PROYECTO-SENA
        
        ---
        © 2024 PROYECTO-SENA
        Enviado a: {user_email}
        """
        
        return SMTPEmailService._send_email(user_email, "Suscriptor", subject, html_content, text_content)


# Servicio de email principal
class EmailService:
    
    # Email de bienvenida
    @staticmethod
    def send_welcome_email(user_name, user_email):
        if DEBUG:
            return True, "Correo de bienvenida simulado (modo desarrollo)"
        else:
            try:
                result = SMTPEmailService.send_welcome_email(user_name, user_email)
                return result
            except Exception as e:
                return False, f"Error enviando email: {e}"
    
    # Notificación de cambio de contraseña
    @staticmethod
    def send_password_change_notification(user_name, user_email):
        if DEBUG:
            return True, "Notificación de contraseña simulada (modo desarrollo)"
        else:
            return SMTPEmailService.send_password_change_notification(user_name, user_email)
    
    # Notificación de cuenta eliminada
    @staticmethod
    def send_account_deleted_notification(user_name, user_email):
        if DEBUG:
            return True, "Notificación de eliminación simulada (modo desarrollo)"
        else:
            return SMTPEmailService.send_account_deleted_notification(user_name, user_email)
    
    # Confirmación de suscripción al newsletter
    @staticmethod
    def send_newsletter_confirmation(user_email):
        if DEBUG:
            return True, "Confirmación newsletter simulada (modo desarrollo)"
        else:
            return SMTPEmailService.send_newsletter_confirmation(user_email)
