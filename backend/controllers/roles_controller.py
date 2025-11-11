"""Controller: roles - thin wrapper around models for routes"""
from backend.models.roles_models import get_all_roles, get_role_by_id, create_role, update_role, delete_role


def list_roles():
    return get_all_roles()


def retrieve_role(id_rol):
    return get_role_by_id(id_rol)


def add_role(data):
    nombre = data.get('nombre_rol')
    if not nombre:
        return None
    return create_role(nombre)


def edit_role(id_rol, data):
    nombre = data.get('nombre_rol')
    if not nombre:
        return False
    return update_role(id_rol, nombre)


def remove_role(id_rol):
    return delete_role(id_rol)
