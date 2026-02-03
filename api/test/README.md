# Pruebas de Carga con Locust

Este directorio contiene scripts para realizar pruebas de carga en la API de SignTechnology.

## Requisitos

- Python 3.8+
- Locust instalado: `pip install locust`

## Configuración

Antes de ejecutar las pruebas de carga, debes configurar las siguientes variables de entorno:

- `TEST_USER_EMAIL`: Correo electrónico de un usuario de prueba con permisos adecuados
- `TEST_USER_PASSWORD`: Contraseña del usuario de prueba

### Ejemplo de configuración

```bash
export TEST_USER_EMAIL="test@example.com"
export TEST_USER_PASSWORD="test_password"
```

O puedes crear un archivo `.env.test` (asegúrate de que esté en `.gitignore`):

```env
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=test_password
```

## Ejecución

Para ejecutar las pruebas de carga:

```bash
# Cargar variables de entorno
export TEST_USER_EMAIL="your_test_email@example.com"
export TEST_USER_PASSWORD="your_test_password"

# Ejecutar Locust
locust -f locustfile.py --host=http://localhost:8000
```

Luego abre tu navegador en `http://localhost:8089` para acceder a la interfaz web de Locust.

## Seguridad

**IMPORTANTE**: Nunca incluyas credenciales reales en el código fuente. Siempre usa variables de entorno para configurar credenciales de prueba.
