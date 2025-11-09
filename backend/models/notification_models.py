"""
Modelo para el manejo de alertas del sistema
"""
from connection.db import get_connection
import pymysql
from datetime import datetime


class NotificationModel:
    """Modelo para interactuar con la tabla alertas_sistema"""
    
    @staticmethod
    def get_all_alerts():
        """Obtener todas las alertas del sistema ordenadas por severidad"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        id_alerta,
                        modulo,
                        tipo_error,
                        severidad,
                        descripcion,
                        estado,
                        fecha,
                        id_responsable
                    FROM alertas_sistema
                    ORDER BY 
                        CASE severidad 
                            WHEN 'crítico' THEN 1
                            WHEN 'alto' THEN 2
                            WHEN 'medio' THEN 3
                            WHEN 'bajo' THEN 4
                        END,
                        fecha DESC
                """)
                
                return cursor.fetchall()
                
        except pymysql.Error as e:
            print(f"[ERROR] Error al obtener alertas: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def get_unresolved_alerts(limit=None):
        """Obtener alertas NO resueltas (pendientes y en revisión)"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        id_alerta,
                        modulo,
                        tipo_error,
                        severidad,
                        descripcion,
                        estado,
                        fecha
                    FROM alertas_sistema
                    WHERE estado != 'resuelto'
                    ORDER BY 
                        CASE severidad 
                            WHEN 'crítico' THEN 1
                            WHEN 'alto' THEN 2
                            WHEN 'medio' THEN 3
                            WHEN 'bajo' THEN 4
                        END,
                        fecha DESC
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query)
                return cursor.fetchall()
                
        except pymysql.Error as e:
            print(f"[ERROR] Error al obtener alertas no resueltas: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def count_unresolved_alerts():
        """Contar alertas NO resueltas"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM alertas_sistema
                    WHERE estado != 'resuelto'
                """)
                
                result = cursor.fetchone()
                return result['count'] if result else 0
                
        except pymysql.Error as e:
            print(f"[ERROR] Error al contar alertas: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def update_status(alert_id, new_status):
        """Actualizar el estado de una alerta"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE alertas_sistema
                    SET estado = %s
                    WHERE id_alerta = %s
                """, (new_status, alert_id))
                
                connection.commit()
                return cursor.rowcount > 0
                
        except pymysql.Error as e:
            connection.rollback()
            print(f"[ERROR] Error al actualizar estado: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def delete_alert(alert_id):
        """Eliminar una alerta"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM alertas_sistema
                    WHERE id_alerta = %s
                """, (alert_id,))
                
                connection.commit()
                return cursor.rowcount > 0
                
        except pymysql.Error as e:
            connection.rollback()
            print(f"[ERROR] Error al eliminar alerta: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def mark_all_as_resolved():
        """Marcar todas las alertas pendientes como resueltas"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE alertas_sistema
                    SET estado = 'resuelto',
                        fecha_resolucion = NOW()
                    WHERE estado != 'resuelto'
                """)
                
                connection.commit()
                affected_rows = cursor.rowcount
                print(f"[NOTIFICACIONES] Marcadas {affected_rows} alertas como resueltas")
                return affected_rows > 0
                
        except pymysql.Error as e:
            connection.rollback()
            print(f"[ERROR] Error al marcar todas como resueltas: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def delete_all_notifications():
        """Eliminar todas las alertas del sistema"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                # Primero obtener el conteo
                cursor.execute("SELECT COUNT(*) as count FROM alertas_sistema")
                count = cursor.fetchone()['count']
                
                # Eliminar todas
                cursor.execute("DELETE FROM alertas_sistema")
                
                connection.commit()
                print(f"[NOTIFICACIONES] Eliminadas {count} alertas del sistema")
                return count
                
        except pymysql.Error as e:
            connection.rollback()
            print(f"[ERROR] Error al eliminar todas las alertas: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def delete_all_resolved():
        """Eliminar todas las alertas resueltas"""
        connection = get_connection()
        
        try:
            with connection.cursor() as cursor:
                # Primero obtener el conteo
                cursor.execute("SELECT COUNT(*) as count FROM alertas_sistema WHERE estado = 'resuelto'")
                count = cursor.fetchone()['count']
                
                # Eliminar todas las resueltas
                cursor.execute("DELETE FROM alertas_sistema WHERE estado = 'resuelto'")
                
                connection.commit()
                print(f"[NOTIFICACIONES] Eliminadas {count} alertas resueltas")
                return count
                
        except pymysql.Error as e:
            connection.rollback()
            print(f"[ERROR] Error al eliminar alertas resueltas: {str(e)}")
            raise
        finally:
            connection.close()
    
    @staticmethod
    def calculate_time_ago(fecha):
        """Calcular el tiempo transcurrido desde una fecha"""
        ahora = datetime.now()
        diferencia = ahora - fecha
        
        if diferencia.total_seconds() < 60:
            return 'Hace un momento'
        elif diferencia.total_seconds() < 3600:
            minutos = int(diferencia.total_seconds() / 60)
            return f'Hace {minutos} min' if minutos > 1 else 'Hace 1 min'
        elif diferencia.total_seconds() < 86400:
            horas = int(diferencia.total_seconds() / 3600)
            return f'Hace {horas} hora{"s" if horas > 1 else ""}'
        else:
            dias = diferencia.days
            return f'Hace {dias} día{"s" if dias > 1 else ""}'
