from models.reportes_models import (
    get_all_reportes as model_get_all_reportes,
    get_reporte_by_id as model_get_reporte_by_id,
    get_reportes_by_estado as model_get_reportes_by_estado,
    count_reportes_pendientes as model_count_reportes_pendientes,
    update_estado_reporte as model_update_estado_reporte,
    delete_reporte as model_delete_reporte,
    delete_all_resolved as model_delete_all_resolved,
    get_reportes_paginated as model_get_reportes_paginated,
    count_reportes as model_count_reportes
)
import math
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
def get_page_data(estado=None, page=1, per_page=10):
    """Obtiene todos los datos necesarios para la página de reportes.

    - `estado` (str|None): filtro opcional por estado.
    - `page` (int): número de página 1-based.
    - `per_page` (int): elementos por página.

    Devuelve reportes paginados y estadísticas globales. Además incluye metadata
    de paginación para la UI.
    """
    # Estadísticas globales (calcular sobre todos los reportes)
    all_reportes = model_get_all_reportes()
    pendientes = model_count_reportes_pendientes()

    en_revision = len([r for r in all_reportes if r['estado'] == 'en revision'])
    resueltos = len([r for r in all_reportes if r['estado'] == 'resuelto'])

    # Conteo filtrado (para la paginación)
    total_filtered = model_count_reportes(estado)

    # Obtener reportes a mostrar: paginados
    reportes = model_get_reportes_paginated(page=page, per_page=per_page, estado=estado)

    total_pages = math.ceil(total_filtered / per_page) if per_page and total_filtered else 1

    return {
        'reportes': reportes,
        'stats': {
            'pendientes': pendientes,
            'en_revision': en_revision,
            'resueltos': resueltos,
            'total': len(all_reportes)
        },
        'pagination': {
            'current_page': int(page),
            'per_page': int(per_page),
            'total_pages': int(total_pages),
            'total_items': int(total_filtered)
        }
    }
