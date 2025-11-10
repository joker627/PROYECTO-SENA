"""
CONTROLADOR DE NOTIFICACIONES 
=====================================================================
Este archivo conecta las rutas (routes) con el modelo (models).
Es como un "intermediario" que organiza la información.
Incluye manejo de errores automático con ErrorHandler.
"""

from models.notification_models import (
    obtener_todas_las_notificaciones,
    obtener_notificaciones_pendientes,
    contar_notificaciones_pendientes,
    cambiar_estado_notificacion,
    eliminar_notificacion,
    marcar_todas_como_resueltas,
    eliminar_todas_las_notificaciones,
    eliminar_notificaciones_resueltas
)
from utils.error_handler import error_generico
from utils.error_handler import capturar_error

@capturar_error(modulo='notificaciones', severidad='medio')
def obtener_todas():
    """
    Obtiene todas las notificaciones y las devuelve en formato JSON.
    
    Retorna: Diccionario con success=True/False y los datos
    """
    try:
        # 1. Llamar al modelo para obtener las notificaciones
        notificaciones = obtener_todas_las_notificaciones()
        
        # 2. Devolver resultado exitoso
        return {
            'success': True,
            'notificaciones': notificaciones,
            'total': len(notificaciones)
        }
        
    except Exception as error:
        # Registrar el error en el sistema
        error_generico(
            funcion='obtener_todas',
            detalle=f'Error en controlador al obtener todas las notificaciones: {str(error)}',
            severidad='alto',
            archivo='controllers/notifications_controller.py',
            tipo_especifico='Error Controlador Notificaciones'
        )
        print(f"❌ Error en controlador - obtener todas: {error}")
        return {
            'success': False,
            'error': 'Error al obtener notificaciones',
            'notificaciones': []
        }


@capturar_error(modulo='notificaciones', severidad='medio')
def obtener_pendientes():
    """
    Obtiene solo las notificaciones que NO están resueltas.
    
    Retorna: Diccionario con las notificaciones pendientes
    """
    try:
        # 1. Obtener notificaciones pendientes del modelo
        notificaciones = obtener_notificaciones_pendientes()
        
        # 2. Devolver resultado
        return {
            'success': True,
            'notificaciones': notificaciones,
            'total': len(notificaciones)
        }
        
    except Exception as error:
        error_generico(
            funcion='obtener_pendientes',
            detalle=f'Error al obtener notificaciones pendientes: {str(error)}',
            severidad='medio',
            archivo='controllers/notifications_controller.py',
            tipo_especifico='Error Controlador Notificaciones'
        )
        print(f"❌ Error en controlador - obtener pendientes: {error}")
        return {
            'success': False,
            'error': 'Error al obtener notificaciones pendientes',
            'notificaciones': []
        }


@capturar_error(modulo='notificaciones', severidad='medio')
def contar_pendientes():
    """
    Cuenta cuántas notificaciones están pendientes.
    Este número se muestra en el badge rojo.
    
    Retorna: Diccionario con el conteo
    """
    try:
        # 1. Obtener el conteo del modelo
        cantidad = contar_notificaciones_pendientes()
        
        # 2. Devolver el número
        return {
            'success': True,
            'count': cantidad
        }
        
    except Exception as error:
        error_generico(
            funcion='contar_pendientes',
            detalle=f'Error al contar notificaciones pendientes: {str(error)}',
            severidad='medio',
            archivo='controllers/notifications_controller.py',
            tipo_especifico='Error Controlador Notificaciones'
        )
        print(f"❌ Error en controlador - contar pendientes: {error}")
        return {
            'success': False,
            'count': 0
        }


