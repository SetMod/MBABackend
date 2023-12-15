from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.routes.common import register_crud_routes
from app.schemas import OrganizationMembersFullSchema
from app.services import organization_members_service

jwt_optional = False
members_bp = Blueprint(name="members", import_name=__name__)
register_crud_routes(members_bp, organization_members_service, jwt_optional)


@members_bp.get("/full")
@jwt_required(optional=jwt_optional)
def get_full():
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_members = organization_members_service.get_all()
    return (
        jsonify(OrganizationMembersFullSchema().dump(organization_members, many=True)),
        200,
    )


@members_bp.get("/<int:id>/full")
@jwt_required(optional=jwt_optional)
def get_by_id_full(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member = organization_members_service.get_by_id(id)

    return jsonify(OrganizationMembersFullSchema().dump(organization_member)), 200
