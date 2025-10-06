# 🚀 Guía Rápida de Desarrollo - PROYECTO SENA

## ⚡ Setup Rápido

### 📋 Pre-requisitos
- 🐍 Python 3.8+
- 🗄️ MySQL 8.0+
- 🌐 Navegador moderno

### 🛠️ Instalación Express
```bash
# 1. Clonar proyecto
git clone [repository-url]
cd PROYECTO-SENA

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar BD (editar backend/config/conexion.py)
# 4. Ejecutar
cd backend && python main.py
```

---

## 🎯 Estructura de Archivos Clave

### 📁 Backend (Lo más importante)
```
backend/
├── 🚀 main.py              # ⭐ Punto de entrada
├── 🎮 controllers/         # ⭐ Lógica de negocio
│   ├── auth_controller.py
│   └── profile_controller.py
├── 🛤️ routes/              # ⭐ Endpoints
│   ├── auth/auth.py
│   ├── profile_routes.py
│   └── routes.py
└── 🗃️ models/user_model.py # ⭐ Base de datos
```

### 📁 Frontend (Lo esencial)
```
frontend/
├── 📄 templates/           # ⭐ HTML (Jinja2)
│   ├── base/layout.html    # Layout principal
│   └── auth/profile/index.html
├── 🎨 static/css/          # ⭐ Estilos
└── ⚡ static/js/           # JavaScript mínimo
```

---

## 🔧 Flujos de Desarrollo Comunes

### 1. 🆕 Agregar Nueva Funcionalidad

#### Paso 1: Crear Model Function
```python
# models/user_model.py
def nueva_funcion_bd():
    conexion = conectar_db()
    cursor = conexion.cursor()
    # SQL queries aquí
    return resultado
```

#### Paso 2: Crear Controller Method
```python
# controllers/nuevo_controller.py
class NuevoController:
    @staticmethod
    def nueva_funcionalidad():
        # Lógica de negocio aquí
        resultado = nueva_funcion_bd()
        return success, message
```

#### Paso 3: Crear Route
```python
# routes/nuevas_routes.py
@bp.route('/nueva-ruta', methods=['POST'])
def nueva_ruta():
    resultado = NuevoController.nueva_funcionalidad()
    flash(resultado[1], 'success' if resultado[0] else 'danger')
    return redirect(url_for('destino'))
```

#### Paso 4: Actualizar Template
```html
<!-- templates/nueva_pagina.html -->
<form method="POST" action="{{ url_for('nuevo_bp.nueva_ruta') }}">
    <!-- Formulario aquí -->
</form>
```

### 2. 🔐 Agregar Ruta Protegida

```python
def require_login():
    if not AuthController.require_login():
        flash('Debes iniciar sesión', 'danger')
        return redirect(url_for('auth.login'))
    return None

@bp.route('/ruta-protegida')
def ruta_protegida():
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    # Lógica de la ruta protegida
    return render_template('template.html')
```

### 3. 📝 Agregar Validación de Forms

```python
# En Controller
def validar_datos(data):
    errors = []
    
    if not data.get('campo'):
        errors.append('Campo es obligatorio')
    
    if len(data.get('campo', '')) < 3:
        errors.append('Campo debe tener al menos 3 caracteres')
    
    return len(errors) == 0, errors
```

---

## 📊 Patrones de Código

### 🎮 Controller Pattern
```python
class MiController:
    @staticmethod
    def accion_principal(parametros):
        # 1. Validaciones
        if not validacion():
            return False, "Error de validación"
        
        # 2. Lógica de negocio
        resultado = procesar_datos(parametros)
        
        # 3. Llamada al modelo
        success = MiModel.guardar_datos(resultado)
        
        # 4. Respuesta
        return success, "Mensaje de éxito/error"
```

### 🛤️ Route Pattern
```python
@bp.route('/mi-ruta', methods=['GET', 'POST'])
def mi_ruta():
    # 1. Verificar autenticación (si es necesario)
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    
    if request.method == 'POST':
        # 2. Obtener datos del formulario
        data = request.form.get('campo')
        
        # 3. Llamar al controller
        success, message = MiController.accion_principal(data)
        
        # 4. Flash message y redirect
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('mi_bp.mi_ruta'))
    
    # 5. GET request - mostrar formulario
    return render_template('mi_template.html')
```

