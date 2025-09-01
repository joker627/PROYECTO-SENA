from flask import Flask, render_template

# Crear la aplicación Flask y configurar las carpetas del frontend
app = Flask(__name__, 
    static_folder="../../frontend/static", 
    template_folder="../../frontend/templates")

# Ruta principal que muestra el index.html
@app.route('/')
def home():
    return render_template('index.html')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')