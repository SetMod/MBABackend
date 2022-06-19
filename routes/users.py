from flask import Blueprint, jsonify, request
from models.UsersModel import Users
from services.UsersService import UsersService

users_api = Blueprint('users', __name__)
users_service = UsersService()
# users_organizations_service = UsersOrganizationsService()


@users_api.get('/')
def get_all_users():
    role_name = request.args.get('role_name')
    if role_name:
        users = users_service.get_users_by_role(role_name)
    else:
        users = users_service.get_all_users()

    if isinstance(users, str):
        return users, 404
    else:
        return jsonify(users), 200


@users_api.get('/<int:user_id>')
def get_user_by_id(user_id: int):
    user = users_service.get_user_by_id(user_id)
    role = users_service.get_user_role(user_id)

    if isinstance(user, str) or isinstance(role, str):
        return user, 404

    user = {**user, **role}
    return jsonify(user), 200


@users_api.get('/<int:user_id>/organizations')
def get_user_organizations(user_id: int):
    user_organizations = users_service.get_user_organizations(user_id)

    if isinstance(user_organizations, str):
        return user_organizations, 404
    else:
        return jsonify(user_organizations), 200


@users_api.get('/<int:user_id>/files')
def get_user_files(user_id: int):
    user_files = users_service.get_user_files(user_id)

    if isinstance(user_files, str):
        return user_files, 404
    else:
        return jsonify(user_files), 200


@users_api.get('/<int:user_id>/reports')
def get_user_reports(user_id: int):
    user_reports = users_service.get_user_reports(user_id)

    if isinstance(user_reports, str):
        return user_reports, 404
    else:
        return jsonify(user_reports), 200


@users_api.post('/login')
def get_user_by_credentials():
    user_username = request.json['user_username']
    user_password = request.json['user_password']

    if user_username is None:
        return 'Field "user_username" don\'t specified', 404
    if user_password is None:
        return 'Field "user_password" don\'t specified', 404

    user = users_service.get_user_by_credentials(user_username, user_password)

    if isinstance(user, str):
        return user, 404

    role = users_service.get_user_role(user['user_id'])

    user = {**user, **role}
    return jsonify(user), 200


@users_api.post('/')
def create_user():
    user = users_service.map_user(request.json)

    if not isinstance(user, Users):
        return jsonify(user), 400

    created_user = users_service.create_user(user)

    if isinstance(created_user, str):
        return created_user, 400
    else:
        return jsonify(created_user), 201


@users_api.put('/<int:user_id>')
def update_user(user_id: int):
    user = users_service.map_user(request.json)

    if not isinstance(user, Users):
        return jsonify(user), 400

    updated_user = users_service.update_user(user_id, user)

    if isinstance(updated_user, str):
        return updated_user, 400
    else:
        return jsonify(updated_user), 200


@users_api.delete('/<int:user_id>')
def delete_user(user_id: int):
    deleted_user = users_service.delete_user(user_id)

    if isinstance(deleted_user, str):
        return deleted_user, 400
    else:
        return jsonify(deleted_user), 200