### 🗃️ Model Pattern
```python
def operacion_bd(parametros):
    conexion = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Query SQL
        query = "SELECT * FROM tabla WHERE condicion = %s"
        cursor.execute(query, (parametros,))
        
        resultado = cursor.fetchall()
        return resultado
        
    except Exception as e:
        print(f"Error en BD: {e}")
        return None
    finally:
        if conexion:
            conexion.close()
```

---

## 🎨 Frontend Guidelines

### 📄 Template Structure
```html
{% extends "base/layout.html" %}

{% block title %}Título de la Página{% endblock %}

{% block content %}
    <!-- Mostrar mensajes flash -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <!-- Flash messages aquí -->
        {% endif %}
    {% endwith %}

    <!-- Contenido principal -->
    <div class="container">
        <!-- Tu contenido aquí -->
    </div>
{% endblock %}
```

### 🎨 CSS Classes Convention
```css
/* Estructura de clases */
.component-name              /* Componente principal */
.component-name__element     /* Elemento del componente */
.component-name--modifier    /* Modificador del componente */

/* Ejemplos */
.profile-form               /* Formulario de perfil */
.profile-form__input        /* Input del formulario */
.profile-form--loading      /* Estado de carga */
```

### ⚡ JavaScript Minimal
```javascript
// Solo para interacciones simples
function toggleSection(sectionId) {
    const sections = document.querySelectorAll('.profile-section');
    sections.forEach(s => s.classList.remove('active'));
    
    document.getElementById(sectionId).classList.add('active');
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Inicialización aquí
});
```

---

## 🗄️ Database Quick Reference

### 👥 Tabla usuarios
```sql
-- Estructura principal
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,  -- bcrypt hash
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);
```

### 🔍 Queries Comunes
```sql
-- Buscar usuario por email
SELECT * FROM usuarios WHERE correo = %s;

-- Actualizar nombre de usuario
UPDATE usuarios SET nombre = %s WHERE id_usuario = %s;

-- Verificar si email existe
SELECT COUNT(*) FROM usuarios WHERE correo = %s;

-- Obtener usuario con rol
SELECT u.*, r.nombre_rol 
FROM usuarios u 
JOIN roles r ON u.id_rol = r.id_rol 
WHERE u.id_usuario = %s;
```

---

## 🔧 Debugging Tips

### 🐛 Errores Comunes

#### 1. ImportError
```python
# ❌ Error: No module named 'controllers'
from controllers.auth_controller import AuthController

# ✅ Solución: Verificar PYTHONPATH o usar rutas relativas
import sys
sys.path.append('..')
```

#### 2. Template Not Found
```python
# ❌ Error: template not found
return render_template('login.html')

# ✅ Verificar ruta completa
return render_template('auth/login.html')
```

#### 3. Database Connection
```python
# ❌ Error de conexión
# Verificar config/conexion.py
# Verificar que MySQL esté ejecutándose
# Verificar credenciales de BD
```

### 📊 Debug Mode
```python
# En main.py para desarrollo
app.run(debug=True, host='0.0.0.0')

# Variables de entorno para producción
app.run(debug=False)
```

---

## 🚀 Deployment Checklist

### 📋 Pre-Deploy
- [ ] 🔐 Cambiar `app.secret_key`
- [ ] 🗄️ Configurar BD de producción
- [ ] 🔍 Revisar todos los `debug=False`
- [ ] 📦 Generar `requirements.txt` actualizado
- [ ] 🧪 Ejecutar todos los tests
- [ ] 🔒 Verificar configuraciones de seguridad

### 🌐 Production Settings
```python
# config/production.py
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False
    TESTING = False
```

---

## 📚 Recursos Útiles

### 📖 Documentación
- 🌶️ [Flask Docs](https://flask.palletsprojects.com/)
- 🗄️ [PyMySQL Docs](https://pymysql.readthedocs.io/)
- 🔐 [bcrypt Docs](https://pypi.org/project/bcrypt/)

### 🛠️ Herramientas de Desarrollo
- 🔍 **Debug**: Flask debug mode + browser dev tools
- 🗄️ **DB Manager**: phpMyAdmin, MySQL Workbench
- 🧪 **Testing**: pytest (para futuras pruebas)
- 📊 **Performance**: Flask profiler

---

*⚡ Esta guía te permite desarrollar eficientemente en el PROYECTO SENA*
*📅 Actualizado: Octubre 2025*