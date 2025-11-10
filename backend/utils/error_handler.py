"""
Sistema automático de registro de errores en alertas_sistema
Previene duplicados usando hash MD5
"""
import hashlib
from connection.db import get_connection


def _generar_hash(modulo, tipo_error, funcion_fallida):
    """Genera hash único para identificar el error"""
    cadena = f"{modulo}|{tipo_error}|{funcion_fallida or 'N/A'}"
    return hashlib.md5(cadena.encode()).hexdigest()


def registrar_error(modulo, tipo_error, severidad, descripcion, funcion_fallida=None, origen_sistema=None, extra_context=None):
    """
    Registra error en alertas_sistema. Si ya existe sin resolver, incrementa contador.
    Args:
        modulo: 'traducción', 'almacenamiento', 'autenticación', 'otro'
        tipo_error: Tipo de error
    severidad: 'bajo', 'medio', 'alto', 'critico'
        descripcion: Descripción del error
        funcion_fallida: Nombre de la función
        origen_sistema: Origen del error
    """
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Generar hash único
            # Enriquecer descripción con contexto de request/session si existe
            try:
                from flask import has_request_context, request, session
                if 'Request Context Not Available':
                    pass
            except Exception:
                has_request_context = lambda: False
                request = None
                session = {}

            contexto_parts = []
            if extra_context:
                contexto_parts.append(str(extra_context))

            try:
                if has_request_context():
                    try:
                        usuario = None
                        # intentar obtener id de usuario común en session
                        if session:
                            usuario = session.get('user_id') or session.get('usuario') or session.get('user')
                        metodo = request.method
                        ruta = request.path
                        ip = request.remote_addr
                        params = dict(request.args) if request.args else {}
                        contexto_parts.append(f"ruta={ruta} method={metodo} ip={ip} usuario={usuario} params={params}")
                    except Exception:
                        # no queremos que capturar el contexto falle la registración
                        contexto_parts.append('context_capture_failed')
            except Exception:
                pass

            # Añadir traceback si está disponible
            try:
                import traceback
                tb = traceback.format_exc()
                if tb and 'NoneType: None' not in tb:
                    contexto_parts.append(f"traceback:\n{tb}")
            except Exception:
                pass

            if contexto_parts:
                descripcion = f"{descripcion}\n\nContexto: {' | '.join(contexto_parts)}"
            hash_error = _generar_hash(modulo, tipo_error, funcion_fallida)

            # Verificar si ya existe error sin resolver
            cursor.execute("""
                SELECT id_alerta, contador_ocurrencias 
                FROM alertas_sistema 
                WHERE hash_error = %s AND estado != 'resuelto'
            """, (hash_error,))

            error_existente = cursor.fetchone()

            if error_existente:
                # Incrementar contador
                cursor.execute("""
                    UPDATE alertas_sistema 
                    SET contador_ocurrencias = contador_ocurrencias + 1,
                        ultima_ocurrencia = NOW(),
                        descripcion = %s
                    WHERE id_alerta = %s
                """, (descripcion, error_existente['id_alerta']))
                connection.commit()
                print(f"⚠️ Error repetido (ID: {error_existente['id_alerta']}, Ocurrencias: {error_existente['contador_ocurrencias'] + 1})")
            else:
                # Crear nueva alerta
                cursor.execute("""
                    INSERT INTO alertas_sistema 
                    (modulo, tipo_error, severidad, origen_sistema, funcion_fallida, 
                     descripcion, hash_error, contador_ocurrencias, estado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 1, 'pendiente')
                """, (modulo, tipo_error, severidad, origen_sistema, funcion_fallida, descripcion, hash_error))
                connection.commit()
                print(f"🆕 Nueva alerta creada (ID: {cursor.lastrowid})")

    except Exception as e:
        print(f"❌ Error al registrar alerta: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


def error_db(funcion, detalle, archivo=None):
    """Registra error de base de datos con ubicación específica"""
    ubicacion = f"Archivo: {archivo} | Función: {funcion}" if archivo else f"Función: {funcion}"
    registrar_error(
        modulo='almacenamiento',
        tipo_error=f'Error BD en {funcion}',
        severidad='critico',
        descripcion=f"{ubicacion}\nDetalle: {detalle}",
        funcion_fallida=funcion,
        origen_sistema=archivo or 'database'
    )


def error_traduccion(funcion, detalle, archivo=None):
    """Registra error de traducción con ubicación específica"""
    ubicacion = f"Archivo: {archivo} | Función: {funcion}" if archivo else f"Función: {funcion}"
    registrar_error(
        modulo='traducción',
        tipo_error=f'Error traducción en {funcion}',
        severidad='alto',
        descripcion=f"{ubicacion}\nDetalle: {detalle}",
        funcion_fallida=funcion,
        origen_sistema=archivo or 'translation'
    )


def error_auth(funcion, detalle, archivo=None):
    """Registra error de autenticación con ubicación específica"""
    ubicacion = f"Archivo: {archivo} | Función: {funcion}" if archivo else f"Función: {funcion}"
    registrar_error(
        modulo='autenticación',
        tipo_error=f'Error auth en {funcion}',
        severidad='medio',
        descripcion=f"{ubicacion}\nDetalle: {detalle}",
        funcion_fallida=funcion,
        origen_sistema=archivo or 'auth'
    )


def error_generico(funcion, detalle, severidad='medio', archivo=None, tipo_especifico=None):
    """Registra error con detalles específicos de ubicación"""
    ubicacion = f"Archivo: {archivo} | Función: {funcion}" if archivo else f"Función: {funcion}"
    tipo = tipo_especifico or f'Error en {funcion}'
    registrar_error(
        modulo='otro',
        tipo_error=tipo,
        severidad=severidad,
        descripcion=f"{ubicacion}\nDetalle: {detalle}",
        funcion_fallida=funcion,
        origen_sistema=archivo or 'backend'
    )


def capturar_error(modulo='otro', severidad='medio'):
    """
    Decorador para capturar errores automáticamente

    Uso:
        @capturar_error(modulo='traducción', severidad='alto')
        def mi_funcion():
            # código
    """
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                registrar_error(
                    modulo=modulo,
                    tipo_error=f'Error en {func.__name__}',
                    severidad=severidad,
                    descripcion=str(e),
                    funcion_fallida=func.__name__,
                    origen_sistema=func.__module__
                )
                raise
        return wrapper
    return decorador

