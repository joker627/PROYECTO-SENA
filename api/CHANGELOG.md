# API Changelog

All notable changes to the SignTechnology API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Breaking Changes - Authentication & Authorization

⚠️ **IMPORTANT:** The following endpoints now require authentication and/or specific role authorization. API consumers must update their integrations accordingly.

#### Usuarios (Users) Endpoints

All user management endpoints now require admin role (role_id = 1), except for `/me`:

- **GET /api/v1/usuarios/stats** - Now requires admin role
  - **Before:** Public access
  - **After:** Requires admin authentication (`require_role(1)`)
  - **Migration:** Ensure requests include JWT token with admin role

- **GET /api/v1/usuarios** - Now requires admin role
  - **Before:** Public access
  - **After:** Requires admin authentication (`require_role(1)`)
  - **Migration:** Ensure requests include JWT token with admin role

- **POST /api/v1/usuarios** - Now requires admin role
  - **Before:** Public user registration
  - **After:** Only admins can create users (`require_role(1)`)
  - **Migration:** User registration flow must be updated. Consider creating a separate public registration endpoint if self-registration is needed.

- **GET /api/v1/usuarios/{id_usuario}** - Now requires admin role
  - **Before:** Public access to user profiles
  - **After:** Requires admin authentication (`require_role(1)`)
  - **Migration:** Users can access their own profile via `/api/v1/usuarios/me` endpoint

- **PUT /api/v1/usuarios/{id_usuario}** - Now requires admin role
  - **Before:** Public access to update any user
  - **After:** Only admins can update users (`require_role(1)`)
  - **Migration:** Users should update their own profile through a dedicated endpoint, or admins must authenticate

- **DELETE /api/v1/usuarios/{id_usuario}** - Now requires admin role
  - **Before:** Public access to delete users
  - **After:** Only admins can delete users (`require_role(1)`)
  - **Migration:** Ensure delete operations are performed by authenticated admins only

#### Contribuciones (Contributions) Endpoints

- **GET /api/v1/contribuciones/stats** - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (`get_current_user_id`)
  - **Migration:** Include JWT token in Authorization header

- **GET /api/v1/contribuciones** - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (`get_current_user_id`)
  - **Migration:** Include JWT token in Authorization header

- **PUT /api/v1/contribuciones/{id_contribucion}/estado** - Now requires admin role
  - **Before:** Public access to update contribution status
  - **After:** Only admins can update contribution status (`require_role(1)`)
  - **Migration:** Ensure status updates are performed by authenticated admins only

#### Reportes (Reports) Endpoints

- **GET /api/v1/reportes/stats** - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (`get_current_user_id`)
  - **Migration:** Include JWT token in Authorization header

- **GET /api/v1/reportes** - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (`get_current_user_id`)
  - **Migration:** Include JWT token in Authorization header

- **PUT /api/v1/reportes/{id_reporte}/gestion** - Now requires admin role
  - **Before:** Public access to manage reports
  - **After:** Only admins can manage reports (`require_role(1)`)
  - **Migration:** Ensure report management is performed by authenticated admins only

- **DELETE /api/v1/reportes/{id_reporte}** - Now requires admin role
  - **Before:** Public access to resolve/delete reports
  - **After:** Only admins can resolve/delete reports (`require_role(1)`)
  - **Migration:** Ensure report deletion is performed by authenticated admins only

#### Estadisticas (Statistics) Endpoints

- **GET /api/v1/estadisticas** - Now requires authentication
  - **Before:** Public access
  - **After:** Requires valid JWT token (`get_current_user_id`)
  - **Migration:** Include JWT token in Authorization header

### Migration Guide

#### Authentication Setup

All authenticated endpoints now require a valid JWT token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

To obtain a JWT token, authenticate via the login endpoint:

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

#### Role Requirements

- **Admin Role (role_id = 1):** Required for all user management operations, contribution/report management
- **Authenticated User:** Required for viewing contributions, reports, and statistics

#### Public Endpoints Remaining

The following endpoints remain publicly accessible:
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/usuarios/me` - Current user profile (requires authentication but not admin role)

### Rationale

These changes were implemented to:

1. **Improve Security:** Prevent unauthorized access to sensitive user data and system statistics
2. **Enforce Role-Based Access Control (RBAC):** Ensure only administrators can perform critical operations
3. **Protect User Privacy:** Restrict access to user information to authorized personnel only
4. **Prevent Data Manipulation:** Limit contribution and report management to administrators

### Backwards Compatibility

⚠️ **These are breaking changes.** Applications consuming this API must be updated to:

1. Obtain and include JWT tokens for authenticated endpoints
2. Ensure proper role permissions for admin-only endpoints
3. Update error handling for 401 (Unauthorized) and 403 (Forbidden) responses

### Need Help?

For questions about migration or implementation, please:
- Review the [Technical Documentation](README_TECNICO.md)
- Check the [Swagger UI](http://localhost:8000/docs) for interactive API documentation
- Open an issue in the repository

---

## [Previous Versions]

No previous versions documented. This is the first changelog entry documenting breaking changes.
