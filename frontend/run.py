"""
Sign Technology - Frontend Flask
Sistema de gestión para traducción de Lengua de Señas Colombiana
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import requests
import math
import os
import glob
import time

app = Flask(__name__)
app.secret_key = 'sign-technology-2026-secret-key-change-in-production'
API_URL = 'http://localhost:8000'


def login_required(f):
    """Decorador para rutas que requieren autenticación."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated


# ══════════════════════════════════════════════════════════════════════════════
# RUTAS PÚBLICAS
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/nosotros')
def nosotros():
    return render_template("pages/nosotros.html")

@app.route('/tutoriales')
def tutoriales():
    return render_template("pages/tutoriales.html")


# ══════════════════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/login', methods=['GET'])
def login_page():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template("pages/login.html")

@app.route('/login', methods=['POST'])
def login_post():
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    remember = request.form.get('remember') == 'on'
    
    if not correo or not contrasena:
        flash('Completa todos los campos', 'error')
        return redirect(url_for('login_page'))
    
    try:
        response = requests.post(f'{API_URL}/api/v1/auth/login', json={'correo': correo, 'contrasena': contrasena}, timeout=10)
        data = response.json()

        if response.status_code == 200:
            session['user'] = data.get('user')
            session['token'] = data.get('access_token')
            session.permanent = remember
            flash(f"¡Bienvenido {session['user'].get('nombre_completo', 'Usuario')}!", 'success')
            return redirect(url_for('dashboard') if session['user'].get('rol') in ['admin', 'Administrador'] else url_for('inicio'))
        else:
            flash(data.get('detail', 'Credenciales inválidas'), 'error')
            return redirect(url_for('login_page'))
            
    except requests.exceptions.ConnectionError:
        flash('Error de conexión con el servidor', 'error')
        return redirect(url_for('login_page'))
    except Exception:
        flash('Error al procesar la solicitud', 'error')
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('inicio'))


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    stats = {}
    try:
        response = requests.get(f'{API_URL}/api/v1/estadisticas/', timeout=5)
        if response.status_code == 200:
            stats = response.json()
    except:
        flash('Error al cargar estadísticas', 'error')
    return render_template("pages/dashboard.html", user=session.get('user'), stats=stats)


