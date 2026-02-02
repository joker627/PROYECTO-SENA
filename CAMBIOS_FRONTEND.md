# Cambios en el Frontend - Autenticación JWT

## Resumen de Cambios

Se actualizó el frontend de Flask para trabajar con la nueva arquitectura de autenticación JWT de la API, donde el login retorna solo el token y el perfil del usuario se obtiene a través del endpoint `/usuarios/me`.

---

## 🔐 Cambios en Autenticación

### 1. Nueva Función Helper: `get_auth_headers()`
```python
def get_auth_headers():
    """Obtiene los headers de autorización con el token JWT."""
    token = session.get('token')
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}
```

**Ubicación:** `frontend/run.py` (línea ~30)  
**Propósito:** Centraliza la generación de headers de autorización para todas las peticiones a la API.

---

## 🔄 Flujo de Login Actualizado

### Antes (❌ Antiguo)
```python
response = requests.post(f'{API_URL}/api/v1/auth/login', ...)
data = response.json()
session['user'] = data.get('user')  # ❌ Ya no viene
session['token'] = data.get('access_token')
```

### Ahora (✅ Nuevo)
```python
# Paso 1: Obtener token
response = requests.post(f'{API_URL}/api/v1/auth/login', ...)
token = data.get('access_token')

# Paso 2: Obtener perfil con el token
profile_response = requests.get(
    f'{API_URL}/api/v1/usuarios/me',
    headers={'Authorization': f'Bearer {token}'}
)
user_profile = profile_response.json()

# Guardar en sesión
session['token'] = token
session['user'] = user_profile
```

**Beneficios:**
- ✅ Mayor seguridad: JWT solo contiene `{sub, email, role, exp}`
- ✅ Datos frescos: El perfil siempre está actualizado
- ✅ Mejor separación: Token ≠ Perfil
- ✅ Menor payload: Token más liviano (~200 bytes vs ~800 bytes)

---

## 📝 Rutas Actualizadas

### Gestión de Usuarios
| Ruta | Método | Cambio |
|------|--------|--------|
| `/usuarios/create` | POST | ✅ Ahora envía `headers=get_auth_headers()` |
| `/usuarios/update` | POST | ✅ Ahora envía `headers=get_auth_headers()` |
| `/usuarios/delete` | POST | ✅ Ahora envía `headers=get_auth_headers()` |

### Perfil de Usuario
| Ruta | Método | Cambios Realizados |
|------|--------|-------------------|
| `/perfil` | GET | ✅ Usa `/usuarios/me` en lugar de `/usuarios/{id}` |
| `/perfil/update` | POST | ✅ Envía token + refresca datos desde `/usuarios/me` |
| `/perfil/avatar` | POST | ✅ Envía token + refresca datos desde `/usuarios/me` |
| `/perfil/password` | POST | ✅ Envía token en la actualización |

### Cambio Crítico en `/perfil`

**Antes:**
```python
user = session.get('user')
response = requests.get(f"{API_URL}/api/v1/usuarios/{user.get('id_usuario')}", ...)
```

**Ahora:**
```python
response = requests.get(
    f"{API_URL}/api/v1/usuarios/me",  # ✅ Endpoint correcto
    headers=get_auth_headers(),        # ✅ Con token
    timeout=5
)
```

---

## 🔒 Seguridad Mejorada

### JWT Payload Reducido

**Antes (❌ Inseguro):**
```json
{
  "sub": 1,
  "email": "user@example.com",
  "role": "admin",
  "nombre_completo": "Juan Pérez",
  "imagen_perfil": "user_1.jpg",
  "tipo_documento": "CC",
  "numero_documento": "123456789",
  ...  // ~800 bytes
}
```

**Ahora (✅ Seguro):**
```json
{
  "sub": 1,
  "email": "user@example.com", 
  "role": "admin",
  "exp": 1735689600
}
// ~200 bytes
```

### Ventajas de Seguridad

1. **Datos sensibles protegidos:** El token no expone información personal
2. **Menor superficie de ataque:** Menos datos = menos riesgo si el token es interceptado
3. **Datos siempre actualizados:** El perfil se obtiene desde la base de datos, no del token
4. **Cumple estándares:** Sigue las mejores prácticas de JWT (RFC 7519)

---

## ✅ Verificación de Cambios

### Checklist de Funcionalidades

- [x] **Login:** Autenticación con token + obtención de perfil
- [x] **Perfil:** Visualización usando `/usuarios/me`
- [x] **Actualizar datos:** Envía token + refresca desde `/usuarios/me`
- [x] **Cambiar avatar:** Envía token + refresca desde `/usuarios/me`
- [x] **Cambiar contraseña:** Envía token en la actualización
- [x] **CRUD Usuarios:** Todas las operaciones envían el token
- [x] **Headers centralizados:** Función `get_auth_headers()` implementada

---

## 🧪 Pruebas Recomendadas

1. **Login exitoso:**
   - Ingresar con credenciales válidas
   - Verificar que se guarda el token en `session['token']`
   - Verificar que se guarda el perfil en `session['user']`

2. **Login fallido:**
   - Ingresar con credenciales inválidas
   - Verificar mensaje de error

3. **Perfil:**
   - Acceder a `/perfil`
   - Verificar que se muestra la información correcta
   - Actualizar nombre completo
   - Cambiar imagen de perfil
   - Cambiar contraseña

4. **Gestión de usuarios (admin):**
   - Crear un nuevo usuario
   - Actualizar un usuario existente
   - Eliminar un usuario

5. **Token expirado:**
   - Esperar a que el token expire (o manipular la fecha)
   - Verificar que la API retorna 401
   - Verificar redirección al login

---

## 📋 Archivos Modificados

- ✅ `frontend/run.py` - Actualización completa del flujo de autenticación

---

## 🚀 Próximos Pasos

1. **Probar el flujo completo de login**
2. **Verificar que todas las rutas protegidas funcionen**
3. **Implementar manejo de token expirado** (redireccionar al login)
4. **Actualizar pruebas unitarias** si existen

---

## 📝 Notas Importantes

- **Compatibilidad:** El frontend ahora es compatible con la API actualizada
- **Sesión:** Los datos del usuario se siguen guardando en `session['user']` para compatibilidad con templates
- **Token:** Se guarda en `session['token']` y se envía en cada petición autenticada
- **Endpoint `/usuarios/me`:** Es el nuevo estándar para obtener el perfil del usuario autenticado
