from models.solicitudes_models import (
    get_all_solicitudes as model_get_all_solicitudes,
    get_solicitud_by_id,
    count_solicitudes_pendientes,
    update_estado_solicitud,
    create_user_from_solicitud,
    delete_solicitud as model_delete_solicitud,
    calculate_time_ago
)
from utils.error_handler import capturar_error


@capturar_error(modulo='solicitudes', severidad='medio')
def get_all_solicitudes():
    # Obtener y formatear solicitudes con tiempo relativo y clase CSS
    solicitudes = model_get_all_solicitudes()
    for solicitud in solicitudes:
        solicitud['time_ago'] = calculate_time_ago(solicitud['fecha'])
        solicitud['estado_class'] = {
            'pendiente': 'pending',
            'aceptado': 'completed',
            'rechazado': 'rejected'
        }.get(solicitud['estado'], 'pending')
    return solicitudes


@capturar_error(modulo='solicitudes', severidad='medio')
def get_solicitud_detail(id_solicitud):
    # Detalle de una solicitud específica
    solicitud = get_solicitud_by_id(id_solicitud)
    if solicitud:
        solicitud['time_ago'] = calculate_time_ago(solicitud['fecha'])
        solicitud['estado_class'] = {
            'pendiente': 'pending',
            'aceptado': 'completed',
            'rechazado': 'rejected'
        }.get(solicitud['estado'], 'pending')
    return solicitud


@capturar_error(modulo='solicitudes', severidad='medio')
def get_pending_count():
    # Contar solicitudes pendientes
    return count_solicitudes_pendientes()


@capturar_error(modulo='solicitudes', severidad='alto')
def accept_solicitud(id_solicitud, id_revisor):
    # Aceptar solicitud: actualiza estado, crea usuario GESTOR y elimina solicitud
    success = update_estado_solicitud(id_solicitud, 'aceptado', id_revisor)
    if success:
        user_created = create_user_from_solicitud(id_solicitud)
        if user_created:
            model_delete_solicitud(id_solicitud)
            print(f"✅ Solicitud {id_solicitud} aceptada, usuario creado y solicitud eliminada")
        else:
            print(f"⚠️ Solicitud {id_solicitud} aceptada pero usuario no creado (posible duplicado)")
    return success


@capturar_error(modulo='solicitudes', severidad='alto')
def reject_solicitud(id_solicitud, id_revisor, motivo_rechazo=None):
    # Rechazar solicitud con motivo y eliminarla
    success = update_estado_solicitud(id_solicitud, 'rechazado', id_revisor, motivo_rechazo)
    if success:
        model_delete_solicitud(id_solicitud)
        print(f"🗑️ Solicitud {id_solicitud} rechazada y eliminada")
    return success


@capturar_error(modulo='solicitudes', severidad='alto')
def delete_solicitud(id_solicitud):
    # Eliminar solicitud manualmente
    return model_delete_solicitud(id_solicitud)


@capturar_error(modulo='solicitudes', severidad='medio')
def get_page_data(page=1, per_page=10, estado_filter=None, orden='reciente'):
    # Obtener solicitudes con paginación, filtros y ordenamiento
    solicitudes = get_all_solicitudes()
    
    # Filtrar por estado si se especifica
    if estado_filter:
        solicitudes = [s for s in solicitudes if s['estado'] == estado_filter]
    
    # Ordenar: reciente (desc) o antigua (asc)
    if orden == 'reciente':
        solicitudes = sorted(solicitudes, key=lambda x: x.get('fecha', ''), reverse=True)
    elif orden == 'antigua':
        solicitudes = sorted(solicitudes, key=lambda x: x.get('fecha', ''), reverse=False)
    
    # Calcular paginación
    total = len(solicitudes)
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    # Paginar resultados
    start = (page - 1) * per_page
    end = start + per_page
    solicitudes_paginadas = solicitudes[start:end]
    
    return {
        'solicitudes': solicitudes_paginadas,
        'pending_count': get_pending_count(),
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
    }
