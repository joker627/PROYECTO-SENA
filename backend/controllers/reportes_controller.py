from models.reportes_models import (
    get_all_reportes as model_get_all_reportes,
    get_reporte_by_id as model_get_reporte_by_id,
    get_reportes_by_estado as model_get_reportes_by_estado,
    count_reportes_pendientes as model_count_reportes_pendientes,
    update_estado_reporte as model_update_estado_reporte,
    delete_reporte as model_delete_reporte,
    delete_all_resolved as model_delete_all_resolved
)
from utils.error_handler import capturar_error


@capturar_error(modulo='reportes', severidad='medio')
def get_all_reportes():
    """Obtiene todos los reportes con formato"""
    reportes = model_get_all_reportes()
    return reportes


@capturar_error(modulo='reportes', severidad='medio')
def get_reporte_detail(id_reporte):
    """Obtiene detalle de un reporte específico"""
    reporte = model_get_reporte_by_id(id_reporte)
    return reporte


@capturar_error(modulo='reportes', severidad='medio')
def get_reportes_by_estado(estado):
    """Obtiene reportes filtrados por estado"""
    reportes = model_get_reportes_by_estado(estado)
    return reportes


@capturar_error(modulo='reportes', severidad='medio')
def get_pending_count():
    """Obtiene el conteo de reportes pendientes"""
    count = model_count_reportes_pendientes()
    return count


@capturar_error(modulo='reportes', severidad='alto')
def mark_as_revision(id_reporte):
    """Marca un reporte como 'en revisión'"""
    success = model_update_estado_reporte(id_reporte, 'en revision')
    return success


@capturar_error(modulo='reportes', severidad='alto')
def mark_as_resolved(id_reporte):
    """Marca un reporte como resuelto"""
    success = model_update_estado_reporte(id_reporte, 'resuelto')
    return success


@capturar_error(modulo='reportes', severidad='alto')
def delete_reporte(id_reporte):
    """Elimina un reporte"""
    success = model_delete_reporte(id_reporte)
    return success


@capturar_error(modulo='reportes', severidad='alto')
def delete_all_resolved():
    """Elimina todos los reportes resueltos"""
    count = model_delete_all_resolved()
    return count


@capturar_error(modulo='reportes', severidad='medio')
def get_page_data():
    """Obtiene todos los datos necesarios para la página de reportes"""
    reportes = model_get_all_reportes()
    pendientes = model_count_reportes_pendientes()
    
    # Contar por estado
    en_revision = len([r for r in reportes if r['estado'] == 'en revision'])
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
