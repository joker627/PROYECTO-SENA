"""Controller: traducciones"""
from models.traducciones_models import get_all_traducciones, get_traduccion_by_id, create_traduccion, update_traduccion, delete_traduccion

def list_traducciones(limit=100, offset=0):
    return get_all_traducciones(limit, offset)


def retrieve_traduccion(id_traduccion):
    return get_traduccion_by_id(id_traduccion)


def add_traduccion(data):
    return create_traduccion(data)


def edit_traduccion(id_traduccion, data):
    return update_traduccion(id_traduccion, data)


def remove_traduccion(id_traduccion):
    return delete_traduccion(id_traduccion)
