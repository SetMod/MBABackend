from flask import Blueprint, jsonify, request
from app.models import Organizations, UsersOrganizations
from app.services import OrganizationsService, UsersOrganizationsService

organizations_api = Blueprint("organizations", __name__)
organizations_service = OrganizationsService()
users_organizations_service = UsersOrganizationsService()


@organizations_api.get("/")
def get_all_organizations():
    organizations = organizations_service.get_all_organizations()

    if isinstance(organizations, str):
        return organizations, 404
    else:
        return jsonify(organizations), 200


@organizations_api.get("/<int:id>")
def get_organization_by_id(id: int):
    organization = organizations_service.get_organization_by_id(id)

    if isinstance(organization, str):
        return organization, 404
    else:
        return jsonify(organization), 200


@organizations_api.get("/<int:id>/users")
def get_organization_users(id: int):
    members = organizations_service.get_organization_users(id)

    if isinstance(members, str):
        return members, 404
    else:
        return jsonify(members), 200


@organizations_api.get("/user/<int:user_id>")
def get_user_organizations(user_id: int):
    user_organizations = organizations_service.get_user_organizations(user_id)

    if isinstance(user_organizations, str):
        return user_organizations, 404
    else:
        return jsonify(user_organizations), 200


@organizations_api.get("/<int:id>/files")
def get_organization_files(id: int):
    organization_files = organizations_service.get_organization_files(id)

    if isinstance(organization_files, str):
        return organization_files, 404
    else:
        return jsonify(organization_files), 200


@organizations_api.get("/<int:id>/reports")
def get_organization_reports(id: int):
    organization_reports = organizations_service.get_organization_reports(id)

    if isinstance(organization_reports, str):
        return organization_reports, 404
    else:
        return jsonify(organization_reports), 200


@organizations_api.post("/users")
def add_user_to_organization():
    user_organization = users_organizations_service.map_users_organizations(
        request.json
    )

    if not isinstance(user_organization, UsersOrganizations):
        return jsonify(user_organization), 400

    created_user_organization = organizations_service.add_user_to_organization(
        user_organization
    )

    if isinstance(created_user_organization, str):
        return created_user_organization, 400
    else:
        return jsonify(created_user_organization), 201


@organizations_api.post("/")
def create_organization():
    user_id = request.args.get("user_id")

    if user_id is None:
        return "User id not specified", 400

    organization = organizations_service.map_organization(request.json)
    if not isinstance(organization, Organizations):
        return jsonify(organization), 400

    created_organization = organizations_service.create_organization(
        organization, user_id
    )

    if isinstance(created_organization, str):
        return created_organization, 400
    else:
        return jsonify(created_organization), 201


@organizations_api.put("/<int:id>")
def update_organization(id: int):
    organization = organizations_service.map_organization(request.json)
    if not isinstance(organization, Organizations):
        return jsonify(organization), 400

    updated_organization = organizations_service.update_organization(id, organization)

    if isinstance(updated_organization, str):
        return updated_organization, 400
    else:
        return jsonify(updated_organization), 200


@organizations_api.delete("/<int:id>/user/<int:user_id>")
def remove_user_from_organization(user_id: int, id: int):
    user_organizations = organizations_service.delete_user_from_organization(
        user_id, id
    )

    if user_organizations is None:
        return "Failed to remove user from organization", 400
    else:
        return jsonify(user_organizations), 200


@organizations_api.delete("/<int:id>")
def delete_organization(id: int):
    deleted_organization = organizations_service.delete_organization(id)

    if deleted_organization is None:
        return "Failed to delete an organization", 400
    else:
        return jsonify(deleted_organization), 200
