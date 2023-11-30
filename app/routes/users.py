from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from app.logger import logger
from app.routes.crud import register_crud_routes
from app.services import (
    DatasourcesService,
    OrganizationsService,
    ReportsService,
    UsersService,
)

users_svc = UsersService()
organizations_svc = OrganizationsService()
reports_svc = ReportsService()
datasources_svc = DatasourcesService()
jwt_optional = False
users_bp = Blueprint(name="users", import_name=__name__)
register_crud_routes(users_bp, users_svc, jwt_optional)


@users_bp.post("/auth/register")
def register():
    new_user_dict = request.json
    new_model = users_svc.create(new_user_dict)

    return jsonify(users_svc.to_json(new_model)), 201


@users_bp.post("/auth/login")
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
    user = users_svc.login(user_dict["username"], user_dict["password"])
    access_token = create_access_token(identity=user.username)
    # return jsonify(access_token=access_token)

    response = jsonify({"message": "login successful"})
    set_access_cookies(response, access_token)
    return response


@users_bp.get("/auth/logout")
@jwt_required(optional=jwt_optional)
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response


@users_bp.post("/<string:username>/request_reset")
def request_reset(username: str):
    email = request.args.get("email")

    users_svc.request_reset(username, email)

    return jsonify({"message": "Reset email sent"}), 200


@users_bp.route("/<string:username>/reset_password")
def reset_password(username: str):
    token = request.json.get("token")
    password = request.json.get("password")

    users_svc.reset_password(username=username, password=password, token=token)

    return jsonify({"message": "Password reset successfully"}), 200


@users_bp.get("/<int:id>/organizations")
@jwt_required(optional=jwt_optional)
def get_all_organizations(id: int):
    user_organizations = users_svc.get_all_organizations(id)

    return jsonify(organizations_svc.to_json(user_organizations)), 200


@users_bp.get("/<int:id>/reports")
@jwt_required(optional=jwt_optional)
def get_all_reports(id: int):
    user_reports = users_svc.get_all_reports(id)

    return jsonify(reports_svc.to_json(user_reports)), 200


@users_bp.get("/<int:id>/datasources")
@jwt_required(optional=jwt_optional)
def get_all_datasources(id: int):
    user_datasources = users_svc.get_all_datasources(id)

    return jsonify(datasources_svc.to_json(user_datasources)), 200
