from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.routes.common import register_crud_routes, register_get_full_routes
from app.schemas import (
    AnalyzesFullSchema,
    DatasourcesTypeFullSchema,
    OrganizationMembersFullSchema,
    ReportsFullSchema,
)
from app.services import (
    organizations_service,
    reports_service,
    datasources_service,
    analyzes_service,
    organization_members_service,
)

jwt_optional = False
organizations_bp = Blueprint(name="organizations", import_name=__name__)
register_crud_routes(organizations_bp, organizations_service, jwt_optional)
register_get_full_routes(organizations_bp, organizations_service, jwt_optional)


@organizations_bp.get("/<int:id>/members")
@jwt_required(optional=jwt_optional)
def get_all_members(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    args = request.args.to_dict()

    args["organization_id"] = id
    organization_members = organizations_service.get_all_members(id)
    return jsonify(organization_members_service.to_json(organization_members)), 200


@organizations_bp.get("/<int:id>/members/full")
@jwt_required(optional=jwt_optional)
def get_all_member_full(id: int):
    org_members = organizations_service.get_all_members(id)

    return (
        jsonify(OrganizationMembersFullSchema().dump(org_members, many=True)),
        200,
    )
