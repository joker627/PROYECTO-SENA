"""
Controlador para el manejo de notificaciones del sistema
"""
from models.notification_models import NotificationModel
from utils.error_handler import ErrorHandler


class NotificationController:
    """Controlador para manejar la lógica de negocio de notificaciones"""
    
    @staticmethod
    def get_all_notifications():
        """Obtener todas las notificaciones con formato para API"""
        try:
            alerts = NotificationModel.get_all_alerts()
            
            notifications = []
            for alert in alerts:
                notifications.append({
                    'id': alert['id_alerta'],
                    'modulo': alert['modulo'],
                    'tipo_error': alert['tipo_error'],
                    'severidad': alert['severidad'],
                    'descripcion': alert['descripcion'],
                    'estado': alert['estado'],
                    'created_at': alert['fecha'].strftime('%Y-%m-%d %H:%M:%S') if alert['fecha'] else None,
                    'id_responsable': alert['id_responsable'],
                    'title': f"[{alert['modulo'].upper()}] {alert['tipo_error']}",
                    'message': alert['descripcion'],
                    'type': NotificationController._get_alert_type(alert),
                    'is_read': alert['estado'] == 'resuelto'
                })
            
            return {'success': True, 'notifications': notifications}
            
        except Exception as e:
            ErrorHandler.error_generico('get_all_notifications', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error Controlador Notificaciones')
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_unread_notifications(limit=10):
        """Obtener notificaciones no resueltas"""
        try:
            alerts = NotificationModel.get_unresolved_alerts(limit)
            
            notifications = []
            for alert in alerts:
                notifications.append({
                    'id': alert['id_alerta'],
                    'modulo': alert['modulo'],
                    'tipo_error': alert['tipo_error'],
                    'severidad': alert['severidad'],
                    'descripcion': alert['descripcion'],
                    'created_at': alert['fecha'].strftime('%Y-%m-%d %H:%M:%S') if alert['fecha'] else None,
                    'title': f"[{alert['modulo'].upper()}] {alert['tipo_error']}",
                    'message': alert['descripcion'],
                    'type': NotificationController._get_alert_type(alert)
                })
            
            return {
                'success': True,
                'count': len(notifications),
                'notifications': notifications
            }
            
        except Exception as e:
            ErrorHandler.error_generico('get_unread_notifications', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en get_unread_notifications')
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_unread_count():
        """Obtener conteo de notificaciones no resueltas"""
        try:
            count = NotificationModel.count_unresolved_alerts()
            
            print(f"[NOTIFICACIONES] Conteo de alertas NO resueltas: {count}")
            
            return {'success': True, 'count': count}
            
        except Exception as e:
            ErrorHandler.error_generico('get_unread_count', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en get_unread_count')
            print(f"[ERROR] Error al contar alertas: {str(e)}")
            return {'success': False, 'error': str(e), 'count': 0}
    
    @staticmethod
    def get_notifications_preview(limit=5):
        """Obtener vista previa de notificaciones para dropdown"""
        try:
            alerts = NotificationModel.get_unresolved_alerts(limit)
            
            preview_list = []
            for alert in alerts:
                # Determinar icono según severidad
                if alert['severidad'] == 'crítico':
                    icon = 'fa-times-circle'
                    icon_class = 'error'
                elif alert['severidad'] == 'alto':
                    icon = 'fa-exclamation-triangle'
                    icon_class = 'warning'
                else:
                    icon = 'fa-info-circle'
                    icon_class = 'info'
                
                # Calcular tiempo transcurrido
                tiempo = NotificationModel.calculate_time_ago(alert['fecha'])
                
                # Truncar descripción
                text = alert['descripcion'][:80] + '...' if len(alert['descripcion']) > 80 else alert['descripcion']
                
                preview_list.append({
                    'id': alert['id_alerta'],
                    'title': f"[{alert['modulo'].upper()}] {alert['tipo_error']}",
                    'text': text,
                    'time': tiempo,
                    'icon': icon,
                    'icon_class': icon_class,
                    'is_unread': alert['estado'] != 'resuelto',
                    'severidad': alert['severidad']
                })
            
            return {'success': True, 'notifications': preview_list}
            
        except Exception as e:
            ErrorHandler.error_generico('get_notifications_preview', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en get_notifications_preview')
            print(f"[ERROR] Error al obtener preview: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def change_notification_status(notification_id, new_status):
        """Cambiar el estado de una notificación"""
        # Validar el estado
        valid_statuses = ['pendiente', 'en revisión', 'resuelto']
        if not new_status or new_status not in valid_statuses:
            return {'success': False, 'message': 'Estado no válido'}
        
        try:
            success = NotificationModel.update_status(notification_id, new_status)
            
            if success:
                return {'success': True, 'message': f'Estado cambiado a: {new_status.upper()}'}
            else:
                return {'success': False, 'message': 'Alerta no encontrada'}
                
        except Exception as e:
            ErrorHandler.error_generico('change_notification_status', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en change_notification_status')
            return {'success': False, 'message': f'Error al cambiar estado: {str(e)}'}
    
    @staticmethod
    def delete_notification(notification_id):
        """Eliminar una notificación"""
        try:
            success = NotificationModel.delete_alert(notification_id)
            
            if success:
                return {'success': True, 'message': 'Alerta eliminada correctamente'}
            else:
                return {'success': False, 'message': 'Alerta no encontrada'}
                
        except Exception as e:
            ErrorHandler.error_generico('delete_notification', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en delete_notification')
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def get_page_data():
        """Obtener datos para la página de notificaciones"""
        try:
            alertas = NotificationModel.get_all_alerts()
            unread_count = NotificationModel.count_unresolved_alerts()
            
            print(f"[NOTIFICACIONES] Total de alertas: {len(alertas)}")
            print(f"[NOTIFICACIONES] Conteo de alertas NO resueltas: {unread_count}")
            
            return {
                'alertas': alertas,
                'unread_count': unread_count
            }
            
        except Exception as e:
            ErrorHandler.error_generico('get_page_data', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en get_page_data')
            print(f"[ERROR] Error al cargar datos de página: {str(e)}")
            return {
                'alertas': [],
                'unread_count': 0
            }
    
    @staticmethod
    def mark_all_as_resolved():
        """Marcar todas las alertas pendientes como resueltas"""
        try:
            result = NotificationModel.mark_all_as_resolved()
            
            if result:
                return {
                    'success': True,
                    'message': f'Todas las alertas han sido marcadas como resueltas'
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudieron actualizar las alertas'
                }
        except Exception as e:
            ErrorHandler.error_generico('mark_all_as_resolved', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en mark_all_as_resolved')
            print(f"[ERROR] Error al marcar todas como resueltas: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    @staticmethod
    def delete_all_notifications():
        """Eliminar todas las alertas del sistema"""
        try:
            count = NotificationModel.delete_all_notifications()
            
            if count > 0:
                return {
                    'success': True,
                    'message': f'Se eliminaron {count} alerta{"s" if count != 1 else ""} correctamente'
                }
            else:
                return {
                    'success': False,
                    'message': 'No hay alertas para eliminar'
                }
        except Exception as e:
            ErrorHandler.error_generico('delete_all_notifications', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en delete_all_notifications')
            print(f"[ERROR] Error al eliminar todas las alertas: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    @staticmethod
    def delete_all_resolved():
        """Eliminar todas las alertas resueltas"""
        try:
            count = NotificationModel.delete_all_resolved()
            
            if count > 0:
                return {
                    'success': True,
                    'message': f'Se eliminaron {count} alerta{"s" if count != 1 else ""} resuelta{"s" if count != 1 else ""}'
                }
            else:
                return {
                    'success': False,
                    'message': 'No hay alertas resueltas para eliminar'
                }
        except Exception as e:
            ErrorHandler.error_generico('delete_all_resolved', f'Error: {str(e)}', 'alto', 'controllers/notifications_controller.py', 'Error en delete_all_resolved')
            print(f"[ERROR] Error al eliminar alertas resueltas: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    @staticmethod
    def _get_alert_type(alert):
        """Determinar el tipo de alerta para iconos/estilos"""
        if alert['severidad'] == 'crítico':
            return 'error'
        elif alert['severidad'] == 'alto':
            return 'warning'
        elif alert['estado'] == 'resuelto':
            return 'success'
        else:
            return 'info'
