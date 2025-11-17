from web.config.db import get_db_connection


class VistaModel:
    """
    Modelo para acceder a la vista SQL `vista_estadisticas`.
    """

    @staticmethod
    def obtener_estadisticas():
        """Consulta la vista `vista_estadisticas` y devuelve un diccionario.

        Retorna un dict con las columnas definidas en la vista o un diccionario
        vacío si no hay resultados.
        """
        conn = get_db_connection()
        try:
            query = "SELECT * FROM vista_estadisticas"
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        finally:
            conn.close()

        return result or {}
