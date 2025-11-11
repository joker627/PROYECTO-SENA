from flask import Blueprint, jsonify, request, redirect, url_for
from backend.controllers.reportes_controller import list_reportes, retrieve_reporte, add_reporte, edit_reporte, remove_reporte
from connection.db import get_connection

reportes_bp = Blueprint('reportes_bp', __name__)


@reportes_bp.route('/api/reportes', methods=['GET'])
def api_list_reportes():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    return jsonify(list_reportes(limit, offset))


@reportes_bp.route('/api/reportes/<int:id_reporte>', methods=['GET'])
def api_get_reporte(id_reporte):
    r = retrieve_reporte(id_reporte)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@reportes_bp.route('/api/reportes', methods=['POST'])
def api_create_reporte():
    data = request.get_json() or {}
    new_id = add_reporte(data)
    if not new_id:
        return jsonify({'error': 'Bad request'}), 400
    return jsonify({'id_reporte': new_id}), 201


@reportes_bp.route('/api/reportes/<int:id_reporte>', methods=['PUT'])
def api_update_reporte(id_reporte):
    data = request.get_json() or {}
    ok = edit_reporte(id_reporte, data)
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@reportes_bp.route('/api/reportes/<int:id_reporte>', methods=['DELETE'])
def api_delete_reporte(id_reporte):
    ok = remove_reporte(id_reporte)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})


@reportes_bp.route('/reportes/page')
def reportes_page():
    """Compatibility endpoint: templates call `url_for('reportes_bp.reportes_page', ...)`.

    Redirect to the admin page provided by `general_bp.admin_reportes`, preserving
    any query parameters like 'estado', 'page', or 'per_page'. This avoids
    duplicating the admin view while keeping old template links valid.
    """
    # preserve query string parameters
    params = request.args.to_dict(flat=True)
    target = url_for('general_bp.admin_reportes')
    if params:
        qs = '&'.join(f"{k}={v}" for k, v in params.items())
        target = f"{target}?{qs}"
    return redirect(target)


@reportes_bp.route('/reportes/<int:id_reporte>/eliminar', methods=['POST'])
def eliminar_reporte(id_reporte):
    """Delete a single reporte and redirect back to admin page."""
    try:
        remove_reporte(id_reporte)
    except Exception:
        # ignore errors for compatibility
        pass
    return redirect(url_for('general_bp.admin_reportes'))


@reportes_bp.route('/reportes/<int:id_reporte>/marcar_revision', methods=['POST'])
def marcar_revision(id_reporte):
    """Mark a report as 'en_revision'."""
    try:
        edit_reporte(id_reporte, {'estado': 'en_revision'})
    except Exception:
        pass
    return redirect(url_for('general_bp.admin_reportes'))


@reportes_bp.route('/reportes/<int:id_reporte>/resolver', methods=['POST'])
def resolver_reporte(id_reporte):
    """Mark a report as 'resuelto'."""
    try:
        edit_reporte(id_reporte, {'estado': 'resuelto'})
    except Exception:
        pass
    return redirect(url_for('general_bp.admin_reportes'))


@reportes_bp.route('/reportes/eliminar_resueltos', methods=['POST'])
def eliminar_resueltos():
    """Bulk-delete all resolved reports. This is a small compatibility helper."""
    conn = None
    try:
        conn = get_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM reportes_errores WHERE estado = 'resuelto'")
                conn.commit()
    except Exception:
        pass
    finally:
        if conn:
            conn.close()
    return redirect(url_for('general_bp.admin_reportes'))
