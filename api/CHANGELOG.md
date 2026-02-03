# API Changelog

All notable changes to the SignTechnology API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### ⚠️ BREAKING CHANGES - Authentication & Authorization

The following endpoints now require authentication and/or specific roles. These are **breaking changes** that affect API consumers:

#### 🔐 Endpoints Now Requiring Authentication (JWT Token)

Previously public endpoints that now require authentication:

- **GET** `/api/v1/estadisticas` - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (any authenticated user)
  - **Impact:** Anonymous users can no longer access system statistics

- **GET** `/api/v1/contribuciones/stats` - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (any authenticated user)
  - **Impact:** Anonymous users can no longer access contribution statistics

- **GET** `/api/v1/contribuciones` - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (any authenticated user)
  - **Impact:** Anonymous users can no longer list contributions

- **GET** `/api/v1/reportes/stats` - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (any authenticated user)
  - **Impact:** Anonymous users can no longer access report statistics

- **GET** `/api/v1/reportes` - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (any authenticated user)
  - **Impact:** Anonymous users can no longer list reports

#### 👮 Endpoints Now Requiring Admin Role (Role ID = 1)

Previously open endpoints that now require admin privileges:

##### Usuarios (Users)

- **GET** `/api/v1/usuarios/stats` - Now requires admin role
  - **Before:** Public access
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** User statistics contain sensitive system information

- **GET** `/api/v1/usuarios` - Now requires admin role
  - **Before:** Public access
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** Listing all users exposes sensitive user information

- **POST** `/api/v1/usuarios` - Now requires admin role
  - **Before:** Public registration
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** User creation is now controlled by administrators only
  - **Note:** Description updated from "Registra un nuevo usuario" to "Crea un nuevo usuario (solo admin)"

- **GET** `/api/v1/usuarios/{id_usuario}` - Now requires admin role
  - **Before:** Public access
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** Viewing individual user details exposes sensitive information

- **PUT** `/api/v1/usuarios/{id_usuario}` - Now requires admin role
  - **Before:** No authentication required
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** User updates should be controlled by administrators

- **DELETE** `/api/v1/usuarios/{id_usuario}` - Now requires admin role
  - **Before:** No authentication required
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** User deletion is a critical operation that should be admin-only

##### Contribuciones (Contributions)

- **PUT** `/api/v1/contribuciones/{id_contribucion}/estado` - Now requires admin role
  - **Before:** No authentication required
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** Managing contribution status is an administrative task

##### Reportes (Reports)

- **PUT** `/api/v1/reportes/{id_reporte}/gestion` - Now requires admin role
  - **Before:** No authentication required
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** Managing report status and priority is an administrative task

- **DELETE** `/api/v1/reportes/{id_reporte}` - Now requires admin role
  - **Before:** No authentication required
  - **After:** Requires admin role (role_id = 1)
  - **Reason:** Resolving/deleting reports is an administrative task

### 📝 Other Changes

#### Added
- JWT authentication dependency `get_current_user_id` for authenticated endpoints
- Role-based authorization dependency `require_role(1)` for admin-only endpoints
- Improved docstrings for all endpoints with clearer descriptions

#### Changed
- Enhanced security model with proper authentication and authorization layers
- Standardized authorization pattern across all endpoints
- Improved endpoint documentation strings for clarity

### Migration Guide

#### For API Consumers

1. **Authentication Required**: Most endpoints now require a valid JWT token. Include it in requests:
   ```
   Authorization: Bearer <your_jwt_token>
   ```

2. **Admin-Only Endpoints**: Some management operations now require admin privileges (role_id = 1). Non-admin users will receive a `403 Forbidden` response.

3. **User Registration**: The `/usuarios` POST endpoint is no longer for self-registration. Contact an administrator to create new accounts.

4. **Public Endpoints Removed**: If your application relied on public access to statistics or listings, you'll need to:
   - Implement authentication flow
   - Obtain JWT tokens for authenticated requests
   - Request admin access if using management endpoints

#### Endpoints Still Public

The following endpoints remain publicly accessible without authentication:

- **POST** `/api/v1/auth/login` - User login

#### Endpoints Available to Authenticated Users (Not Admin-Only)

The following endpoints require authentication but are available to any authenticated user:

- **GET** `/api/v1/usuarios/me` - Get current user profile (no change, was always authenticated)

### Security Rationale

These changes were implemented to:
- Protect sensitive user data from unauthorized access
- Prevent unauthorized modifications to system resources
- Implement proper role-based access control (RBAC)
- Follow security best practices for API design
- Ensure only administrators can perform critical system operations

### Testing

When testing these endpoints:
- Use the `/auth/login` endpoint to obtain a JWT token
- Include the token in the `Authorization` header for all authenticated requests
- Ensure your test user has the appropriate role for admin-only endpoints

---

## Contact

For questions about these breaking changes or to request API access, please contact the development team.
