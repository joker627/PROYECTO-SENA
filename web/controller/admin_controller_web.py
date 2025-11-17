from web.models.contribucion_model import ContribucionModel
from web.models.reporte_model import ReporteModel


class AdminControllerWeb:
    """Controlador administrativo centralizado para operaciones sobre
    contribuciones y reportes. Contiene lógica de negocio usada por las rutas
    del panel de administración.
    """

    # Contribuciones
    @staticmethod
    def obtener_contribuciones_pendientes():
        return ContribucionModel.listar_pendientes()

    @staticmethod
    def aprobar_contribucion(id_contribucion):
        return ContribucionModel.aprobar(id_contribucion)

    @staticmethod
    def eliminar_contribucion(id_contribucion):
        return ContribucionModel.eliminar(id_contribucion)

    # Reportes
    @staticmethod
    def obtener_reportes(estado=None):
        return ReporteModel.listar(estado)

    @staticmethod
    def poner_reporte_en_revision(id_reporte):
        return ReporteModel.marcar_en_revision(id_reporte)

    @staticmethod
    def eliminar_reporte(id_reporte):
        return ReporteModel.eliminar(id_reporte)
