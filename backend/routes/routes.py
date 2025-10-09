# Rutas principales de la aplicación

from flask import Blueprint, render_template, request, flash, redirect, url_for
from controllers.newsletter_controller import NewsletterController

main_bp = Blueprint('main', __name__)

# Página de inicio
@main_bp.route('/')
def inicio():
    return render_template('pages/home.html')

# Página de traducción señas a texto
@main_bp.route('/senas')
def senas():
    return render_template('features/translator/sign-to-text.html')

# Página de traducción texto a señas
@main_bp.route('/texto')
def texto():
    return render_template('features/translator/text-to-sign.html')

# Página del menú
@main_bp.route('/menu')
def menu():
    return render_template('base/layout.html')

# Suscripción al newsletter
@main_bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    email = request.form.get('email')
    success, message = NewsletterController.subscribe_user(email)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    # Redirigir a la página anterior o inicio
    return redirect(request.referrer or url_for('main.inicio'))

# Páginas legales
@main_bp.route('/terminos')
def terminos():
    return render_template('legal/terms-conditions.html')

@main_bp.route('/privacidad')
def privacidad():
    return render_template('legal/privacy-policy.html')

# Endpoint para ver información de sesión (debug)
@main_bp.route('/debug/session')
def debug_session():
    from flask import session, jsonify
    from controllers.auth_controller import AuthController
    
    current_user = AuthController.get_current_user()
    anonymous_session = AuthController.get_anonymous_session_info()
    
    return jsonify({
        'authenticated': current_user is not None,
        'user': current_user['nombre'] if current_user else None,
        'anonymous_session_id': session.get('anonymous_session_id'),
        'anonymous_session_data': anonymous_session,
        'session_keys': list(session.keys())
    })





