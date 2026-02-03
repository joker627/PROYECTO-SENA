# API Changelog

Este documento registra todos los cambios importantes en la API, especialmente cambios que rompen compatibilidad hacia atrás (breaking changes).

## [Unreleased] - 2026-02-02

### 🔒 Breaking Changes - Autenticación y Autorización

En el commit `853913c`, se implementó un sistema completo de autenticación y autorización basado en JWT. Todos los endpoints ahora requieren autenticación, y algunos requieren permisos específicos de administrador.

#### Endpoints de Usuarios (`/api/v1/usuarios`)

**Cambios de Autorización:**

| Endpoint | Antes | Ahora | Impacto |
|----------|-------|-------|---------|
| `GET /usuarios/me` | No requería autenticación | ✅ Requiere autenticación JWT | Los usuarios deben estar autenticados |
| `GET /usuarios/stats` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden acceder |
| `GET /usuarios/` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden listar usuarios |
| `POST /usuarios/` | Abierto (registro público) | 🔐 Requiere rol de administrador (rol_id=1) | ⚠️ **BREAKING**: Solo administradores pueden crear usuarios |
| `GET /usuarios/{id}` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden ver detalles |
| `PUT /usuarios/{id}` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden actualizar |
| `DELETE /usuarios/{id}` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | ⚠️ **BREAKING**: Solo administradores pueden eliminar usuarios |

**Justificación:**
- La creación de usuarios ahora está restringida a administradores para prevenir registros no autorizados
- La eliminación de usuarios requiere permisos administrativos por razones de seguridad y auditoría
- Los usuarios pueden consultar su propio perfil mediante `/usuarios/me`

#### Endpoints de Contribuciones (`/api/v1/contribuciones`)

**Cambios de Autorización:**

| Endpoint | Antes | Ahora | Impacto |
|----------|-------|-------|---------|
| `GET /contribuciones/stats` | No requería autenticación | ✅ Requiere autenticación JWT | Los usuarios deben estar autenticados |
| `GET /contribuciones/` | No requería autenticación | ✅ Requiere autenticación JWT | Los usuarios deben estar autenticados |
| `PUT /contribuciones/{id}/estado` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden cambiar estados |

**Justificación:**
- Solo usuarios autenticados pueden ver y crear contribuciones
- La aprobación/rechazo de contribuciones requiere permisos administrativos

#### Endpoints de Reportes (`/api/v1/reportes`)

**Cambios de Autorización:**

| Endpoint | Antes | Ahora | Impacto |
|----------|-------|-------|---------|
| `GET /reportes/stats` | No requería autenticación | ✅ Requiere autenticación JWT | Los usuarios deben estar autenticados |
| `GET /reportes/` | No requería autenticación | ✅ Requiere autenticación JWT | Los usuarios deben estar autenticados |
| `PUT /reportes/{id}/gestion` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden gestionar reportes |
| `DELETE /reportes/{id}` | No requería autenticación | 🔐 Requiere rol de administrador (rol_id=1) | Solo administradores pueden eliminar reportes |

**Justificación:**
- Los reportes son sensibles y solo deben ser visibles para usuarios autenticados
- La gestión y resolución de reportes es una operación administrativa

#### Endpoints de Estadísticas (`/api/v1/estadisticas`)

**Cambios de Autorización:**

| Endpoint | Antes | Ahora | Impacto |
|----------|-------|-------|---------|
| `GET /estadisticas/` | No requería autenticación | ✅ Requiere autenticación JWT | Los usuarios deben estar autenticados |

**Justificación:**
- Las estadísticas del sistema son información interna que requiere autenticación

### 🔑 Cómo Autenticarse

Para acceder a los endpoints protegidos, los clientes deben:

1. **Obtener un token JWT** mediante el endpoint de login:
   ```http
   POST /api/v1/auth/login
   Content-Type: application/json

   {
     "correo": "usuario@ejemplo.com",
     "contrasena": "password"
   }
   ```

2. **Incluir el token en las peticiones** subsiguientes:
   ```http
   GET /api/v1/usuarios/me
   Authorization: Bearer <tu_token_jwt>
   ```

### 📝 Notas de Migración

**Para desarrolladores de clientes:**
- Actualicen sus aplicaciones para incluir el header `Authorization: Bearer <token>` en todas las peticiones
- Implementen flujos de login y gestión de tokens
- Los usuarios anónimos ya no pueden acceder a la mayoría de endpoints

**Para administradores del sistema:**
- Creen las primeras cuentas de administrador directamente en la base de datos si es necesario
- Configuren las variables de entorno JWT (`SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE`)

### 🔧 Cambios Técnicos

- ✅ Agregadas dependencias `get_current_user_id` y `require_role` en `app.core.dependencies`
- ✅ Implementación completa de JWT en `app.core.security`
- ✅ Validación de roles por endpoint
- ✅ Eliminado `UserInfoSchema` no utilizado
- ✅ Optimizados imports en todos los endpoints

---

## Formato de Versiones

Este changelog sigue el formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y se adhiere al [Versionado Semántico](https://semver.org/lang/es/).

### Tipos de Cambios

- **Added** - Nuevas funcionalidades
- **Changed** - Cambios en funcionalidades existentes
- **Deprecated** - Funcionalidades que serán eliminadas en futuras versiones
- **Removed** - Funcionalidades eliminadas
- **Fixed** - Corrección de errores
- **Security** - Correcciones de seguridad
- **Breaking Changes** - Cambios que rompen compatibilidad con versiones anteriores

### Símbolos

- ✅ Requiere autenticación JWT
- 🔐 Requiere rol de administrador
- ⚠️ Cambio que rompe compatibilidad (Breaking Change)
