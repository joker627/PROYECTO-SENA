"""Controller: contribuciones"""
from models.contribuciones_models import get_all_contribuciones, get_contribucion_by_id, create_contribucion, update_contribucion, delete_contribucion

def list_contribuciones(limit=100, offset=0):
    return get_all_contribuciones(limit, offset)


def retrieve_contribucion(id_contribucion):
    return get_contribucion_by_id(id_contribucion)


def add_contribucion(data):
    return create_contribucion(data)


def edit_contribucion(id_contribucion, data):
    return update_contribucion(id_contribucion, data)


def remove_contribucion(id_contribucion):
    return delete_contribucion(id_contribucion)
