from flask import Flask, render_template

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Ruta principal
@app.route('/')
def index():
    return render_template('base.html')

# Rutas del menú principal
@app.route('/desarrolladores')
def desarrolladores():
    return render_template('base.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('base.html')

@app.route('/servicios')
def servicios():
    return render_template('base.html')

@app.route('/contacto')
def contacto():
    return render_template('base.html')

# Rutas de autenticación
@app.route('/login')
def login():
    return render_template('base.html')

@app.route('/registro')
def registro():
    return render_template('base.html')

@app.route('/logout')
def logout():
    return render_template('base.html')

# Rutas de administrador
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('base.html')

@app.route('/admin/usuarios')
def admin_usuarios():
    return render_template('base.html')

@app.route('/admin/reportes')
def admin_reportes():
    return render_template('base.html')

@app.route('/admin/configuracion')
def admin_configuracion():
    return render_template('base.html')

@app.route('/admin/perfil')
def admin_perfil():
    return render_template('base.html')

# Rutas de colaborador
@app.route('/colaborador/panel')
def colaborador_panel():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
