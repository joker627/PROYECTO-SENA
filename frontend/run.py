from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sign-technology-2026-secret-key-change-in-production'

# Configuración de la API
API_URL = 'http://localhost:8000'

# Helper para peticiones con autenticación
def get_auth_headers():
    """Retorna headers con el token de autenticación si existe."""
    token = session.get('token')
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}

def api_request(method, endpoint, **kwargs):
    """Wrapper para peticiones a la API con autenticación automática."""
    headers = kwargs.pop('headers', {})
    headers.update(get_auth_headers())
    
    url = f'{API_URL}{endpoint}'
    response = requests.request(method, url, headers=headers, **kwargs)
    
    # Si retorna 401, limpiar sesión y redirigir
    if response.status_code == 401:
        session.clear()
    
    return response

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def inicio():
    return render_template("/index.html")

@app.route('/nosotros')
def nosotros():
    return render_template("pages/nosotros.html")

@app.route('/tutoriales')
def tutoriales():
    return render_template("pages/tutoriales.html")

@app.route('/login', methods=['GET'])
def login_page():
    # Si ya está logueado, redirigir
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template("pages/login.html")

@app.route('/login', methods=['POST'])
def login_post():
    try:
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        
        if not correo or not contrasena:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('login_page'))
        
        # 1. Llamar a la API de autenticación (FastAPI v1)
        response = requests.post(
            f'{API_URL}/api/v1/auth/login',
            json={'correo': correo, 'contrasena': contrasena},
            timeout=10
        )

        data = response.json()

        if response.status_code == 200:
            # 2. Guardar el token
            token = data.get('access_token')
            session['token'] = token
            
            # 3. Obtener datos del usuario usando el endpoint /me
            try:
                headers = {'Authorization': f'Bearer {token}'}
                user_response = requests.get(
                    f'{API_URL}/api/v1/usuarios/me',
                    headers=headers,
                    timeout=5
                )
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    session['user'] = user_data
                    
                    nombre = user_data.get('nombre_completo', 'Usuario')
                    flash(f"¡Bienvenido {nombre}!", 'success')
                    
                    # Redirigir según el rol
                    rol = user_data.get('id_rol')
                    if rol == 1:  # Admin
                        return redirect(url_for('dashboard'))
                    else:
                        return redirect(url_for('inicio'))
                else:
                    flash('Error al obtener datos del usuario', 'error')
                    session.clear()
                    return redirect(url_for('login_page'))
                    
            except Exception as e:
                print(f"Error obteniendo perfil: {str(e)}")
                flash('Error al cargar datos del usuario', 'error')
                session.clear()
                return redirect(url_for('login_page'))
        else:
            # Intentar obtener mensaje de error de la API
            msg = data.get('detail') if isinstance(data, dict) else 'Credenciales inválidas'
            flash(msg, 'error')
            return redirect(url_for('login_page'))
            
    except requests.exceptions.ConnectionError:
        flash('Error de conexión con el servidor. Verifica que el backend esté ejecutándose.', 'error')
        return redirect(url_for('login_page'))
    except Exception as e:
        print(f"Error en login: {str(e)}")
        flash('Error al procesar la solicitud', 'error')
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('inicio'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = {}
    try:
        response = api_request('GET', '/api/v1/estadisticas/', timeout=5)
        if response.status_code == 200:
            stats = response.json()
    except:
        flash('Error al cargar estadísticas', 'error')
        
    from datetime import datetime
    current_time = datetime.now()
    return render_template("pages/dashboard.html", user=session.get('user'), stats=stats, current_time=current_time)

# --- GESTIÓN DE USUARIOS ---

@app.route('/usuarios')
@login_required
def usuarios():
    """Vista principal de gestión de usuarios con filtros y paginación."""
    page = request.args.get('page', 1, type=int)
    limit = 10
    skip = (page - 1) * limit
    
    # Parámetros de filtrado
    query = request.args.get('query')
    rol = request.args.get('rol')
    estado = request.args.get('estado')
    
    params = {'skip': skip, 'limit': limit}
    if query:
        params['query'] = query
    if rol:
        params['rol'] = rol
    if estado:
        params['estado'] = estado
    
    users = []
    total_pages = 1
    stats = {"total": 0, "administradores": 0, "colaboradores": 0, "activos": 0}
    
    try:
        # Obtener lista de usuarios desde el backend
        response = api_request('GET', '/api/v1/usuarios/', params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            users = data.get('data', [])
            total = data.get('total', 0)
            import math
            total_pages = math.ceil(total / limit)
            
        # Obtener estadísticas de usuarios
        stats_response = api_request('GET', '/api/v1/usuarios/stats', timeout=3)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
    except Exception as e:
        flash('Error al cargar datos de usuarios', 'error')
        
    return render_template("pages/usuarios.html", user=session.get('user'), users=users, page=page, total_pages=total_pages, stats=stats, filter_query=query, filter_rol=rol, filter_estado=estado)

@app.route('/usuarios/create', methods=['POST'])
@login_required
def create_usuario():
    """Procesa la creación de un nuevo usuario."""
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
        # Petición POST al backend para crear el usuario
        response = api_request('POST', '/api/v1/usuarios/', json=datos, timeout=5)
        if response.status_code == 200:
            flash('Usuario creado correctamente', 'success')
        else:
            error_detail = response.json().get('detail', 'Error desconocido')
            flash(f'Error al crear el usuario: {error_detail}', 'error')
    except Exception as e:
        flash('Error de conexión con el servidor', 'error')
        
    return redirect(url_for('usuarios'))

@app.route('/usuarios/update', methods=['POST'])
@login_required
def update_usuario():
    """Procesa la actualización de datos de un usuario."""
    id_usuario = request.form.get('id_usuario')
    datos = {
        "nombre_completo": request.form.get('nombre_completo'),
        "correo": request.form.get('correo'),
        "id_rol": int(request.form.get('id_rol')) if request.form.get('id_rol') else None,
        "estado": request.form.get('estado')
    }
    
    try:
        # Petición PUT al backend para actualizar el usuario
        response = api_request('PUT', f'/api/v1/usuarios/{id_usuario}', json=datos, timeout=5)
        if response.status_code == 200:
            flash('Usuario actualizado correctamente', 'success')
        else:
            flash('Error al actualizar el usuario', 'error')
    except:
        flash('Error de conexión con el servidor', 'error')
        
    return redirect(url_for('usuarios'))

@app.route('/usuarios/delete', methods=['POST'])
@login_required
def delete_usuario():
    """Elimina un usuario del sistema."""
    id_usuario = request.form.get('id_usuario')
    try:
        response = api_request('DELETE', f'/api/v1/usuarios/{id_usuario}', timeout=5)
        if response.status_code == 200:
            flash('Usuario eliminado correctamente', 'success')
        else:
            flash('Error al eliminar usuario', 'error')
    except:
        flash('Error de conexión', 'error')
    return redirect(url_for('usuarios'))


@app.route('/contribuciones')
@login_required
def contribuciones():
    estado = request.args.get('estado')
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    limit = 10
    skip = (page - 1) * limit
    
    params = {'skip': skip, 'limit': limit}
    if estado and estado != 'todos':
        params['estado'] = estado
    if query:
        params['query'] = query
        
    stats = {"total": 0, "pendientes": 0, "aprobadas": 0}
        
    try:
        response = api_request('GET', '/api/v1/contribuciones/', params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            contribuciones = data.get('data', [])
            total = data.get('total', 0)
            import math
            total_pages = math.ceil(total / limit)
        else:
            contribuciones = []
            total_pages = 1
            
        # Fetch Stats
        stats_response = api_request('GET', '/api/v1/contribuciones/stats', timeout=3)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
    except:
        contribuciones = []
        total_pages = 1
        flash('Error al cargar contribuciones', 'error')
    return render_template("pages/contribuciones.html", user=session.get('user'), contribuciones=contribuciones, active_filter=estado or 'todos', filter_query=query, page=page, total_pages=total_pages, stats=stats)

@app.route('/contribuciones/update', methods=['POST'])
@login_required
def update_contribucion():
    id_contribucion = request.form.get('id_contribucion')
    nuevo_estado = request.form.get('nuevo_estado')
    observaciones = request.form.get('observaciones')
    
    try:
        # La API espera query params según el endpoint que definimos
        params = {'estado': nuevo_estado}
        if observaciones:
            params['observaciones'] = observaciones
            
        response = api_request(
            'PUT',
            f'/api/v1/contribuciones/{id_contribucion}/estado',
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            flash(f'Contribución {nuevo_estado} correctamente', 'success')
        else:
            flash('Error al actualizar estado', 'error')
    except:
        flash('Error de conexión con el backend', 'error')
        
    return redirect(url_for('contribuciones'))

@app.route('/reportes')
@login_required
def reportes():
    estado = request.args.get('estado')
    prioridad = request.args.get('prioridad')
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    limit = 10
    skip = (page - 1) * limit
    
    params = {'skip': skip, 'limit': limit}
    if estado and estado != 'todos':
        params['estado'] = estado
    if prioridad and prioridad != 'todas':
        params['prioridad'] = prioridad
    if query:
        params['query'] = query

    stats = {"total": 0, "pendientes": 0, "resueltos": 0, "urgentes": 0}

    try:
        response = api_request('GET', '/api/v1/reportes/', params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            reports = data.get('data', [])
            total = data.get('total', 0)
            import math
            total_pages = math.ceil(total / limit)
        else:
            reports = []
            total_pages = 1
            
        # Fetch Stats
        stats_response = api_request('GET', '/api/v1/reportes/stats', timeout=3)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
    except:
        reports = []
        total_pages = 1
        flash('Error al cargar reportes', 'error')
        
    return render_template("pages/reportes.html", user=session.get('user'), reports=reports, filter_estado=estado, filter_prioridad=prioridad, filter_query=query, page=page, total_pages=total_pages, stats=stats)

@app.route('/reportes/update', methods=['POST'])
@login_required
def update_reporte():
    id_reporte = request.form.get('id_reporte')
    nuevo_estado = request.form.get('nuevo_estado')
    nueva_prioridad = request.form.get('nueva_prioridad')
    
    params = {}
    if nuevo_estado: params['estado'] = nuevo_estado
    if nueva_prioridad: params['prioridad'] = nueva_prioridad
    
    try:
        response = api_request(
            'PUT',
            f'/api/v1/reportes/{id_reporte}/gestion',
            params=params,
            timeout=5
        )
        if response.status_code == 200:
            flash('Reporte actualizado correctamente', 'success')
        else:
            flash('Error al actualizar reporte', 'error')
    except:
        flash('Error de conexión con el backend', 'error')
        
    return redirect(url_for('reportes'))

@app.route('/perfil')
@login_required
def perfil():
    """Muestra el perfil del usuario actual, refrescando datos desde el backend."""
    try:
        # Obtener datos actualizados del usuario desde el endpoint /me
        response = api_request('GET', '/api/v1/usuarios/me', timeout=5)
        if response.status_code == 200:
            user_data = response.json()
            session['user'] = user_data
            session.modified = True
    except:
        pass # Si falla el backend, usamos lo que hay en sesión
        
    return render_template("pages/perfil.html", user=session.get('user'))

@app.route('/perfil/update', methods=['POST'])
@login_required
def update_perfil():
    """Procesa la actualización de los datos personales del usuario."""
    user = session.get('user')
    id_usuario = user.get('id_usuario')
    
    # Recopilar solo datos que existen en la DB
    datos = {
        "nombre_completo": request.form.get('nombre_completo')
    }
    
    try:
        # Petición PUT al backend (FastAPI)
        response = api_request('PUT', f'/api/v1/usuarios/{id_usuario}', json=datos, timeout=5)
        
        if response.status_code == 200:
            # Sincronizar sesión con el objeto completo devuelto
            user_data = response.json()
            session['user'] = user_data
            session.modified = True
            flash('Perfil actualizado correctamente', 'success')
        else:
            error_detail = response.json().get('detail', 'Error desconocido')
            flash(f'Error al actualizar el perfil: {error_detail}', 'error')
    except Exception as e:
        print(f"Error sincronizando perfil: {str(e)}")
        flash('Error de conexión con el servidor', 'error')
        
    return redirect(url_for('perfil'))

@app.route('/perfil/avatar', methods=['POST'])
@login_required
def update_avatar():
    """Procesa el cambio de la imagen de perfil."""
    if 'avatar' not in request.files:
        flash('No se seleccionó ninguna imagen', 'error')
        return redirect(url_for('perfil'))
        
    file = request.files['avatar']
    if file.filename == '':
        flash('No se seleccionó ninguna imagen', 'error')
        return redirect(url_for('perfil'))
        
    if file:
        import os
        from werkzeug.utils import secure_filename
        
        # Asegurar directorio de destino
        upload_dir = os.path.join(app.root_path, 'static', 'img', 'profiles')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        user = session.get('user')
        id_usuario = user.get('id_usuario')
        
        # Generar nombre único con tiempo para forzar sincronización: user_1_162548.jpg/png
        import time
        timestamp = int(time.time())
        extension = os.path.splitext(file.filename)[1]
        filename = f"user_{id_usuario}_{timestamp}{extension}"
        file_path = os.path.join(upload_dir, filename)
        
        try:
            # Eliminar imagen anterior si existe
            old_image = user.get('imagen_perfil')
            if old_image and old_image != 'user.svg':  # No eliminar el default
                old_path = os.path.join(upload_dir, old_image)
                if os.path.exists(old_path):
                    os.remove(old_path)
                    print(f"Imagen anterior eliminada: {old_path}")
            
            # Guardar archivo físicamente con su formato original
            file.save(file_path)
            
            # Notificar al backend sobre el nuevo nombre exacto
            response = api_request(
                'PUT',
                f'/api/v1/usuarios/{id_usuario}', 
                json={"imagen_perfil": filename},
                timeout=5
            )
            
            if response.status_code == 200:
                # Sincronizar sesión con los datos nuevos del backend
                user_data = response.json()
                session['user'] = user_data
                session.modified = True
                flash('Imagen de perfil actualizada correctamente', 'success')
            else:
                flash('Error al registrar la imagen en el servidor', 'error')
                
        except Exception as e:
            print(f"Error procesando avatar: {str(e)}")
            flash('Error al guardar la imagen', 'error')
            
    return redirect(url_for('perfil'))

@app.route('/perfil/password', methods=['POST'])
@login_required
def update_password():
    """Procesa el cambio de contraseña."""
    user = session.get('user')
    id_usuario = user.get('id_usuario')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    try:
        # 1. Verificar contraseña actual con el backend (login)
        login_response = requests.post(
            f'{API_URL}/api/v1/auth/login',
            json={'correo': user.get('correo'), 'contrasena': current_password},
            timeout=5
        )
        
        if login_response.status_code != 200:
            flash('La contraseña actual es incorrecta', 'error')
            return redirect(url_for('perfil'))
            
        # 2. Si es correcta, actualizar a la nueva
        update_response = api_request(
            'PUT',
            f'/api/v1/usuarios/{id_usuario}',
            json={'contrasena': new_password},
            timeout=5
        )
        
        if update_response.status_code == 200:
            flash('Contraseña cambiada exitosamente', 'success')
        else:
            flash('Error al cambiar la contraseña', 'error')
            
    except Exception as e:
        flash('Error de conexión con el servidor', 'error')
        
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")