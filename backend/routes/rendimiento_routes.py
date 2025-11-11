from flask import Blueprint, jsonify, request
from controllers.rendimiento_controller import get_rendimiento,add_rendimiento,edit_rendimiento,\
remove_rendimiento


rendimiento_bp = Blueprint('rendimiento_bp', __name__)


@rendimiento_bp.route('/api/rendimiento', methods=['GET'])
def api_get_rendimiento():
    r = get_rendimiento()
    if not r:
        return jsonify({}), 200
    return jsonify(r)


@rendimiento_bp.route('/api/rendimiento', methods=['POST'])
def api_create_rendimiento():
    data = request.get_json() or {}
    precision = data.get('precision_actual')
    obs = data.get('observaciones')
    if precision is None:
        return jsonify({'error': 'precision_actual required'}), 400
    new_id = add_rendimiento(precision, obs)
    return jsonify({'id_rendimiento': new_id}), 201


@rendimiento_bp.route('/api/rendimiento/<int:id_rendimiento>', methods=['PUT'])
def api_update_rendimiento(id_rendimiento):
    data = request.get_json() or {}
    ok = edit_rendimiento(id_rendimiento, data.get('precision_actual'), data.get('observaciones'))
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@rendimiento_bp.route('/api/rendimiento/<int:id_rendimiento>', methods=['DELETE'])
def api_delete_rendimiento(id_rendimiento):
    ok = remove_rendimiento(id_rendimiento)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})
