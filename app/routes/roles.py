from flask import Blueprint, jsonify, request
from app.models import Roles
from app.services import RolesService

roles_api = Blueprint("roles", __name__)
roles_service = RolesService()


@roles_api.get("/")
def get_all_roles():
    roles = roles_service.get_all_roles()

    if isinstance(roles, str):
        return roles, 404
    else:
        return jsonify(roles), 200


@roles_api.get("/<int:id>")
def get_role_by_id(id: int):
    role = roles_service.get_role_by_id(id)

    if isinstance(role, str):
        return role, 404
    else:
        return jsonify(role), 200


@roles_api.get("/<string:name>")
def get_role_by_name(name: str):
    role = roles_service.get_role_by_name(name)

    if isinstance(role, str):
        return role, 404
    else:
        return jsonify(role), 200


@roles_api.post("/")
def create_role():
    role = roles_service.map_role(request.json)
    if not isinstance(role, Roles):
        return jsonify(role), 400

    new_role = roles_service.create_role(role)

    if isinstance(new_role, str):
        return new_role, 400
    else:
        return jsonify(new_role), 201


@roles_api.put("/<int:id>")
def update_role(id: int):
    role = roles_service.map_role(request.json)
    if not isinstance(role, Roles):
        return jsonify(role), 400

    updated_role = roles_service.update_role(id, role)

    if isinstance(updated_role, str):
        return updated_role, 400
    else:
        return jsonify(updated_role), 200


@roles_api.delete("/<int:id>")
def delete_role(id: int):
    deleted_role = roles_service.delete_role(id)

    if isinstance(deleted_role, str):
        return deleted_role, 400
    else:
        return jsonify(deleted_role), 200
