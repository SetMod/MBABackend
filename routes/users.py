from flask import Blueprint, jsonify, request
from models.UsersModel import Users
from models.UsersOrganizationsModel import UsersOrganizations
from services.UsersOrganizationsService import UsersOrganizationsService
from services.UsersService import UsersService

users_api = Blueprint('users', __name__)
users_service = UsersService()
users_organizations_service = UsersOrganizationsService()


@users_api.get('/')
def get_all_users():
    users = users_service.get_all_users()

    if users is None:
        return 'Users not found', 404
    else:
        return jsonify(users), 200


@users_api.get('/<int:user_id>')
def get_user_by_id(user_id: int):
    user = users_service.get_user_by_id(user_id)

    if user is None:
        return 'User not found', 404
    else:
        return jsonify(user), 200


@users_api.get('/?role_name=<string:role_name>')
def get_users_by_role(role_name: str):
    users = users_service.get_users_by_role(role_name)

    if users is None:
        return 'Users not found', 404
    else:
        return jsonify(users), 200


@users_api.get('/<int:user_id>/organizations')
def get_user_organizations(user_id: int):
    user_organizations = users_service.get_user_organizations(user_id)

    if user_organizations is None:
        return 'Organizations not found', 404
    else:
        return jsonify(user_organizations), 200


@users_api.get('/<int:user_id>/files')
def get_user_files(user_id: int):
    user_files = users_service.get_user_files(user_id)

    if user_files is None:
        return 'Files not found', 404
    else:
        return jsonify(user_files), 200


@users_api.get('/<int:user_id>/reports')
def get_user_reports(user_id: int):
    user_reports = users_service.get_user_reports(user_id)

    if user_reports is None:
        return 'Reports not found', 404
    else:
        return jsonify(user_reports), 200


@users_api.post('/login')
def get_user_by_credentials():
    user_username = request.json['user_username']
    user_password = request.json['user_password']
    print(request.json)

    if user_username is None:
        return jsonify({'user_password': ['Field don\'t specified']}), 404
    if user_password is None:
        return jsonify({'user_password': ['Field don\'t specified']}), 404

    user = users_service.get_user_by_credentials(user_username, user_password)
    print(user)
    if user is None:
        return "User not found", 404
    else:
        return jsonify(user), 201


@users_api.post('/')
def create_user():
    user = users_service.map_user(request.json)

    if not isinstance(user, Users):
        return jsonify(user), 400

    created_user = users_service.create_user(user)

    if created_user is None:
        return "Failed to create a user", 400
    else:
        return jsonify(created_user), 201


@users_api.put('/<int:user_id>')
def update_user(user_id: int):
    user = users_service.map_user(request.json)

    if not isinstance(user, Users):
        return jsonify(user), 400

    updated_user = users_service.update_user(user_id, user)

    if updated_user is None:
        return "Failed to update a user", 400
    else:
        return jsonify(updated_user), 200


@users_api.post('/organizations')
def add_user_to_organization():
    user_organization = users_organizations_service.map_users_organizations(
        request.json)

    if not isinstance(user_organization, UsersOrganizations):
        return jsonify(user_organization), 400

    added_user_organization = users_service.add_user_to_organization(
        user_organization)

    if added_user_organization is None:
        return 'Failed to add user to organization', 400
    else:
        return jsonify(added_user_organization), 201


@users_api.delete('/<int:user_id>')
def delete_user(user_id: int):
    deleted_user = users_service.delete_user(user_id)

    if deleted_user is None:
        return "Failed to delete a user", 400
    else:
        return jsonify(deleted_user), 200


@users_api.delete('/<int:user_id>/organizations/<int:organization_id>')
def remove_user_from_organization(user_id: int, organization_id: int):
    user_organizations = users_service.remove_user_from_organization(
        user_id, organization_id)

    if user_organizations is None:
        return 'Failed to remove user from organization', 400
    else:
        return jsonify(user_organizations), 200
