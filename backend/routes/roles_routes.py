from flask import Blueprint, jsonify, request
from controllers.roles_controller import list_roles,retrieve_role,add_role,edit_role,remove_role

roles_bp = Blueprint('roles_bp', __name__)


@roles_bp.route('/api/roles', methods=['GET'])
def api_list_roles():
    return jsonify(list_roles())


@roles_bp.route('/api/roles/<int:id_rol>', methods=['GET'])
def api_get_role(id_rol):
    r = retrieve_role(id_rol)
    if not r:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(r)


@roles_bp.route('/api/roles', methods=['POST'])
def api_create_role():
    data = request.get_json() or {}
    new_id = add_role(data)
    if not new_id:
        return jsonify({'error': 'Bad request'}), 400
    return jsonify({'id_rol': new_id}), 201


@roles_bp.route('/api/roles/<int:id_rol>', methods=['PUT'])
def api_update_role(id_rol):
    data = request.get_json() or {}
    ok = edit_role(id_rol, data)
    if not ok:
        return jsonify({'error': 'Bad request or not found'}), 400
    return jsonify({'ok': True})


@roles_bp.route('/api/roles/<int:id_rol>', methods=['DELETE'])
def api_delete_role(id_rol):
    ok = remove_role(id_rol)
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})
