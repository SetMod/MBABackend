from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import OrganizationMembersService

organization_members_svc = OrganizationMembersService()
jwt_optional = False
members_bp = Blueprint(name="members", import_name=__name__)
register_crud_routes(members_bp, organization_members_svc, jwt_optional)
