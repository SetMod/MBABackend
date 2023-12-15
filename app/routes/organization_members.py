from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.schemas import OrganizationMembersFullSchema
from app.services import (
    organization_members_service,
    organizations_service,
    users_service,
)

jwt_optional = False
organization_members_bp = Blueprint(name="organization_members", import_name=__name__)


# @organization_members_bp.get("/")
# @jwt_required(optional=jwt_optional)
# def get_all(org_id: int):
#     logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

#     args = request.args.to_dict()

#     args["organization_id"] = org_id
#     organization_members = organization_members_service.get_by_fields(args, many=True)
#     return jsonify(organization_members_service.to_json(organization_members)), 200


# @organization_members_bp.get("/full")
# @jwt_required(optional=jwt_optional)
# def get_all_member_full(org_id: int):
#     org_members = organizations_service.get_all_members(org_id)

#     return (
#         jsonify(OrganizationMembersFullSchema().dump(org_members, many=True)),
#         200,
#     )


@organization_members_bp.get("/<int:user_id>")
@jwt_required(optional=jwt_optional)
def get_by_org_and_user_ids(org_id: int, user_id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member = organization_members_service.get_by_fields(
        {
            "user_id": user_id,
            "organization_id": org_id,
        }
    )

    return jsonify(organization_members_service.to_json(organization_member)), 200


@organization_members_bp.get("/<int:user_id>/full")
@jwt_required(optional=jwt_optional)
def get_by_org_and_user_ids_full(org_id: int, user_id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member = organization_members_service.get_by_fields(
        {
            "user_id": user_id,
            "organization_id": org_id,
        }
    )

    return jsonify(OrganizationMembersFullSchema().dump(organization_member)), 200


@organization_members_bp.post("/")
@jwt_required(optional=jwt_optional)
def create(org_id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member_dict = request.json
    organization_member_dict["organization_id"] = org_id
    user_id = organization_member_dict["user_id"]

    users_service.get_by_id(user_id)
    organizations_service.get_by_id(org_id)
    organization_members_service.get_by_fields(
        {
            "user_id": user_id,
            "organization_id": org_id,
        },
        must_exist=False,
    )
    new_organization_member = organization_members_service.create(
        new_model_dict=organization_member_dict
    )

    return jsonify(organization_members_service.to_json(new_organization_member)), 201


@organization_members_bp.put("/<int:user_id>")
@jwt_required(optional=jwt_optional)
def update(org_id: int, user_id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member_dict = request.json
    organization_member_dict["user_id"] = user_id
    organization_member_dict["organization_id"] = org_id

    users_service.get_by_id(user_id)
    organizations_service.get_by_id(organization_member_dict["organization_id"])

    organization_member = organization_members_service.get_by_fields(
        {
            "user_id": user_id,
            "organization_id": org_id,
        }
    )

    organization_member_dict["id"] = organization_member.id

    updated_organization_member = organization_members_service.update(
        id=organization_member.id,
        updated_model_dict=organization_member_dict,
    )

    return (
        jsonify(organization_members_service.to_json(updated_organization_member)),
        200,
    )


@organization_members_bp.delete("/<int:user_id>/soft")
@jwt_required(optional=jwt_optional)
def soft_delete(org_id: int, user_id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member = organization_members_service.get_by_fields(
        {
            "user_id": user_id,
            "organization_id": org_id,
        }
    )
    deleted_organization_member = organization_members_service.soft_delete(
        id=organization_member.id
    )

    return (
        jsonify(organization_members_service.to_json(deleted_organization_member)),
        200,
    )


@organization_members_bp.delete("/<int:user_id>")
@jwt_required(optional=jwt_optional)
def delete(org_id: int, user_id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    organization_member = organization_members_service.get_by_fields(
        {
            "user_id": user_id,
            "organization_id": org_id,
        }
    )
    deleted_organization_member = organization_members_service.delete(
        id=organization_member.id
    )

    return (
        jsonify(organization_members_service.to_json(deleted_organization_member)),
        200,
    )
