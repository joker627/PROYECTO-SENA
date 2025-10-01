from flask import Blueprint, render_template

# Se crea el blueprint principal para las rutas
main_bp = Blueprint('main', __name__)

# Ruta de inicio, renderiza la página principal
@main_bp.route('/')
def inicio():
    return render_template('index.html')

# Ruta para la página de señas
@main_bp.route('/senas')
def senas():
    return render_template('senas.html')

# Ruta para la página de texto
@main_bp.route('/texto')
def texto():
    return render_template('texto.html')

# Ruta para la página del menú
@main_bp.route('/menu')
def menu():
    return render_template('menu.html')

# Rutas para páginas legales

@main_bp.route('/terminos')
def terminos():
    return render_template('legal/terminos_y_condiciones.html')

@main_bp.route('/privacidad')
def privacidad():
    return render_template('legal/politica_y_privacidad.html')

@main_bp.route('/cookies')
def cookies():
    return render_template('legal/cookies.html')

@main_bp.route('/licencias')
def licencias():
    return render_template('legal/licencias.html')

@main_bp.route('/accesibilidad')
def accesibilidad():
    return render_template('legal/accesibilidad.html')




