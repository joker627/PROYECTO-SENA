"""
Modelo para la gestión de usuarios del sistema
"""
from connection.db import get_connection
import pymysql
from datetime import datetime
from utils.error_handler import ErrorHandler


class UsuariosModel:
    """Modelo para interactuar con la tabla usuarios"""
    
    @staticmethod
    def get_all_usuarios():
        """Obtener todos los usuarios del sistema"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        u.id_usuario,
                        u.nombre,
                        u.correo,
                        u.id_rol,
                        r.nombre as rol,
                        u.fecha_registro,
                        u.ultimo_acceso,
                        u.estado
                    FROM usuarios u
                    LEFT JOIN roles r ON u.id_rol = r.id_rol
                    ORDER BY u.fecha_registro DESC
                """
                cursor.execute(query)
                usuarios = cursor.fetchall()
                
                # Calcular tiempo desde último acceso
                for usuario in usuarios:
                    if usuario['ultimo_acceso']:
                        usuario['tiempo_ultimo_acceso'] = UsuariosModel.calculate_time_ago(usuario['ultimo_acceso'])
                    else:
                        usuario['tiempo_ultimo_acceso'] = 'Nunca'
                    
                    if usuario['fecha_registro']:
                        usuario['tiempo_registro'] = UsuariosModel.calculate_time_ago(usuario['fecha_registro'])
                    else:
                        usuario['tiempo_registro'] = 'Desconocido'
                
                return usuarios
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            ErrorHandler.error_db('get_all_usuarios', f'Error en consulta: {str(e)}', 'models/usuarios_models.py')
            return []
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def get_usuario_by_id(id_usuario):
        """Obtener un usuario específico por ID"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        id_usuario,
                        nombre,
                        correo,
                        rol,
                        fecha_registro,
                        ultimo_acceso,
                        estado
                    FROM usuarios
                    WHERE id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            ErrorHandler.error_db('get_usuario_by_id', f'Error: {str(e)}', 'models/usuarios_models.py')
            return None
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def create_usuario(nombre, correo, contrasena_hash, id_rol):
        """Crear un nuevo usuario"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO usuarios (nombre, correo, contrasena, id_rol, fecha_registro, estado)
                    VALUES (%s, %s, %s, %s, NOW(), 'ACTIVO')
                """
                cursor.execute(query, (nombre, correo, contrasena_hash, id_rol))
                connection.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError as e:
            if connection:
                connection.rollback()
            print(f"Error de integridad al crear usuario: {e}")
            return None
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error al crear usuario: {e}")
            ErrorHandler.error_db('create_usuario', f'Error: {str(e)}', 'models/usuarios_models.py')
            return None
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def update_usuario(id_usuario, nombre=None, correo=None, id_rol=None, estado=None):
        """Actualizar información de un usuario"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                updates = []
                params = []
                
                if nombre:
                    updates.append("nombre = %s")
                    params.append(nombre)
                if correo:
                    updates.append("correo = %s")
                    params.append(correo)
                if id_rol:
                    updates.append("id_rol = %s")
                    params.append(id_rol)
                if estado:
                    updates.append("estado = %s")
                    params.append(estado)
                
                if not updates:
                    return False
                
                params.append(id_usuario)
                query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id_usuario = %s"
                
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error al actualizar usuario: {e}")
            ErrorHandler.error_db('update_usuario', f'Error: {str(e)}', 'models/usuarios_models.py')
            return False
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def delete_usuario(id_usuario):
        """Eliminar un usuario"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(query, (id_usuario,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Error al eliminar usuario: {e}")
            ErrorHandler.error_db('delete_usuario', f'Error: {str(e)}', 'models/usuarios_models.py')
            return False
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def change_estado(id_usuario, nuevo_estado):
        """Cambiar el estado de un usuario (ACTIVO/INACTIVO/ELIMINADO)"""
        return UsuariosModel.update_usuario(id_usuario, estado=nuevo_estado)
    
    @staticmethod
    def change_rol(id_usuario, nuevo_rol):
        """Cambiar el rol de un usuario usando id_rol"""
        return UsuariosModel.update_usuario(id_usuario, id_rol=nuevo_rol)
    
    @staticmethod
    def count_by_rol():
        """Contar usuarios por rol"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        r.nombre as rol,
                        COUNT(*) as total
                    FROM usuarios u
                    LEFT JOIN roles r ON u.id_rol = r.id_rol
                    WHERE u.estado != 'ELIMINADO'
                    GROUP BY r.nombre
                """
                cursor.execute(query)
                results = cursor.fetchall()
                
                counts = {'ADMINISTRADOR': 0, 'GESTOR': 0}
                for row in results:
                    if row['rol']:
                        counts[row['rol']] = row['total']
                
                return counts
        except Exception as e:
            print(f"Error al contar usuarios por rol: {e}")
            return {'ADMINISTRADOR': 0, 'GESTOR': 0}
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def count_by_estado():
        """Contar usuarios por estado"""
        connection = None
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        estado,
                        COUNT(*) as total
                    FROM usuarios
                    WHERE estado != 'ELIMINADO'
                    GROUP BY estado
                """
                cursor.execute(query)
                results = cursor.fetchall()
                
                counts = {'ACTIVO': 0, 'INACTIVO': 0}
                for row in results:
                    if row['estado'] in counts:
                        counts[row['estado']] = row['total']
                
                return counts
        except Exception as e:
            print(f"Error al contar usuarios por estado: {e}")
            return {'ACTIVO': 0, 'INACTIVO': 0}
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def calculate_time_ago(fecha):
        """Calcular el tiempo transcurrido desde una fecha"""
        if not fecha:
            return "Fecha no disponible"
        
        now = datetime.now()
        diff = now - fecha
        
        if diff.days > 365:
            years = diff.days // 365
            return f"hace {years} año{'s' if years > 1 else ''}"
        elif diff.days > 30:
            months = diff.days // 30
            return f"hace {months} mes{'es' if months > 1 else ''}"
        elif diff.days > 0:
            return f"hace {diff.days} día{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"hace {hours} hora{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "hace un momento"
