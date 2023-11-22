from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.routes.GenericRoute import GenericRoute
from app.services import RolesService, UsersService


class RolesRoute(GenericRoute):
    bp = Blueprint(name="roles", import_name=__name__)
    roles_svc = RolesService()
    users_svc = UsersService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.roles_svc)
        self.register_routes()

    def register_routes(self):
        super().register_routes()

        self.get_all_users()

    def get_all_users(self):
        @self.bp.get("/<int:id>/users")
        @jwt_required(optional=self.jwt_optional)
        def get_all_users(id: int):
            role_users = self.roles_svc.get_all_users(id)

            return jsonify(self.users_svc.to_json(role_users)), 200
