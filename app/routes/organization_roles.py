from flask import Blueprint, jsonify, request
from models.OrganizationRolesModel import OrganizationRoles
from services.OrganizationRolesService import OrganizationRolesService

organization_roles_api = Blueprint('organization_roles', __name__)
organization_roles_service = OrganizationRolesService()


@organization_roles_api.get('/')
def get_all_organization_roles():
    organization_roles = organization_roles_service.get_all_organization_roles()

    if organization_roles is None:
        return 'Organization roles not found', 404
    else:
        return jsonify(organization_roles), 200


@organization_roles_api.get('/<int:organization_role_id>')
def get_organization_role_by_id(organization_role_id: int):
    organization_role = organization_roles_service.get_organization_role_by_id(
        organization_role_id)

    if organization_role is None:
        return 'Organization roles not found', 404
    else:
        return jsonify(organization_role), 200


@organization_roles_api.post('/')
def create_organization_role():
    organization_role = organization_roles_service.map_organization_role(
        request.json)
    if not isinstance(organization_role, OrganizationRoles):
        return jsonify(organization_role), 400

    created_organization_role = organization_roles_service.create_organization_role(
        organization_role)

    if created_organization_role is None:
        return 'Failed to create an organization roles', 400
    else:
        return jsonify(created_organization_role), 202


@organization_roles_api.put('/<int:organization_role_id>')
def update_organization_role(organization_role_id: int):
    organization_role = organization_roles_service.map_organization_role(
        request.json)
    if not isinstance(organization_role, OrganizationRoles):
        return jsonify(organization_role), 400

    updated_organization_role = organization_roles_service.update_organization_role(
        organization_role_id, organization_role)

    if updated_organization_role is None:
        return 'Failed to update an organization roles', 400
    else:
        return jsonify(updated_organization_role), 200


@organization_roles_api.delete('/<int:organization_role_id>')
def delete_organization_role(organization_role_id: int):
    deleted_organization_role = organization_roles_service.delete_organization_role(
        organization_role_id)

    if deleted_organization_role is None:
        return 'Failed to delete an organization roles', 400
    else:
        return jsonify(deleted_organization_role), 200
