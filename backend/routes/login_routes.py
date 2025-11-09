from flask import Blueprint, render_template, request
from controllers.login_controller import iniciar_sesion

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return iniciar_sesion()
    return render_template('auth/login.html')

@login_bp.route('/logout')
def logout():
    from flask import session, redirect, url_for
    session.clear()
    return redirect(url_for('general_bp.inicio'))