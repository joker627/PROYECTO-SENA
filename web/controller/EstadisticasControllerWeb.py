from shared.models.vista_model import VistaModel


class EstadisticasControllerWeb:
    @staticmethod
    def obtener_estadisticas():
        try:
            stats = VistaModel.obtener_estadisticas()
            return {"status": 200, "data": stats}
        except Exception as e:
            return {"status": 500, "error": str(e)}
