from flask import Blueprint, jsonify, request
from ..controllers.contribuciones_controller import list_contribuciones, retrieve_contribucion, add_contribucion, edit_contribucion, remove_contribucion

contribuciones_bp = Blueprint('contribuciones_bp', __name__)


@contribuciones_bp.route('/api/contribuciones', methods=['GET'])
def api_list_contribuciones():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    return jsonify(list_contribuciones(limit, offset))


@contribuciones_bp.route('/api/contribuciones/<int:id_contribucion>', methods=['GET'])
def api_get_contribucion(id_contribucion):
    r = retrieve_contribucion(id_contribucion)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@contribuciones_bp.route('/api/contribuciones', methods=['POST'])
def api_create_contribucion():
    data = request.get_json() or {}
    new_id = add_contribucion(data)
    if not new_id:
        return jsonify({'error': 'Bad request'}), 400
    return jsonify({'id_contribucion': new_id}), 201


@contribuciones_bp.route('/api/contribuciones/<int:id_contribucion>', methods=['PUT'])
def api_update_contribucion(id_contribucion):
    data = request.get_json() or {}
    ok = edit_contribucion(id_contribucion, data)
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@contribuciones_bp.route('/api/contribuciones/<int:id_contribucion>', methods=['DELETE'])
def api_delete_contribucion(id_contribucion):
    ok = remove_contribucion(id_contribucion)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})