@capturar_error(modulo='notificaciones', severidad='medio')
def cambiar_estado(id_notificacion, nuevo_estado):
    """
    Cambia el estado de una notificación.
    Por ejemplo: 'pendiente' → 'en revisión' → 'resuelto'
    
    Parámetros:
        id_notificacion: ID de la notificación
        nuevo_estado: Nuevo estado a aplicar
    
    Retorna: Diccionario indicando si funcionó o no
    """
    try:
        # 1. Validar que el estado sea válido
        estados_validos = ['pendiente', 'en revision', 'resuelto']

        if nuevo_estado not in estados_validos:
            return {
                'success': False,
                'message': f'Estado no válido. Usa: {", ".join(estados_validos)}'
            }

        # 2. Cambiar el estado en la base de datos
        exito = cambiar_estado_notificacion(id_notificacion, nuevo_estado)

        # 3. Devolver resultado
        if exito:
            return {
                'success': True,
                'message': f'Estado cambiado a: {nuevo_estado}'
            }
        else:
            return {
                'success': False,
                'message': 'No se pudo cambiar el estado'
            }

    except Exception as error:
        print(f"❌ Error en controlador - cambiar estado: {error}")
        return {
            'success': False,
            'message': 'Error al cambiar el estado'
        }


@capturar_error(modulo='notificaciones', severidad='alto')
def eliminar(id_notificacion):
    """
    Elimina una notificación específica.
    
    Parámetros:
        id_notificacion: ID de la notificación a eliminar
    
    Retorna: Diccionario indicando si se eliminó correctamente
    """
    try:
        # 1. Eliminar la notificación
        exito = eliminar_notificacion(id_notificacion)
        
        # 2. Devolver resultado
        if exito:
            return {
                'success': True,
                'message': 'Notificación eliminada correctamente'
            }
        else:
            return {
                'success': False,
                'message': 'No se pudo eliminar la notificación'
            }
            
    except Exception as error:
        print(f"❌ Error en controlador - eliminar: {error}")
        return {
            'success': False,
            'message': 'Error al eliminar la notificación'
        }


@capturar_error(modulo='notificaciones', severidad='alto')
def marcar_todas_resueltas():
    """
    Marca TODAS las notificaciones como resueltas.
    Es útil para limpiar todas las alertas de golpe.
    
    Retorna: Diccionario indicando si funcionó
    """
    try:
        # 1. Marcar todas como resueltas
        exito = marcar_todas_como_resueltas()
        
        # 2. Devolver resultado
        if exito:
            return {
                'success': True,
                'message': 'Todas las notificaciones marcadas como resueltas'
            }
        else:
            return {
                'success': False,
                'message': 'No se pudieron marcar como resueltas'
            }
            
    except Exception as error:
        print(f"❌ Error en controlador - marcar todas resueltas: {error}")
        return {
            'success': False,
            'message': 'Error al marcar las notificaciones'
        }


@capturar_error(modulo='notificaciones', severidad='alto')
def eliminar_todas():
    """
    Elimina TODAS las notificaciones del sistema.
    ⚠️ Cuidado: Esta acción no se puede deshacer.
    
    Retorna: Diccionario indicando si funcionó
    """
    try:
        # 1. Eliminar todas
        exito = eliminar_todas_las_notificaciones()
        
        # 2. Devolver resultado
        if exito:
            return {
                'success': True,
                'message': 'Todas las notificaciones eliminadas'
            }
        else:
            return {
                'success': False,
                'message': 'No se pudieron eliminar las notificaciones'
            }
            
    except Exception as error:
        print(f"❌ Error en controlador - eliminar todas: {error}")
        return {
            'success': False,
            'message': 'Error al eliminar las notificaciones'
        }


@capturar_error(modulo='notificaciones', severidad='alto')
def eliminar_resueltas():
    """
    Elimina solo las notificaciones que ya están resueltas.
    Sirve para limpiar el historial sin perder las pendientes.
    
    Retorna: Diccionario indicando si funcionó
    """
    try:
        # 1. Eliminar las resueltas
        exito = eliminar_notificaciones_resueltas()
        
        # 2. Devolver resultado
        if exito:
            return {
                'success': True,
                'message': 'Notificaciones resueltas eliminadas'
            }
        else:
            return {
                'success': False,
                'message': 'No se pudieron eliminar las notificaciones resueltas'
            }
            
    except Exception as error:
        print(f"❌ Error en controlador - eliminar resueltas: {error}")
        return {
            'success': False,
            'message': 'Error al eliminar las notificaciones resueltas'
        }


