"""
Modelo para el Dashboard - Consultas de métricas del sistema
"""

from connection.db import get_connection
from datetime import datetime, timedelta
from utils.error_handler import ErrorHandler


class DashboardModel:
    """Modelo para obtener métricas y estadísticas del dashboard"""
    
    @staticmethod
    def get_total_users():
        """Obtener total de usuarios registrados"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM usuarios WHERE estado = 'ACTIVO'")
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_total_users', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_total_users: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_users_growth():
        """Obtener crecimiento de usuarios en el último mes"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                # Usuarios del mes actual
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM usuarios 
                    WHERE fecha_registro >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    AND estado = 'ACTIVO'
                """)
                current_month = cursor.fetchone()['total']
                
                # Usuarios del mes anterior
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM usuarios 
                    WHERE fecha_registro >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
                    AND fecha_registro < DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    AND estado = 'ACTIVO'
                """)
                previous_month = cursor.fetchone()['total']
                
                # Calcular porcentaje de crecimiento
                if previous_month == 0:
                    return 100 if current_month > 0 else 0
                
                growth = ((current_month - previous_month) / previous_month) * 100
                return round(growth, 1)
        except Exception as e:
            ErrorHandler.error_db('get_users_growth', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_users_growth: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_total_contributions():
        """Obtener total de contribuciones de señas validadas"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM contribuciones_senas WHERE estado = 'validada'")
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_total_contributions', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_total_contributions: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_contributions_growth():
        """Obtener crecimiento de contribuciones en el último mes"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                # Contribuciones del mes actual
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM contribuciones_senas 
                    WHERE fecha >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    AND estado = 'validada'
                """)
                current_month = cursor.fetchone()['total']
                
                # Contribuciones del mes anterior
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM contribuciones_senas 
                    WHERE fecha >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
                    AND fecha < DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    AND estado = 'validada'
                """)
                previous_month = cursor.fetchone()['total']
                
                if previous_month == 0:
                    return 100 if current_month > 0 else 0
                
                growth = ((current_month - previous_month) / previous_month) * 100
                return round(growth, 1)
        except Exception as e:
            ErrorHandler.error_db('get_contributions_growth', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_contributions_growth: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_pending_reports():
        """Obtener reportes de error pendientes"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM reportes_error WHERE estado = 'pendiente'")
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_pending_reports', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_pending_reports: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_reports_growth():
        """Obtener cambio en reportes pendientes (negativo = mejora)"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                # Reportes pendientes actuales
                cursor.execute("SELECT COUNT(*) as total FROM reportes_error WHERE estado = 'pendiente'")
                current = cursor.fetchone()['total']
                
                # Reportes del mes anterior (total generados)
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM reportes_error 
                    WHERE fecha >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                """)
                this_month = cursor.fetchone()['total']
                
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM reportes_error 
                    WHERE fecha >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
                    AND fecha < DATE_SUB(NOW(), INTERVAL 1 MONTH)
                """)
                last_month = cursor.fetchone()['total']
                
                if last_month == 0:
                    return 0
                
                change = ((this_month - last_month) / last_month) * 100
                return round(change, 1)
        except Exception as e:
            ErrorHandler.error_db('get_reports_growth', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_reports_growth: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_system_alerts():
        """Obtener alertas del sistema no resueltas"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM alertas_sistema WHERE estado != 'resuelto'")
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_system_alerts', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_system_alerts: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_pending_solicitudes():
        """Obtener solicitudes de colaboración pendientes"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM solicitudes_colaboracion WHERE estado = 'pendiente'")
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_pending_solicitudes', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_pending_solicitudes: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_total_translations():
        """Obtener total de traducciones realizadas"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM traducciones_senas_texto) +
                        (SELECT COUNT(*) FROM traducciones_texto_senas) as total
                """)
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_total_translations', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_total_translations: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_translations_growth():
        """Obtener crecimiento de traducciones en el último mes"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                # Traducciones del mes actual
                cursor.execute("""
                    SELECT COUNT(*) as total FROM (
                        SELECT fecha FROM traducciones_senas_texto 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                        UNION ALL
                        SELECT fecha FROM traducciones_texto_senas 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    ) as traducciones_mes
                """)
                current_month = cursor.fetchone()['total']
                
                # Traducciones del mes anterior
                cursor.execute("""
                    SELECT COUNT(*) as total FROM (
                        SELECT fecha FROM traducciones_senas_texto 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
                        AND fecha < DATE_SUB(NOW(), INTERVAL 1 MONTH)
                        UNION ALL
                        SELECT fecha FROM traducciones_texto_senas 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 2 MONTH)
                        AND fecha < DATE_SUB(NOW(), INTERVAL 1 MONTH)
                    ) as traducciones_mes_anterior
                """)
                previous_month = cursor.fetchone()['total']
                
                if previous_month == 0:
                    return 100 if current_month > 0 else 0
                
                growth = ((current_month - previous_month) / previous_month) * 100
                return round(growth, 1)
        except Exception as e:
            ErrorHandler.error_db('get_translations_growth', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_translations_growth: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_total_anonymous_users():
        """Obtener total de usuarios anónimos registrados"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM usuarios_anonimos")
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_total_anonymous_users', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_total_anonymous_users: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_average_precision():
        """Obtener precisión promedio del modelo"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT AVG(precision_modelo) as promedio 
                    FROM traducciones_senas_texto
                    WHERE precision_modelo IS NOT NULL
                """)
                result = cursor.fetchone()
                return round(result['promedio'], 2) if result and result['promedio'] else 0
        except Exception as e:
            ErrorHandler.error_db('get_average_precision', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_average_precision: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_colaboradores_count():
        """Obtener total de colaboradores activos"""
        connection = get_connection()
        if not connection:
            return 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) as total 
                    FROM usuarios 
                    WHERE id_rol = 2 AND estado = 'ACTIVO'
                """)
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            ErrorHandler.error_db('get_colaboradores_count', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_colaboradores_count: {e}")
            return 0
        finally:
            connection.close()
    
    @staticmethod
    def get_recent_activity(limit=5):
        """Obtener actividad reciente del sistema"""
        connection = get_connection()
        if not connection:
            return []
        
        try:
            activities = []
            
            with connection.cursor() as cursor:
                # Usuarios recientes
                cursor.execute("""
                    SELECT nombre, fecha_registro as fecha, 'user' as tipo
                    FROM usuarios 
                    WHERE estado = 'ACTIVO'
                    ORDER BY fecha_registro DESC 
                    LIMIT 3
                """)
                users = cursor.fetchall()
                for user in users:
                    activities.append({
                        'tipo': 'user',
                        'icon': 'fa-user-plus',
                        'descripcion': f'Nuevo usuario registrado: <strong>{user["nombre"]}</strong>',
                        'fecha': user['fecha']
                    })
                
                # Contribuciones recientes
                cursor.execute("""
                    SELECT c.descripcion, c.fecha, u.nombre
                    FROM contribuciones_senas c
                    JOIN usuarios u ON c.id_colaborador = u.id_usuario
                    WHERE c.estado = 'validada'
                    ORDER BY c.fecha DESC 
                    LIMIT 3
                """)
                contributions = cursor.fetchall()
                for contrib in contributions:
                    activities.append({
                        'tipo': 'contribution',
                        'icon': 'fa-check-circle',
                        'descripcion': f'Contribución validada: <strong>{contrib["descripcion"][:50]}...</strong>',
                        'fecha': contrib['fecha']
                    })
                
                # Reportes recientes
                cursor.execute("""
                    SELECT tipo_error, fecha
                    FROM reportes_error
                    ORDER BY fecha DESC 
                    LIMIT 2
                """)
                reports = cursor.fetchall()
                for report in reports:
                    activities.append({
                        'tipo': 'report',
                        'icon': 'fa-exclamation-triangle',
                        'descripcion': f'Reporte de error: <strong>{report["tipo_error"]}</strong>',
                        'fecha': report['fecha']
                    })
                
                # Alertas recientes
                cursor.execute("""
                    SELECT tipo_error, fecha
                    FROM alertas_sistema
                    WHERE estado = 'pendiente'
                    ORDER BY fecha DESC 
                    LIMIT 2
                """)
                alerts = cursor.fetchall()
                for alert in alerts:
                    activities.append({
                        'tipo': 'alert',
                        'icon': 'fa-bell',
                        'descripcion': f'Alerta del sistema: <strong>{alert["tipo_error"]}</strong>',
                        'fecha': alert['fecha']
                    })
            
            # Ordenar por fecha y limitar
            activities.sort(key=lambda x: x['fecha'], reverse=True)
            return activities[:limit]
            
        except Exception as e:
            ErrorHandler.error_db('get_recent_activity', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_recent_activity: {e}")
            return []
        finally:
            connection.close()
    
    @staticmethod
    def get_weekly_stats():
        """Obtener estadísticas de uso semanal (traducciones)"""
        connection = get_connection()
        if not connection:
            return {'labels': [], 'values': []}
        
        try:
            with connection.cursor() as cursor:
                # Obtener traducciones de los últimos 7 días
                cursor.execute("""
                    SELECT 
                        DATE(fecha) as dia,
                        COUNT(*) as total
                    FROM (
                        SELECT fecha FROM traducciones_senas_texto 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                        UNION ALL
                        SELECT fecha FROM traducciones_texto_senas 
                        WHERE fecha >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                    ) as todas_traducciones
                    GROUP BY DATE(fecha)
                    ORDER BY dia ASC
                """)
                results = cursor.fetchall()
                
                # Crear estructura para los últimos 7 días
                days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
                values = []
                
                # Obtener día de la semana actual
                today = datetime.now()
                
                # Crear diccionario de resultados
                data_dict = {row['dia']: row['total'] for row in results}
                
                # Llenar valores para los últimos 7 días
                for i in range(6, -1, -1):
                    day = today - timedelta(days=i)
                    date_key = day.date()
                    values.append(data_dict.get(date_key, 0))
                
                return {'labels': days, 'values': values}
                
        except Exception as e:
            ErrorHandler.error_db('get_weekly_stats', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_weekly_stats: {e}")
            return {'labels': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'], 'values': [0, 0, 0, 0, 0, 0, 0]}
        finally:
            connection.close()
    
    @staticmethod
    def get_recent_projects():
        """Obtener proyectos/contribuciones recientes"""
        connection = get_connection()
        if not connection:
            return []
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        c.id_contribucion,
                        c.descripcion,
                        c.estado,
                        c.fecha,
                        u.nombre as colaborador
                    FROM contribuciones_senas c
                    JOIN usuarios u ON c.id_colaborador = u.id_usuario
                    ORDER BY c.fecha DESC
                    LIMIT 3
                """)
                results = cursor.fetchall()
                
                projects = []
                for row in results:
                    # Mapear estado a español
                    status_map = {
                        'validada': {'text': 'Completado', 'class': 'completed'},
                        'pendiente': {'text': 'Pendiente', 'class': 'pending'},
                        'rechazada': {'text': 'Rechazado', 'class': 'rejected'}
                    }
                    status = status_map.get(row['estado'], {'text': 'Desconocido', 'class': 'pending'})
                    
                    projects.append({
                        'id': row['id_contribucion'],
                        'titulo': row['descripcion'][:50] + ('...' if len(row['descripcion']) > 50 else ''),
                        'descripcion': row['descripcion'],
                        'estado': status['text'],
                        'estado_class': status['class'],
                        'fecha': row['fecha'].strftime('%d %b %Y'),
                        'colaborador': row['colaborador']
                    })
                
                return projects
                
        except Exception as e:
            ErrorHandler.error_db('get_recent_projects', f'Error: {str(e)}', 'models/dashboard_models.py')
            print(f"Error en get_recent_projects: {e}")
            return []
        finally:
            connection.close()
    
    @staticmethod
    def calculate_time_ago(fecha):
        """Calcular tiempo transcurrido desde una fecha"""
        if not fecha:
            return "Fecha desconocida"
        
        now = datetime.now()
        diff = now - fecha
        
        if diff.days > 365:
            years = diff.days // 365
            return f"Hace {years} año{'s' if years > 1 else ''}"
        elif diff.days > 30:
            months = diff.days // 30
            return f"Hace {months} mes{'es' if months > 1 else ''}"
        elif diff.days > 0:
            return f"Hace {diff.days} día{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"Hace {hours} hora{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"Hace {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "Hace un momento"

