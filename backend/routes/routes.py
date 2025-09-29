from flask import Blueprint, render_template

# Se crea el blueprint principal para las rutas
main_bp = Blueprint('main', __name__)

# Ruta de inicio, renderiza la página principal
@main_bp.route('/')
def inicio():
    from flask import session
    return render_template('index.html', user=session.get('user'))

# Ruta para la página de señas
@main_bp.route('/senas')
def senas():
    from flask import session
    return render_template('senas.html', user=session.get('user'))

# Ruta para la página de texto
@main_bp.route('/texto')
def texto():
    from flask import session
    return render_template('texto.html', user=session.get('user'))


@main_bp.route("/page1")
def page1():
     from flask import session
     return render_template("politicas/page1.html")



@main_bp.route("/page2")
def page2():
     from flask import session
     return render_template("terminos/page2.html")



