from shared.models.vista_model import VistaModel


class EstadisticasControllerAPI:

    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas desde la vista SQL y devuelve un dict listo para JSON.

        Retorna {'status': int, 'data': dict} o {'status': int, 'error': str}.
        """
        try:
            stats = VistaModel.obtener_estadisticas()
        except Exception as e:
            return {"status": 500, "error": f"Error al obtener estadísticas: {str(e)}"}

        if not stats:
            return {"status": 404, "error": "No hay estadísticas disponibles"}

        return {"status": 200, "data": stats}
