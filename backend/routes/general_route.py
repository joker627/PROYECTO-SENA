

from flask import Blueprint, render_template

    
general_bp = Blueprint('general_bp', __name__)

@general_bp.route('/')
def inicio():
    return render_template("pages/index.html")


@general_bp.route('/nosotros')
def nosotros():
    return render_template("pages/nosotros.html")

@general_bp.route('/tutoriales')
def tutoriales():
    return render_template("pages/tutoriales.html")