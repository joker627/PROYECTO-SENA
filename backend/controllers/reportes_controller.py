"""Controller: reportes_errores"""
from models.reportes_models import get_all_reportes, get_reporte_by_id, create_reporte, update_reporte, delete_reporte


def list_reportes(limit=100, offset=0):
    return get_all_reportes(limit, offset)


def retrieve_reporte(id_reporte):
    return get_reporte_by_id(id_reporte)


def add_reporte(data):
    return create_reporte(data)


def edit_reporte(id_reporte, data):
    return update_reporte(id_reporte, data)


def remove_reporte(id_reporte):
    return delete_reporte(id_reporte)
