from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.routes.common import register_crud_routes, register_get_full_routes
from app.schemas import OrganizationMembersFullSchema
from app.services import (
    organizations_service,
    organization_members_service,
    users_service,
)

jwt_optional = False
users_bp = Blueprint(name="users", import_name=__name__)
register_crud_routes(users_bp, users_service, jwt_optional)
register_get_full_routes(users_bp, users_service, jwt_optional)


@users_bp.get("/<int:id>/organizations")
@jwt_required(optional=jwt_optional)
def get_all_organizations(id: int):
    user_organizations = users_service.get_all_organizations(id)

    return jsonify(organizations_service.to_json(user_organizations)), 200


@users_bp.get("/<int:id>/memberships")
@jwt_required(optional=jwt_optional)
def get_all_memberships(id: int):
    user_memberships = users_service.get_all_memberships(id)

    return jsonify(organization_members_service.to_json(user_memberships)), 200


@users_bp.get("/<int:id>/memberships/full")
@jwt_required(optional=jwt_optional)
def get_all_memberships_full(id: int):
    user_memberships = users_service.get_all_memberships(id)

    return (
        jsonify(OrganizationMembersFullSchema().dump(user_memberships, many=True)),
        200,
    )
