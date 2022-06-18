from flask import Blueprint, jsonify, request
from models.OrganizationsModel import Organizations
from models.UsersOrganizationsModel import UsersOrganizations
from services.OrganizationsService import OrganizationsService
from services.UsersOrganizationsService import UsersOrganizationsService

organizations_api = Blueprint('organizations', __name__)
organizations_service = OrganizationsService()
users_organizations_service = UsersOrganizationsService()


@organizations_api.get('/')
def get_all_organizations():
    organizations = organizations_service.get_all_organizations()

    if organizations is None:
        return 'Organizations not found', 404
    else:
        return jsonify(organizations), 200


@organizations_api.get('/<int:organization_id>')
def get_organization_by_id(organization_id: int):
    organization = organizations_service.get_organization_by_id(
        organization_id)

    if organization is None:
        return 'Organization not found', 404
    else:
        return jsonify(organization), 200


@organizations_api.get('/<int:organization_id>/users')
def get_organization_users(organization_id: int):
    organization_users = organizations_service.get_organization_users(
        organization_id)

    if organization_users is None:
        return 'Users not found', 404
    else:
        return jsonify(organization_users), 200


@organizations_api.get('/<int:organization_id>/files')
def get_organization_files(organization_id: int):
    organization_files = organizations_service.get_organization_files(
        organization_id)

    if organization_files is None:
        return 'Files not found', 404
    else:
        return jsonify(organization_files), 200


@organizations_api.get('/<int:organization_id>/reports')
def get_organization_reports(organization_id: int):
    organization_reports = organizations_service.get_organization_reports(
        organization_id)

    if organization_reports is None:
        return 'Reports not found', 404
    else:
        return jsonify(organization_reports), 200


@organizations_api.post('/users')
def add_user_to_organization():
    user_organization = users_organizations_service.map_users_organizations(
        request.json)

    if not isinstance(user_organization, UsersOrganizations):
        return jsonify(user_organization), 400

    added_user_organization = organizations_service.add_user_to_organization(
        user_organization)
    print(added_user_organization)
    if added_user_organization is None:
        return 'Failed to add user to organization', 400
    else:
        return jsonify(added_user_organization), 201


@organizations_api.post('/')
def create_organization():
    organization = organizations_service.map_organization(request.json)
    if not isinstance(organization, Organizations):
        return jsonify(organization), 400

    created_organization = organizations_service.create_organization(
        organization)

    if created_organization is None:
        return "Failed to create an organization", 400
    else:
        return jsonify(created_organization), 201


@organizations_api.put('/<int:organization_id>')
def update_organization(organization_id: int):
    organization = organizations_service.map_organization(request.json)
    if not isinstance(organization, Organizations):
        return jsonify(organization), 400

    updated_organization = organizations_service.update_organization(
        organization_id, organization)

    if updated_organization is None:
        return "Failed to update an organization", 400
    else:
        return jsonify(updated_organization), 201


@organizations_api.delete('/<int:organization_id>/user/<int:user_id>')
def remove_user_from_organization(user_id: int, organization_id: int):
    user_organizations = organizations_service.delete_user_from_organization(
        user_id, organization_id)

    if user_organizations is None:
        return 'Failed to remove user from organization', 400
    else:
        return jsonify(user_organizations), 200


@organizations_api.delete('/<int:organization_id>')
def delete_organization(organization_id: int):
    deleted_organization = organizations_service.delete_organization(
        organization_id)

    if deleted_organization is None:
        return "Failed to delete an organization", 400
    else:
        return jsonify(deleted_organization), 200
