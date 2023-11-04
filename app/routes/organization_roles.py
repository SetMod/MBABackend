from flask import Blueprint, jsonify, request
from app.models import OrganizationRoles
from app.services import OrganizationRolesService

organization_roles_api = Blueprint("organization_roles", __name__)
organization_roles_service = OrganizationRolesService()


@organization_roles_api.get("/")
def get_all_organization_roles():
    organization_roles = organization_roles_service.get_all()

    if organization_roles is None:
        return "Organization roles not found", 404
    else:
        return jsonify(organization_roles), 200


@organization_roles_api.get("/<int:id>")
def get_organization_role_by_id(id: int):
    organization_role = organization_roles_service.get_by_id(id)

    if organization_role is None:
        return "Organization roles not found", 404
    else:
        return jsonify(organization_role), 200


@organization_roles_api.post("/")
def create_organization_role():
    organization_role = organization_roles_service.map_model(request.json)
    if not isinstance(organization_role, OrganizationRoles):
        return jsonify(organization_role), 400

    created_organization_role = organization_roles_service.create(organization_role)

    if created_organization_role is None:
        return "Failed to create an organization roles", 400
    else:
        return jsonify(created_organization_role), 202


@organization_roles_api.put("/<int:id>")
def update_organization_role(id: int):
    organization_role = organization_roles_service.map_model(request.json)
    if not isinstance(organization_role, OrganizationRoles):
        return jsonify(organization_role), 400

    updated_organization_role = organization_roles_service.update(id, organization_role)

    if updated_organization_role is None:
        return "Failed to update an organization roles", 400
    else:
        return jsonify(updated_organization_role), 200


@organization_roles_api.delete("/<int:id>")
def delete_organization_role(id: int):
    deleted_organization_role = organization_roles_service.delete(id)

    if deleted_organization_role is None:
        return "Failed to delete an organization roles", 400
    else:
        return jsonify(deleted_organization_role), 200
