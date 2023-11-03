from flask import Blueprint, jsonify, request
from app.models import Users
from app.services import UsersService

users_api = Blueprint("users", __name__)
users_service = UsersService()
# users_organizations_service = UsersOrganizationsService()


@users_api.get("/")
def get_all_users():
    name = request.args.get("name")
    if name:
        users = users_service.get_users_by_role(name)
    else:
        users = users_service.get_all_users()

    if isinstance(users, str):
        return users, 404
    else:
        return jsonify(users), 200


@users_api.get("/<int:id>")
def get_user_by_id(id: int):
    user = users_service.get_user_by_id(id)
    role = users_service.get_user_role(id)

    if isinstance(user, str) or isinstance(role, str):
        return user, 404

    user = {**user, **role}
    return jsonify(user), 200


@users_api.get("/<int:id>/organizations")
def get_user_organizations(id: int):
    user_organizations = users_service.get_user_organizations(id)

    if isinstance(user_organizations, str):
        return user_organizations, 404
    else:
        return jsonify(user_organizations), 200


@users_api.get("/<int:id>/files")
def get_user_files(id: int):
    user_files = users_service.get_user_files(id)

    if isinstance(user_files, str):
        return user_files, 404
    else:
        return jsonify(user_files), 200


@users_api.get("/<int:id>/reports")
def get_user_reports(id: int):
    user_reports = users_service.get_user_reports(id)

    if isinstance(user_reports, str):
        return user_reports, 404
    else:
        return jsonify(user_reports), 200


@users_api.post("/login")
def get_user_by_credentials():
    username = request.json["username"]
    password = request.json["password"]

    if username is None:
        return 'Field "username" don\'t specified', 404
    if password is None:
        return 'Field "password" don\'t specified', 404

    user = users_service.get_user_by_credentials(username, password)

    if isinstance(user, str):
        return user, 404

    role = users_service.get_user_role(user["id"])

    user = {**user, **role}
    return jsonify(user), 200


@users_api.post("/")
def create_user():
    user = users_service.map_user(request.json)

    if not isinstance(user, Users):
        return jsonify(user), 400

    created_user = users_service.create_user(user)

    if isinstance(created_user, str):
        return created_user, 400
    else:
        return jsonify(created_user), 201


@users_api.put("/<int:id>")
def update_user(id: int):
    user = users_service.map_user(request.json)

    if not isinstance(user, Users):
        return jsonify(user), 400

    updated_user = users_service.update_user(id, user)

    if isinstance(updated_user, str):
        return updated_user, 400

    role = users_service.get_user_role(updated_user["id"])

    user = {**updated_user, **role}
    return jsonify(user), 200


@users_api.delete("/<int:id>")
def delete_user(id: int):
    deleted_user = users_service.delete_user(id)

    if isinstance(deleted_user, str):
        return deleted_user, 400
    else:
        return jsonify(deleted_user), 200
