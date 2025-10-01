# Sistema de Manejo de Errores - Traductor de Señas SENA

Este directorio contiene todas las páginas de error personalizadas para el proyecto traductor de señas.

## Estructura de Archivos

```
errors/
├── 400.html    # Solicitud incorrecta (Bad Request)
├── 403.html    # Acceso prohibido (Forbidden)
├── 404.html    # Página no encontrada (Not Found)
├── 405.html    # Método no permitido (Method Not Allowed)
└── 500.html    # Error interno del servidor (Internal Server Error)
```

## Errores Manejados

### 🔍 **404 - Página No Encontrada**
- **Cuándo ocurre**: URL inexistente o mal escrita
- **Características**: 
  - Enlaces a páginas principales
  - Sugerencias de navegación
  - Botón para volver atrás

### 🚫 **403 - Acceso Prohibido** 
- **Cuándo ocurre**: Sin permisos para el recurso
- **Características**:
  - Enlaces a login (si no está autenticado)
  - Información sobre permisos
  - Contacto con administrador

### ⚠️ **500 - Error Interno del Servidor**
- **Cuándo ocurre**: Fallos en el código del servidor
- **Características**:
  - Mensaje tranquilizador para el usuario
  - Timestamp del error
  - Botón para reintentar

### ❌ **400 - Solicitud Incorrecta**
- **Cuándo ocurre**: Datos del formulario inválidos
- **Características**:
  - Consejos para corregir formularios
  - Validaciones comunes
  - Botón para volver atrás

### 🚫 **405 - Método No Permitido**
- **Cuándo ocurre**: HTTP method incorrecto (GET vs POST)
- **Características**:
  - Explicación técnica simplificada
  - Alternativas de navegación

## Características Comunes

### 🎨 **Diseño Consistente**
- Extienden del template `menu.html`
- Colores diferenciados por tipo de error
- Diseño responsivo para móviles
- Iconos descriptivos

### 🔧 **Funcionalidades**
- **Navegación**: Enlaces al inicio y página anterior
- **Sugerencias**: Acciones específicas para cada error
- **Contacto**: Información del SENA para soporte
- **Accesibilidad**: Compatible con lectores de pantalla

### 📱 **Responsive Design**
- Adaptable a diferentes tamaños de pantalla
- Botones optimizados para touch
- Texto legible en dispositivos móviles

## Implementación Backend

### Archivo: `error_handlers.py`
```python
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    # ... más manejadores
```

### Registro en `main.py`
```python
from error_handlers import register_error_handlers
register_error_handlers(app)
```

## Personalización

### Colores por Tipo de Error
- **404**: Rojo (`#e74c3c`) - Error crítico
- **403**: Púrpura (`#8e44ad`) - Restricción de acceso  
- **500**: Naranja (`#e67e22`) - Error del servidor
- **400**: Rojo claro (`#e74c3c`) - Error del cliente
- **405**: Amarillo (`#f39c12`) - Error de método

### Estilos CSS
Cada página incluye CSS específico para:
- Código de error grande y visible
- Contenedores responsivos
- Botones de acción
- Cajas de sugerencias con estilos únicos

## Testing de Errores

Para probar las páginas de error:

```bash
# 404 - Acceder a URL inexistente
GET /pagina-que-no-existe

# 500 - Forzar error en el código
# (Agregar código que genere excepción)

# 403 - Acceder sin permisos
# (Requerir autenticación en ruta protegida)

# 400 - Enviar datos inválidos
# (Formulario con datos malformados)

# 405 - Método incorrecto
POST /ruta-que-solo-acepta-get
```

## SEO y Accesibilidad

### Meta Tags
- Títulos descriptivos
- Meta description apropiada
- Viewport responsive

### Accesibilidad
- Estructura semántica HTML5
- Contraste de colores adecuado
- Navegación por teclado
- Texto alternativo en iconos

## Monitoreo

### Logging
Los errores se pueden registrar añadiendo:
```python
import logging
logging.error(f'Error {error.code}: {error.description}')
```

### Analytics
Considerar tracking de:
- Páginas de error más frecuentes
- Patrones de navegación después del error
- Tasa de recuperación (vuelven al sitio)

## Futuras Mejoras

- [ ] Página de error offline (PWA)
- [ ] Sistema de reportes de bugs integrado
- [ ] Sugerencias inteligentes basadas en la URL
- [ ] Integración con chat de soporte
- [ ] Página de mantenimiento (503)