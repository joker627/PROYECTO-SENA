from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from ..controllers.solicitudes_controller import list_solicitudes, retrieve_solicitud, add_solicitud, edit_solicitud, remove_solicitud

solicitudes_bp = Blueprint('solicitudes_bp', __name__)


@solicitudes_bp.route('/solicitudes')
def solicitudes_page():
    """Compatibility endpoint: builds a simple page URL for solicitues lists.

    Some templates or code may call url_for('solicitudes_bp.solicitudes_page', orden=...)
    expecting a page route. We redirect to the admin page provided by
    `general_bp.admin_solicitudes` while preserving the optional 'orden'
    query parameter.
    """
    orden = request.args.get('orden')
    target = url_for('general_bp.admin_solicitudes')
    if orden:
        target = f"{target}?orden={orden}"
    return redirect(target)

@solicitudes_bp.route('/admin/solicitudes/page')
def solicitudes_page_admin():
    return render_template('admin/solicitudes.html')

@solicitudes_bp.route('/api/solicitudes', methods=['GET'])
def api_list_solicitudes():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    return jsonify(list_solicitudes(limit, offset))


@solicitudes_bp.route('/api/solicitudes/<int:id_solicitud>', methods=['GET'])
def api_get_solicitud(id_solicitud):
    r = retrieve_solicitud(id_solicitud)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@solicitudes_bp.route('/api/solicitudes', methods=['POST'])
def api_create_solicitud():
    data = request.get_json() or {}
    new_id = add_solicitud(data)
    if not new_id:
        return jsonify({'error': 'Bad request'}), 400
    return jsonify({'id_solicitud': new_id}), 201


@solicitudes_bp.route('/api/solicitudes/<int:id_solicitud>', methods=['PUT'])
def api_update_solicitud(id_solicitud):
    data = request.get_json() or {}
    ok = edit_solicitud(id_solicitud, data)
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@solicitudes_bp.route('/api/solicitudes/<int:id_solicitud>', methods=['DELETE'])
def api_delete_solicitud(id_solicitud):
    ok = remove_solicitud(id_solicitud)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})
