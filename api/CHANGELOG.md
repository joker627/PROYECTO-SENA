# API Changelog

All notable changes to the SignTechnology API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed - BREAKING CHANGES

#### Authentication & Authorization Implementation

All API endpoints now require JWT authentication. The following authorization changes have been implemented:

##### `/api/v1/usuarios` - Users Endpoints

- **`GET /usuarios/me`** - ✅ Requires authentication (any authenticated user)
- **`GET /usuarios/stats`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1)
- **`GET /usuarios/`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1)
- **`POST /usuarios/`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open for registration.
- **`GET /usuarios/{id_usuario}`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open to all.
- **`PUT /usuarios/{id_usuario}`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open to all.
- **`DELETE /usuarios/{id_usuario}`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open to all.

##### `/api/v1/contribuciones` - Contributions Endpoints

- **`GET /contribuciones/stats`** - ✅ **BREAKING**: Now requires authentication (any authenticated user). Previously open to all.
- **`GET /contribuciones/`** - ✅ **BREAKING**: Now requires authentication (any authenticated user). Previously open to all.
- **`PUT /contribuciones/{id_contribucion}/estado`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open to all.

##### `/api/v1/reportes` - Reports Endpoints

- **`GET /reportes/stats`** - ✅ **BREAKING**: Now requires authentication (any authenticated user). Previously open to all.
- **`GET /reportes/`** - ✅ **BREAKING**: Now requires authentication (any authenticated user). Previously open to all.
- **`PUT /reportes/{id_reporte}/gestion`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open to all.
- **`DELETE /reportes/{id_reporte}`** - 🔒 **BREAKING**: Now requires admin role (role ID: 1). Previously open to all.

##### `/api/v1/estadisticas` - Statistics Endpoints

- **`GET /estadisticas/`** - ✅ **BREAKING**: Now requires authentication (any authenticated user). Previously open to all.

#### Migration Guide

**For API Consumers:**

1. **Obtain JWT Token**: All API requests now require authentication. Call `POST /api/v1/auth/login` with valid credentials to obtain a JWT token.

   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"correo": "user@example.com", "contrasena": "password"}'
   ```

2. **Include Authorization Header**: Add the JWT token to all subsequent requests:

   ```bash
   curl -X GET "http://localhost:8000/api/v1/usuarios/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

3. **Admin-Only Endpoints**: Endpoints marked with 🔒 require admin role (role ID: 1). Regular users will receive a `403 Forbidden` response when attempting to access these endpoints.

4. **Error Responses**:
   - `401 Unauthorized` - Missing or invalid JWT token
   - `403 Forbidden` - Valid token but insufficient permissions (non-admin trying to access admin-only endpoint)

**Security Implications:**

- User creation is now restricted to administrators only. Self-registration is no longer available through the API.
- User management (view, update, delete) is restricted to administrators to protect user privacy and data integrity.
- Contribution and report management operations require appropriate permissions to prevent unauthorized modifications.

**Backward Compatibility:**

These changes are **NOT backward compatible**. Existing API clients must be updated to:
1. Implement authentication flow
2. Store and send JWT tokens with requests
3. Handle authentication and authorization errors appropriately

---

## [Previous Versions]

### Initial Release

- Basic CRUD operations for users, contributions, and reports
- Open endpoints without authentication
