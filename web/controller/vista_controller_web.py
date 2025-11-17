from web.models.vista_model import VistaModel


class VistaControllerWeb:
    """Controlador que expone métodos para obtener vistas/estadísticas
    agregadas definidas en `VistaModel`. Usado por las rutas del panel admin.
    """

    @staticmethod
    def obtener_estadisticas():
        return VistaModel.obtener_estadisticas()