@capturar_error(modulo='notificaciones', severidad='medio')
def obtener_datos_para_pagina():
    """
    Obtiene todos los datos necesarios para mostrar la página de notificaciones.
    Incluye: todas las notificaciones + el conteo de pendientes.
    
    Retorna: Diccionario con alertas y conteo
    """
    try:
        # 1. Obtener todas las notificaciones
        todas_notificaciones = obtener_todas_las_notificaciones()
        
        # 2. Contar cuántas están pendientes
        cantidad_pendientes = contar_notificaciones_pendientes()
        
        # 3. Devolver todo junto
        return {
            'alertas': todas_notificaciones,
            'unread_count': cantidad_pendientes
        }
        
    except Exception as error:
        error_generico(
            funcion='obtener_datos_para_pagina',
            detalle=f'Error al obtener datos para la página: {str(error)}',
            severidad='alto',
            archivo='controllers/notifications_controller.py',
            tipo_especifico='Error Controlador Notificaciones'
        )
        print(f"❌ Error en controlador - obtener datos página: {error}")
        return {
            'alertas': [],
            'unread_count': 0
        }


@capturar_error(modulo='notificaciones', severidad='medio')
def obtener_vista_previa(limite=5):
    """
    Obtiene una vista previa de las últimas notificaciones.
    Se usa para mostrar en el dropdown del menú.
    
    Parámetros:
        limite: Cuántas notificaciones mostrar (por defecto 5)
    
    Retorna: Diccionario con las últimas notificaciones formateadas
    """
    try:
        # 1. Obtener todas las notificaciones pendientes
        todas = obtener_notificaciones_pendientes()
        
        # 2. Tomar solo las primeras (según el límite)
        vista_previa = todas[:limite] if todas else []
        
        # 3. Formatear las notificaciones para el frontend
        notificaciones_formateadas = []
        for notif in vista_previa:
            # Determinar icono según severidad
            icon = 'fa-info-circle'
            if notif['severidad'] == 'critico':
                icon = 'fa-times-circle'
            elif notif['severidad'] == 'alto':
                icon = 'fa-exclamation-triangle'
            elif notif['severidad'] == 'medio':
                icon = 'fa-exclamation-circle'
            
            # Calcular tiempo transcurrido
            from datetime import datetime
            fecha = notif['fecha']
            ahora = datetime.now()
            diferencia = ahora - fecha
            segundos = diferencia.total_seconds()
            
            if segundos < 60:
                tiempo = 'Hace un momento'
            elif segundos < 3600:
                minutos = int(segundos / 60)
                tiempo = f'Hace {minutos} min'
            elif segundos < 86400:
                horas = int(segundos / 3600)
                tiempo = f'Hace {horas} hora{"s" if horas > 1 else ""}'
            else:
                dias = diferencia.days
                tiempo = f'Hace {dias} día{"s" if dias > 1 else ""}'
            
            notificaciones_formateadas.append({
                'id': notif['id_alerta'],
                'icon': icon,
                'title': f"[{notif['modulo'].upper()}] {notif['tipo_error']}",
                # No truncar aquí: dejar la descripción completa; la presentación debe manejar el recorte
                'text': notif['descripcion'],
                'time': tiempo,
                'severidad': notif['severidad'],
                'is_unread': notif['estado'] != 'resuelto'
            })
        
        # 4. Devolver resultado
        return {
            'success': True,
            'notifications': notificaciones_formateadas,
            'total': len(todas)
        }
        
    except Exception as error:
        error_generico(
            funcion='obtener_vista_previa',
            detalle=f'Error al obtener vista previa: {str(error)}',
            severidad='medio',
            archivo='controllers/notifications_controller.py',
            tipo_especifico='Error Controlador Notificaciones'
        )
        print(f"❌ Error en controlador - vista previa: {error}")
        return {
            'success': False,
            'notifications': [],
            'total': 0
        }