# ══════════════════════════════════════════════════════════════════════════════
# USUARIOS
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/usuarios')
@login_required
def usuarios():
    page = request.args.get('page', 1, type=int)
    limit = 10
    query = request.args.get('query')
    rol = request.args.get('rol')
    estado = request.args.get('estado')
    
    params = {'skip': (page - 1) * limit, 'limit': limit}
    if query: params['query'] = query
    if rol: params['rol'] = rol
    if estado: params['estado'] = estado
    
    users, total_pages = [], 1
    stats = {"total": 0, "administradores": 0, "colaboradores": 0, "activos": 0}
    
    try:
        response = requests.get(f'{API_URL}/api/v1/usuarios/', params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            users = data.get('data', [])
            total_pages = math.ceil(data.get('total', 0) / limit)
            
        stats_response = requests.get(f'{API_URL}/api/v1/usuarios/stats', timeout=3)
        if stats_response.status_code == 200:
            stats = stats_response.json()
    except:
        flash('Error al cargar usuarios', 'error')
        
    return render_template("pages/usuarios.html", user=session.get('user'), users=users, page=page, total_pages=total_pages, stats=stats, filter_query=query, filter_rol=rol, filter_estado=estado)

@app.route('/usuarios/create', methods=['POST'])
@login_required
def create_usuario():
    datos = {
        "nombre_completo": request.form.get('nombre_completo'),
        "correo": request.form.get('correo'),
        "contrasena": request.form.get('contrasena'),
        "tipo_documento": request.form.get('tipo_documento'),
        "numero_documento": request.form.get('numero_documento'),
        "id_rol": int(request.form.get('id_rol')) if request.form.get('id_rol') else 2,
        "estado": request.form.get('estado', 'activo')
    }
    
    try:
        response = requests.post(f'{API_URL}/api/v1/usuarios/', json=datos, timeout=5)
        if response.status_code == 200:
            flash('Usuario creado correctamente', 'success')
        else:
            flash(f"Error: {response.json().get('detail', 'Error desconocido')}", 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/update', methods=['POST'])
@login_required
def update_usuario():
    id_usuario = request.form.get('id_usuario')
    datos = {
        "nombre_completo": request.form.get('nombre_completo'),
        "correo": request.form.get('correo'),
        "id_rol": int(request.form.get('id_rol')) if request.form.get('id_rol') else None,
        "estado": request.form.get('estado')
    }
    
    try:
        response = requests.put(f'{API_URL}/api/v1/usuarios/{id_usuario}', json=datos, timeout=5)
        flash('Usuario actualizado' if response.status_code == 200 else 'Error al actualizar', 'success' if response.status_code == 200 else 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/delete', methods=['POST'])
@login_required
def delete_usuario():
    id_usuario = request.form.get('id_usuario')
    try:
        response = requests.delete(f'{API_URL}/api/v1/usuarios/{id_usuario}', timeout=5)
        flash('Usuario eliminado' if response.status_code == 200 else 'Error al eliminar', 'success' if response.status_code == 200 else 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('usuarios'))


# ══════════════════════════════════════════════════════════════════════════════
# CONTRIBUCIONES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/contribuciones')
@login_required
def contribuciones():
    estado = request.args.get('estado')
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    limit = 10
    
    params = {'skip': (page - 1) * limit, 'limit': limit}
    if estado and estado != 'todos': params['estado'] = estado
    if query: params['query'] = query
        
    contribuciones_list, total_pages = [], 1
    stats = {"total": 0, "pendientes": 0, "aprobadas": 0}
        
    try:
        response = requests.get(f'{API_URL}/api/v1/contribuciones/', params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            contribuciones_list = data.get('data', [])
            total_pages = math.ceil(data.get('total', 0) / limit)
            
        stats_response = requests.get(f'{API_URL}/api/v1/contribuciones/stats', timeout=3)
        if stats_response.status_code == 200:
            stats = stats_response.json()
    except:
        flash('Error al cargar contribuciones', 'error')
        
    return render_template("pages/contribuciones.html", user=session.get('user'), contribuciones=contribuciones_list, active_filter=estado or 'todos', filter_query=query, page=page, total_pages=total_pages, stats=stats)

@app.route('/contribuciones/update', methods=['POST'])
@login_required
def update_contribucion():
    id_contribucion = request.form.get('id_contribucion')
    nuevo_estado = request.form.get('nuevo_estado')
    observaciones = request.form.get('observaciones')
    
    params = {'estado': nuevo_estado}
    if observaciones: params['observaciones'] = observaciones
    
    try:
        response = requests.put(f'{API_URL}/api/v1/contribuciones/{id_contribucion}/estado', params=params, timeout=5)
        flash(f'Contribución {nuevo_estado}' if response.status_code == 200 else 'Error al actualizar', 'success' if response.status_code == 200 else 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('contribuciones'))


# ══════════════════════════════════════════════════════════════════════════════
# REPORTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/reportes')
@login_required
def reportes():
    estado = request.args.get('estado')
    prioridad = request.args.get('prioridad')
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    limit = 10
    
    params = {'skip': (page - 1) * limit, 'limit': limit}
    if estado and estado != 'todos': params['estado'] = estado
    if prioridad and prioridad != 'todas': params['prioridad'] = prioridad
    if query: params['query'] = query

    reports, total_pages = [], 1
    stats = {"total": 0, "pendientes": 0, "en_revision": 0, "alta_prioridad": 0}

    try:
        response = requests.get(f'{API_URL}/api/v1/reportes/', params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            reports = data.get('data', [])
            total_pages = math.ceil(data.get('total', 0) / limit)
            
        stats_response = requests.get(f'{API_URL}/api/v1/reportes/stats', timeout=3)
        if stats_response.status_code == 200:
            stats = stats_response.json()
    except:
        flash('Error al cargar reportes', 'error')
        
    return render_template("pages/reportes.html", user=session.get('user'), reports=reports, filter_estado=estado, filter_prioridad=prioridad, filter_query=query, page=page, total_pages=total_pages, stats=stats)

@app.route('/reportes/update', methods=['POST'])
@login_required
def update_reporte():
    id_reporte = request.form.get('id_reporte')
    params = {}
    if request.form.get('nuevo_estado'): params['estado'] = request.form.get('nuevo_estado')
    if request.form.get('nueva_prioridad'): params['prioridad'] = request.form.get('nueva_prioridad')
    
    try:
        response = requests.put(f'{API_URL}/api/v1/reportes/{id_reporte}/gestion', params=params, timeout=5)
        if response.status_code == 200:
            flash('Reporte actualizado', 'success')
        elif response.status_code == 404:
            flash('Reporte no encontrado', 'error')
        else:
            flash('Error al actualizar', 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('reportes'))

@app.route('/reportes/resolver', methods=['POST'])
@login_required
def resolver_reporte():
    """Resuelve y elimina un reporte de la base de datos."""
    id_reporte = request.form.get('id_reporte')
    
    try:
        response = requests.delete(f'{API_URL}/api/v1/reportes/{id_reporte}', timeout=5)
        flash('Reporte resuelto y eliminado' if response.status_code == 200 else 'Error al resolver', 'success' if response.status_code == 200 else 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('reportes'))


# ══════════════════════════════════════════════════════════════════════════════
# PERFIL
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/perfil')
@login_required
def perfil():
    """Muestra el perfil del usuario actual."""
    user = session.get('user')
    try:
        response = requests.get(f"{API_URL}/api/v1/usuarios/{user.get('id_usuario')}", timeout=5)
        if response.status_code == 200:
            session['user'] = response.json()
            session.modified = True
    except:
        pass
    return render_template("pages/perfil.html", user=session.get('user'))

@app.route('/perfil/update', methods=['POST'])
@login_required
def update_perfil():
    """Actualiza los datos personales del usuario."""
    user = session.get('user')
    datos = {"nombre_completo": request.form.get('nombre_completo')}
    
    try:
        response = requests.put(f"{API_URL}/api/v1/usuarios/{user.get('id_usuario')}", json=datos, timeout=5)
        if response.status_code == 200:
            session['user'] = response.json()
            session.modified = True
            flash('Perfil actualizado', 'success')
        else:
            flash('Error al actualizar', 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('perfil'))

@app.route('/perfil/avatar', methods=['POST'])
@login_required
def update_avatar():
    """Actualiza la imagen de perfil."""
    if 'avatar' not in request.files or request.files['avatar'].filename == '':
        flash('No se seleccionó imagen', 'error')
        return redirect(url_for('perfil'))
        
    file = request.files['avatar']
    user = session.get('user')
    id_usuario = user.get('id_usuario')
    
    upload_dir = os.path.join(app.root_path, 'static', 'img', 'profiles')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Eliminar fotos anteriores
    for old_photo in glob.glob(os.path.join(upload_dir, f"user_{id_usuario}_*")):
        try:
            os.remove(old_photo)
        except:
            pass
    
    # Guardar nueva foto
    extension = os.path.splitext(file.filename)[1].lower()
    filename = f"user_{id_usuario}_{int(time.time())}{extension}"
    
    try:
        file.save(os.path.join(upload_dir, filename))
        response = requests.put(f'{API_URL}/api/v1/usuarios/{id_usuario}', json={"imagen_perfil": filename}, timeout=5)
        
        if response.status_code == 200:
            session['user'] = response.json()
            session.modified = True
            flash('Imagen actualizada', 'success')
        else:
            flash('Error al registrar imagen', 'error')
    except:
        flash('Error al guardar imagen', 'error')
    return redirect(url_for('perfil'))

@app.route('/perfil/password', methods=['POST'])
@login_required
def update_password():
    """Cambia la contraseña del usuario."""
    user = session.get('user')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    try:
        # Verificar contraseña actual
        login_response = requests.post(f'{API_URL}/api/v1/auth/login', json={'correo': user.get('correo'), 'contrasena': current_password}, timeout=5)
        
        if login_response.status_code != 200:
            flash('Contraseña actual incorrecta', 'error')
            return redirect(url_for('perfil'))
            
        # Actualizar contraseña
        response = requests.put(f"{API_URL}/api/v1/usuarios/{user.get('id_usuario')}", json={'contrasena': new_password}, timeout=5)
        flash('Contraseña cambiada' if response.status_code == 200 else 'Error al cambiar contraseña', 'success' if response.status_code == 200 else 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('perfil'))


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
