"""Controller: rendimiento_modelo"""
from models.rendimiento_models import get_latest_rendimiento, create_rendimiento, update_rendimiento, delete_rendimiento


def get_rendimiento():
    return get_latest_rendimiento()


def add_rendimiento(precision_actual, observaciones=None):
    return create_rendimiento(precision_actual, observaciones)


def edit_rendimiento(id_rendimiento, precision_actual=None, observaciones=None):
    return update_rendimiento(id_rendimiento, precision_actual, observaciones)


def remove_rendimiento(id_rendimiento):
    return delete_rendimiento(id_rendimiento)
