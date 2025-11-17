from web.config.db import get_db_connection

class VistaModel:
    @staticmethod
    def obtener_estadisticas():
        conn = get_db_connection()
        try:
            query = "SELECT * FROM vista_estadisticas"
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        finally:
            conn.close()

        return result or {}
