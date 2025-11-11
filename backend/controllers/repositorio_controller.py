"""Controller: repositorio_senas"""
from models.repositorio_models import get_all_senas, get_sena_by_id, create_sena, update_sena, delete_sena

def list_senas(limit=100, offset=0):
    return get_all_senas(limit, offset)


def retrieve_sena(id_sena):
    return get_sena_by_id(id_sena)


def add_sena(data):
    return create_sena(data)


def edit_sena(id_sena, data):
    return update_sena(id_sena, data)


def remove_sena(id_sena):
    return delete_sena(id_sena)
