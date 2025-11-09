from models.solicitudes_models import SolicitudesModel


class SolicitudesController:
    
    @staticmethod
    def get_all_solicitudes():
        # Obtener y formatear solicitudes con tiempo relativo y clase CSS
        solicitudes = SolicitudesModel.get_all_solicitudes()
        
        for solicitud in solicitudes:
            solicitud['time_ago'] = SolicitudesModel.calculate_time_ago(solicitud['fecha'])
            solicitud['estado_class'] = {
                'pendiente': 'pending',
                'aceptado': 'completed',
                'rechazado': 'rejected'
            }.get(solicitud['estado'], 'pending')
        
        return solicitudes
    
    @staticmethod
    def get_solicitud_detail(id_solicitud):
        # Detalle de una solicitud específica
        solicitud = SolicitudesModel.get_solicitud_by_id(id_solicitud)
        
        if solicitud:
            solicitud['time_ago'] = SolicitudesModel.calculate_time_ago(solicitud['fecha'])
            solicitud['estado_class'] = {
                'pendiente': 'pending',
                'aceptado': 'completed',
                'rechazado': 'rejected'
            }.get(solicitud['estado'], 'pending')
        
        return solicitud
    
    @staticmethod
    def get_pending_count():
        # Contar solicitudes pendientes
        return SolicitudesModel.count_solicitudes_pendientes()
    
    @staticmethod
    def accept_solicitud(id_solicitud, id_revisor):
        # Aceptar solicitud: actualiza estado, crea usuario GESTOR y elimina solicitud
        success = SolicitudesModel.update_estado_solicitud(id_solicitud, 'aceptado', id_revisor)
        
        if success:
            user_created = SolicitudesModel.create_user_from_solicitud(id_solicitud)
            
            if user_created:
                SolicitudesModel.delete_solicitud(id_solicitud)
                print(f"✅ Solicitud {id_solicitud} aceptada, usuario creado y solicitud eliminada")
            else:
                print(f"⚠️ Solicitud {id_solicitud} aceptada pero usuario no creado (posible duplicado)")
        
        return success
    
    @staticmethod
    def reject_solicitud(id_solicitud, id_revisor, motivo_rechazo=None):
        # Rechazar solicitud con motivo y eliminarla
        success = SolicitudesModel.update_estado_solicitud(id_solicitud, 'rechazado', id_revisor, motivo_rechazo)
        
        if success:
            SolicitudesModel.delete_solicitud(id_solicitud)
            print(f"🗑️ Solicitud {id_solicitud} rechazada y eliminada")
        
        return success
    
    @staticmethod
    def delete_solicitud(id_solicitud):
        # Eliminar solicitud manualmente
        return SolicitudesModel.delete_solicitud(id_solicitud)
    
    @staticmethod
    def get_page_data(page=1, per_page=10, estado_filter=None, orden='reciente'):
        # Obtener solicitudes con paginación, filtros y ordenamiento
        solicitudes = SolicitudesController.get_all_solicitudes()
        
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
            'pending_count': SolicitudesController.get_pending_count(),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_prev': page > 1,
                'has_next': page < total_pages
            }
        }
