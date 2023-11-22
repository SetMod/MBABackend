from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.routes.GenericRoute import GenericRoute
from app.services import OrganizationsService, UsersService


class OrganizationsRoute(GenericRoute):
    bp = Blueprint(name="organizations", import_name=__name__)
    organizations_svc = OrganizationsService()
    users_svc = UsersService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.organizations_svc)
        self.register_routes()

    def register_routes(self):
        super().register_routes()

        self.get_all_members()
        self.get_all_member_by_id()

    def get_all_members(self):
        @self.bp.get("/<int:id>/members")
        @jwt_required(optional=self.jwt_optional)
        def get_all_members(id: int):
            members = self.organizations_svc.get_all_members(id)

            return jsonify(self.users_svc.to_json(members)), 200

    def get_all_member_by_id(self):
        @self.bp.get("/<int:id>/members/<int:user_id>")
        @jwt_required(optional=self.jwt_optional)
        def get_all_member_by_id(id: int, user_id: int):
            member = self.organizations_svc.get_member_by_id(id, user_id)

            return jsonify(self.users_svc.to_json(member)), 200
