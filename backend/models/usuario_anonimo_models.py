from connection.db import get_connection
from pymysql.cursors import DictCursor
from utils.error_handler import ErrorHandler
import uuid
from datetime import datetime


class UsuarioAnonimoModel:
    
    @staticmethod
    def crear_usuario_anonimo(ip_usuario=None):
        """Crear nuevo usuario anónimo con UUID único"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(DictCursor)
            
            # Generar UUID único
            uuid_transaccion = str(uuid.uuid4())
            
            query = """
                INSERT INTO usuarios_anonimos (uuid_transaccion, ip_usuario)
                VALUES (%s, %s)
            """
            
            cursor.execute(query, (uuid_transaccion, ip_usuario))
            connection.commit()
            
            id_anonimo = cursor.lastrowid
            
            return {
                'success': True,
                'id_anonimo': id_anonimo,
                'uuid_transaccion': uuid_transaccion
            }
            
        except Exception as e:
            if connection:
                connection.rollback()
            
            # Registrar error en el sistema
            ErrorHandler.error_db(
                funcion='crear_usuario_anonimo',
                detalle=f'Error al crear usuario anónimo: {str(e)}',
                archivo='models/usuario_anonimo_models.py'
            )
            
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    
    @staticmethod
    def obtener_por_uuid(uuid_transaccion):
        """Obtener usuario anónimo por UUID"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(DictCursor)
            
            query = """
                SELECT id_anonimo, uuid_transaccion, ip_usuario, fecha_creacion
                FROM usuarios_anonimos
                WHERE uuid_transaccion = %s
            """
            
            cursor.execute(query, (uuid_transaccion,))
            usuario = cursor.fetchone()
            
            return usuario
            
        except Exception as e:
            ErrorHandler.error_db(
                funcion='obtener_por_uuid',
                detalle=f'Error al obtener usuario por UUID: {str(e)}',
                archivo='models/usuario_anonimo_models.py'
            )
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    
    @staticmethod
    def obtener_por_id(id_anonimo):
        """Obtener usuario anónimo por ID"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(DictCursor)
            
            query = """
                SELECT id_anonimo, uuid_transaccion, ip_usuario, fecha_creacion
                FROM usuarios_anonimos
                WHERE id_anonimo = %s
            """
            
            cursor.execute(query, (id_anonimo,))
            usuario = cursor.fetchone()
            
            return usuario
            
        except Exception as e:
            ErrorHandler.error_db(
                funcion='obtener_por_id',
                detalle=f'Error al obtener usuario por ID: {str(e)}',
                archivo='models/usuario_anonimo_models.py'
            )
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    
    @staticmethod
    def obtener_todos(limite=100, offset=0):
        """Obtener todos los usuarios anónimos con paginación"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(DictCursor)
            
            query = """
                SELECT id_anonimo, uuid_transaccion, ip_usuario, fecha_creacion
                FROM usuarios_anonimos
                ORDER BY fecha_creacion DESC
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, (limite, offset))
            usuarios = cursor.fetchall()
            
            # Obtener total
            cursor.execute("SELECT COUNT(*) as total FROM usuarios_anonimos")
            total = cursor.fetchone()['total']
            
            return {
                'usuarios': usuarios,
                'total': total
            }
            
        except Exception as e:
            ErrorHandler.error_db(
                funcion='obtener_todos',
                detalle=f'Error al obtener lista de usuarios anónimos: {str(e)}',
                archivo='models/usuario_anonimo_models.py'
            )
            return {
                'usuarios': [],
                'total': 0
            }
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    
    @staticmethod
    def obtener_estadisticas():
        """Obtener estadísticas de usuarios anónimos"""
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor(DictCursor)
            
            # Total de usuarios anónimos
            cursor.execute("SELECT COUNT(*) as total FROM usuarios_anonimos")
            total = cursor.fetchone()['total']
            
            # Usuarios hoy
            cursor.execute("""
                SELECT COUNT(*) as hoy 
                FROM usuarios_anonimos 
                WHERE DATE(fecha_creacion) = CURDATE()
            """)
            hoy = cursor.fetchone()['hoy']
            
            # Usuarios esta semana
            cursor.execute("""
                SELECT COUNT(*) as semana 
                FROM usuarios_anonimos 
                WHERE YEARWEEK(fecha_creacion, 1) = YEARWEEK(CURDATE(), 1)
            """)
            semana = cursor.fetchone()['semana']
            
            # Usuarios este mes
            cursor.execute("""
                SELECT COUNT(*) as mes 
                FROM usuarios_anonimos 
                WHERE MONTH(fecha_creacion) = MONTH(CURDATE()) 
                AND YEAR(fecha_creacion) = YEAR(CURDATE())
            """)
            mes = cursor.fetchone()['mes']
            
            return {
                'total': total,
                'hoy': hoy,
                'semana': semana,
                'mes': mes
            }
            
        except Exception as e:
            ErrorHandler.error_db(
                funcion='obtener_estadisticas',
                detalle=f'Error al obtener estadísticas de usuarios anónimos: {str(e)}',
                archivo='models/usuario_anonimo_models.py'
            )
            return {
                'total': 0,
                'hoy': 0,
                'semana': 0,
                'mes': 0
            }
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
