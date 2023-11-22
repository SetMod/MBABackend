from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from app.logger import logger
from app.routes.GenericRoute import GenericRoute
from app.services import (
    DatasourcesService,
    OrganizationsService,
    ReportsService,
    RolesService,
    UsersService,
)


class UsersRoute(GenericRoute):
    bp = Blueprint(name="users", import_name=__name__)
    users_svc = UsersService()
    roles_svc = RolesService()
    organizations_svc = OrganizationsService()
    reports_svc = ReportsService()
    datasources_svc = DatasourcesService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.users_svc)
        self.register_routes()

    def register_routes(self):
        super().register_routes()

        self.register()
        self.login()
        self.logout()
        self.get_role()
        self.get_all_organizations()
        self.get_all_reports()
        self.get_all_datasources()

    def register(self):
        @self.bp.post("/auth/register")
        def register():
            new_user_dict = request.json
            new_model = self.users_svc.create(new_user_dict)

            return jsonify(self.users_svc.to_json(new_model)), 201

    def login(self):
        @self.bp.post("/auth/login")
        def login():
            user_dict = request.json
            if "username" not in user_dict or "password" not in user_dict:
                msg = "User username or password not specified"
                logger.warning(msg)
                return (
                    jsonify(
                        {
                            "errorMsg": msg,
                            "code": 400,
                        }
                    ),
                    400,
                )
            user = self.users_svc.login(user_dict["username"], user_dict["password"])
            access_token = create_access_token(identity=user.username)
            # return jsonify(access_token=access_token)

            response = jsonify({"msg": "login successful"})
            set_access_cookies(response, access_token)
            return response

    def logout(self):
        @self.bp.route("/auth/logout", methods=["GET"])
        @jwt_required(optional=self.jwt_optional)
        def logout():
            response = jsonify({"msg": "logout successful"})
            unset_jwt_cookies(response)
            return response

    def get_role(self):
        @self.bp.get("/<int:id>/role")
        @jwt_required(optional=self.jwt_optional)
        def get_role(id: int):
            user_role = self.users_svc.get_role(id)

            return jsonify(self.roles_svc.to_json(user_role)), 200

    def get_all_organizations(self):
        @self.bp.get("/<int:id>/organizations")
        @jwt_required(optional=self.jwt_optional)
        def get_all_organizations(id: int):
            user_organizations = self.users_svc.get_all_organizations(id)

            return jsonify(self.organizations_svc.to_json(user_organizations)), 200

    def get_all_reports(self):
        @self.bp.get("/<int:id>/reports")
        @jwt_required(optional=self.jwt_optional)
        def get_all_reports(id: int):
            user_reports = self.users_svc.get_all_reports(id)

            return jsonify(self.reports_svc.to_json(user_reports)), 200

    def get_all_datasources(self):
        @self.bp.get("/<int:id>/datasources")
        @jwt_required(optional=self.jwt_optional)
        def get_all_datasources(id: int):
            user_datasources = self.users_svc.get_all_datasources(id)

            return jsonify(self.datasources_svc.to_json(user_datasources)), 200
