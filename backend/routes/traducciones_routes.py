from flask import Blueprint, jsonify, request
from ..controllers.traducciones_controller import list_traducciones, retrieve_traduccion, add_traduccion, edit_traduccion, remove_traduccion

traducciones_bp = Blueprint('traducciones_bp', __name__)


@traducciones_bp.route('/api/traducciones', methods=['GET'])
def api_list_traducciones():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    return jsonify(list_traducciones(limit, offset))


@traducciones_bp.route('/api/traducciones/<int:id_traduccion>', methods=['GET'])
def api_get_traduccion(id_traduccion):
    r = retrieve_traduccion(id_traduccion)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@traducciones_bp.route('/api/traducciones', methods=['POST'])
def api_create_traduccion():
    data = request.get_json() or {}
    new_id = add_traduccion(data)
    if not new_id:
        return jsonify({'error': 'Bad request'}), 400
    return jsonify({'id_traduccion': new_id}), 201


@traducciones_bp.route('/api/traducciones/<int:id_traduccion>', methods=['PUT'])
def api_update_traduccion(id_traduccion):
    data = request.get_json() or {}
    ok = edit_traduccion(id_traduccion, data)
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@traducciones_bp.route('/api/traducciones/<int:id_traduccion>', methods=['DELETE'])
def api_delete_traduccion(id_traduccion):
    ok = remove_traduccion(id_traduccion)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})
