from flask import Blueprint, jsonify, request
from models.RolesModel import Roles
from services.RolesService import RolesService

roles_api = Blueprint('roles', __name__)
roles_service = RolesService()


@roles_api.get('/')
def get_all_roles():
    roles = roles_service.get_all_roles()

    if isinstance(roles, str):
        return roles, 404
    else:
        return jsonify(roles), 200


@roles_api.get('/<int:role_id>')
def get_role_by_id(role_id: int):
    role = roles_service.get_role_by_id(role_id)

    if isinstance(role, str):
        return role, 404
    else:
        return jsonify(role), 200


@roles_api.post('/')
def create_role():
    role = roles_service.map_role(request.json)
    if not isinstance(role, Roles):
        return jsonify(role), 400

    new_role = roles_service.create_role(role)

    if isinstance(new_role, str):
        return new_role, 400
    else:
        return jsonify(new_role), 201


@roles_api.put('/<int:role_id>')
def update_role(role_id: int):
    role = roles_service.map_role(request.json)
    if not isinstance(role, Roles):
        return jsonify(role), 400

    updated_role = roles_service.update_role(role_id, role)

    if isinstance(updated_role, str):
        return updated_role, 400
    else:
        return jsonify(updated_role), 200


@roles_api.delete('/<int:role_id>')
def delete_role(role_id: int):
    deleted_role = roles_service.delete_role(role_id)

    if isinstance(deleted_role, str):
        return deleted_role, 400
    else:
        return jsonify(deleted_role), 200
