from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)
from app.logger import logger
from app.routes.crud import register_crud_routes
from app.services import (
    datasources_service,
    organizations_service,
    organization_members_service,
    reports_service,
    users_service,
    analyzes_service,
)

jwt_optional = False
users_bp = Blueprint(name="users", import_name=__name__)
register_crud_routes(users_bp, users_service, jwt_optional)


@users_bp.post("/auth/register")
def register():
    new_user_dict = request.json
    new_model = users_service.create(new_user_dict)

    return jsonify(users_service.to_json(new_model)), 201


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
    user = users_service.login(user_dict["username"], user_dict["password"])
    access_token = create_access_token(identity=user)
    return jsonify({"message": "login successful", "access_token": access_token})

    # response = jsonify({"message": "login successful"})
    # set_access_cookies(response, access_token)
    # return response


@users_bp.get("/auth/who_am_i")
@jwt_required(optional=jwt_optional)
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    current_user_dict = users_service.to_json(current_user)
    return jsonify(current_user_dict)


@users_bp.get("/auth/logout")
@jwt_required(optional=jwt_optional)
def logout():
    response = jsonify({"message": "logout successful"})
    # unset_jwt_cookies(response)

    return response


@users_bp.post("/<string:username>/request_reset")
def request_reset(username: str):
    email = request.args.get("email")

    users_service.request_reset(username, email)

    return jsonify({"message": "Reset email sent"}), 200


@users_bp.route("/<string:username>/reset_password")
def reset_password(username: str):
    token = request.json.get("token")
    password = request.json.get("password")

    users_service.reset_password(username=username, password=password, token=token)

    return jsonify({"message": "Password reset successfully"}), 200


@users_bp.get("/<int:id>/organizations")
@jwt_required(optional=jwt_optional)
def get_all_organizations(id: int):
    user_organizations = users_service.get_all_organizations(id)

    return jsonify(organizations_service.to_json(user_organizations)), 200


@users_bp.get("/<int:id>/memberships")
@jwt_required(optional=jwt_optional)
def get_all_memberships(id: int):
    user_memberships = users_service.get_all_memberships(id)

    return jsonify(organization_members_service.to_json(user_memberships)), 200


@users_bp.get("/<int:id>/reports")
@jwt_required(optional=jwt_optional)
def get_all_reports(id: int):
    user_reports = users_service.get_all_reports(id)

    return jsonify(reports_service.to_json(user_reports)), 200


@users_bp.get("/<int:id>/datasources")
@jwt_required(optional=jwt_optional)
def get_all_datasources(id: int):
    user_datasources = users_service.get_all_datasources(id)

    return jsonify(datasources_service.to_json(user_datasources)), 200


@users_bp.get("/<int:id>/analyzes")
@jwt_required(optional=jwt_optional)
def get_all_analyzes(id: int):
    user_analyzes = users_service.get_all_analyzes(id)

    return jsonify(analyzes_service.to_json(user_analyzes)), 200
