from flask import Blueprint, jsonify, request
from controllers.repositorio_controller import list_senas, retrieve_sena, add_sena, edit_sena, remove_sena

repositorio_bp = Blueprint('repositorio_bp', __name__)


@repositorio_bp.route('/api/repositorio', methods=['GET'])
def api_list_senas():
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    return jsonify(list_senas(limit, offset))


@repositorio_bp.route('/api/repositorio/<int:id_sena>', methods=['GET'])
def api_get_sena(id_sena):
    r = retrieve_sena(id_sena)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@repositorio_bp.route('/api/repositorio', methods=['POST'])
def api_create_sena():
    data = request.get_json() or {}
    new_id = add_sena(data)
    if not new_id:
        return jsonify({'error': 'Bad request'}), 400
    return jsonify({'id_sena': new_id}), 201


@repositorio_bp.route('/api/repositorio/<int:id_sena>', methods=['PUT'])
def api_update_sena(id_sena):
    data = request.get_json() or {}
    ok = edit_sena(id_sena, data)
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@repositorio_bp.route('/api/repositorio/<int:id_sena>', methods=['DELETE'])
def api_delete_sena(id_sena):
    ok = remove_sena(id_sena)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})
