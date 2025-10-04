from flask import Blueprint, render_template

# Se crea el blueprint principal para las rutas
main_bp = Blueprint('main', __name__)

# Ruta de inicio, renderiza la página principal
@main_bp.route('/')
def inicio():
    return render_template('pages/home.html')

# Ruta para la página de señas
@main_bp.route('/senas')
def senas():
    return render_template('features/translator/sign-to-text.html')

# Ruta para la página de texto
@main_bp.route('/texto')
def texto():
    return render_template('features/translator/text-to-sign.html')

# Ruta para la página del menú
@main_bp.route('/menu')
def menu():
    return render_template('base/layout.html')

# Rutas para páginas legales

@main_bp.route('/terminos')
def terminos():
    return render_template('legal/terms-conditions.html')

@main_bp.route('/privacidad')
def privacidad():
    return render_template('legal/privacy-policy.html')





