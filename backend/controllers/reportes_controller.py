from models.reportes_models import ReportesModels

class ReportesController:
    
    @staticmethod
    def get_all_reportes():
        """Obtiene todos los reportes con formato"""
        reportes = ReportesModels.get_all_reportes()
        return reportes
    
    @staticmethod
    def get_reporte_detail(id_reporte):
        """Obtiene detalle de un reporte específico"""
        reporte = ReportesModels.get_reporte_by_id(id_reporte)
        return reporte
    
    @staticmethod
    def get_reportes_by_estado(estado):
        """Obtiene reportes filtrados por estado"""
        reportes = ReportesModels.get_reportes_by_estado(estado)
        return reportes
    
    @staticmethod
    def get_pending_count():
        """Obtiene el conteo de reportes pendientes"""
        count = ReportesModels.count_reportes_pendientes()
        return count
    
    @staticmethod
    def mark_as_revision(id_reporte):
        """Marca un reporte como 'en revisión'"""
        success = ReportesModels.update_estado_reporte(id_reporte, 'en revisión')
        return success
    
    @staticmethod
    def mark_as_resolved(id_reporte):
        """Marca un reporte como resuelto"""
        success = ReportesModels.update_estado_reporte(id_reporte, 'resuelto')
        return success
    
    @staticmethod
    def delete_reporte(id_reporte):
        """Elimina un reporte"""
        success = ReportesModels.delete_reporte(id_reporte)
        return success
    
    @staticmethod
    def delete_all_resolved():
        """Elimina todos los reportes resueltos"""
        count = ReportesModels.delete_all_resolved()
        return count
    
    @staticmethod
    def get_page_data():
        """Obtiene todos los datos necesarios para la página de reportes"""
        reportes = ReportesModels.get_all_reportes()
        pendientes = ReportesModels.count_reportes_pendientes()
        
        # Contar por estado
        en_revision = len([r for r in reportes if r['estado'] == 'en revisión'])
        resueltos = len([r for r in reportes if r['estado'] == 'resuelto'])
        
        return {
            'reportes': reportes,
            'stats': {
                'pendientes': pendientes,
                'en_revision': en_revision,
                'resueltos': resueltos,
                'total': len(reportes)
            }
        }
