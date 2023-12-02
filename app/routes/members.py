from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import organization_members_service

jwt_optional = False
members_bp = Blueprint(name="members", import_name=__name__)
register_crud_routes(members_bp, organization_members_service, jwt_optional)
