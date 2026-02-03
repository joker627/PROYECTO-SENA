# Changelog - SignTechnology API

All notable changes to the SignTechnology API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- JWT authentication for all endpoints
- Role-based authorization system with `get_current_user_id` and `require_role` dependencies
- Authentication requirement for statistics endpoints
- Admin-only access for user creation endpoint

### Changed - ⚠️ BREAKING CHANGES

#### Authentication Requirements
All API endpoints now require JWT authentication. Previously public endpoints are now protected:

**Reportes (Reports) Endpoints:**
- `GET /api/v1/reportes/stats` - Now requires authentication (any authenticated user)
- `GET /api/v1/reportes/` - Now requires authentication (any authenticated user)
- `PUT /api/v1/reportes/{id_reporte}/gestion` - Now requires **admin role** (role_id = 1)
- `DELETE /api/v1/reportes/{id_reporte}` - Now requires **admin role** (role_id = 1)

**Contribuciones (Contributions) Endpoints:**
- `GET /api/v1/contribuciones/stats` - Now requires authentication (any authenticated user)
- `GET /api/v1/contribuciones/` - Now requires authentication (any authenticated user)
- `PUT /api/v1/contribuciones/{id_contribucion}/estado` - Now requires **admin role** (role_id = 1)

**Usuarios (Users) Endpoints:**
- All endpoints except `GET /api/v1/usuarios/me` now require **admin role** (role_id = 1)
- `POST /api/v1/usuarios/` - User creation now requires **admin role** (role_id = 1)

**Estadísticas (Statistics) Endpoints:**
- `GET /api/v1/estadisticas` - Now requires authentication (any authenticated user)

#### Migration Guide

To continue using these endpoints, clients must:

1. **Obtain a JWT token** by calling `POST /api/v1/auth/login` with valid credentials:
   ```json
   {
     "correo": "user@example.com",
     "contrasena": "password"
   }
   ```

2. **Include the token** in the Authorization header for all subsequent requests:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

3. **Admin-only endpoints** require the authenticated user to have `role_id = 1` (Administrador role)

#### Rationale

These changes were implemented to:
- Protect sensitive data and operations
- Ensure only authorized users can view reports and contributions
- Restrict management operations (updating status, deleting) to administrators only
- Align with security best practices for production environments

### Security
- Implemented bcrypt password hashing
- Added JWT token-based authentication with configurable expiration
- Role-based access control (RBAC) for admin operations

## [1.0.0] - Previous Version

### Initial Release
- Basic CRUD operations for users, contributions, and reports
- No authentication or authorization
- Public access to all endpoints
