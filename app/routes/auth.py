from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)
from app.logger import logger
from app.services import users_service


jwt_optional = False
auth_bp = Blueprint(name="auth", import_name=__name__)


@auth_bp.post("/register")
def register():
    new_user_dict = request.json
    new_model = users_service.create(new_user_dict)

    return jsonify(users_service.to_json(new_model)), 201


@auth_bp.post("/login")
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


@auth_bp.get("/who_am_i")
@jwt_required(optional=jwt_optional)
def protected():
    current_user_dict = users_service.to_json(current_user)

    return jsonify(current_user_dict)


@auth_bp.get("/logout")
@jwt_required(optional=jwt_optional)
def logout():
    response = jsonify({"message": "logout successful"})
    # unset_jwt_cookies(response)

    return response


@auth_bp.post("/<string:username>/request_reset")
def request_reset(username: str):
    email = request.args.get("email")

    users_service.request_reset(username, email)

    return jsonify({"message": "Reset email sent"}), 200


@auth_bp.route("/<string:username>/reset_password")
def reset_password(username: str):
    token = request.json.get("token")
    password = request.json.get("password")

    users_service.reset_password(username=username, password=password, token=token)

    return jsonify({"message": "Password reset successfully"}), 200
