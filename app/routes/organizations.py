from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.routes.crud import register_crud_routes
from app.services import organizations_service, users_service

jwt_optional = False
organizations_bp = Blueprint(name="organizations", import_name=__name__)
register_crud_routes(organizations_bp, organizations_service, jwt_optional)


# @organizations_bp.get("/<int:id>/members")
# @jwt_required(optional=jwt_optional)
# def get_all_members(id: int):
#     members = organizations_service.get_all_members(id)

#     return jsonify(users_service.to_json(members)), 200


# @organizations_bp.get("/<int:id>/members/<int:user_id>")
# @jwt_required(optional=jwt_optional)
# def get_all_member_by_id(id: int, user_id: int):
#     member = organizations_service.organization_members_service.get_by_fields(
#         {"user_id": user_id, "organization_id": id}
#     )

#     return jsonify(users_service.to_json(member)), 200
