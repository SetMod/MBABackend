from flask import Blueprint, jsonify, request
from app.models import UsersOrganizations
from app.services import UsersOrganizationsService


users_organizations_api = Blueprint("users_organizations", __name__)
users_organizations_service = UsersOrganizationsService()


@users_organizations_api.get("/")
def get_all_users_organizations():
    user_id = request.args.get("user_id", type=int)
    organization_id = request.args.get("organization_id", type=int)

    if user_id is not None and organization_id is not None:
        users_organizations = users_organizations_service.get_user_organization(
            user_id, organization_id
        )
    else:
        users_organizations = users_organizations_service.get_all_users_organizations()

    if isinstance(users_organizations, str):
        return users_organizations, 404
    else:
        return jsonify(users_organizations), 200


@users_organizations_api.get("/role")
def get_user_organization_role():
    user_id = request.args.get("user_id", type=int)
    organization_id = request.args.get("organization_id", type=int)
    users_organizations = None

    if user_id is None or organization_id is None:
        return "User id or organization id are not specified", 400

    users_organizations = users_organizations_service.get_user_organization_role(
        user_id, organization_id
    )

    if isinstance(users_organizations, str):
        return users_organizations, 404
    else:
        return jsonify(users_organizations), 200


@users_organizations_api.post("/")
def add_user_to_organization():
    user_organization = users_organizations_service.map_users_organizations(
        request.json
    )

    if not isinstance(user_organization, UsersOrganizations):
        return jsonify(user_organization), 400

    added_user_organization = users_organizations_service.add_user_to_organizations(
        user_organization
    )

    if isinstance(added_user_organization, str):
        return added_user_organization, 400
    else:
        return jsonify(added_user_organization), 201
