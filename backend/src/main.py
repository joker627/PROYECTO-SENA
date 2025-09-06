# Servidor de desarrollo Flask para servir frontend en entorno local
from flask import Flask, render_template
from datetime import datetime


def create_app():
    """
    Crea y configura la aplicación Flask para desarrollo.

    Notas rápidas:
    - Las carpetas de `static` y `templates` apuntan al frontend del repo.
    - Para producción conviene usar un WSGI (gunicorn/uwsgi) y servir
    los archivos estáticos desde un servidor web.
    """
    app = Flask(__name__, 
        static_folder="../../frontend/static", 
        template_folder="../../frontend/templates")

    # Ruta principal: aquí puedes cambiar la plantilla base si lo necesitas
    @app.route('/')
    def home():
        # Rinde la plantilla principal (`menu.html` muestra el header+footer)
        return render_template('index.html')

    # Inyecta el año actual en todas las plantillas para evitar repetirlo
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    return app

# Esto iniciará el servidor de desarrollo en http://127.0.0.1:5000
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
