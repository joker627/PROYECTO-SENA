from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def inicio():
    from flask import session
    return render_template('index.html', user=session.get('user'))

@main_bp.route('/senas')
def senas():
    from flask import session
    return render_template('senas.html', user=session.get('user'))

@main_bp.route('/texto')
def texto():
    from flask import session
    return render_template('texto.html', user=session.get('user'))

