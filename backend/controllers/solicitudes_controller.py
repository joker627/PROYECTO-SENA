"""Controller: solicitudes_colaborador"""
from models.solicitudes_models import get_all_solicitudes, get_solicitud_by_id, create_solicitud, update_solicitud, delete_solicitud


def list_solicitudes(limit=100, offset=0):
    return get_all_solicitudes(limit, offset)


def retrieve_solicitud(id_solicitud):
    return get_solicitud_by_id(id_solicitud)


def add_solicitud(data):
    return create_solicitud(data)


def edit_solicitud(id_solicitud, data):
    return update_solicitud(id_solicitud, data)


def remove_solicitud(id_solicitud):
    return delete_solicitud(id_solicitud)
