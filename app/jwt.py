from flask_jwt_extended import JWTManager

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    from app.models import Users

    user: Users = user
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from app.services import users_service

    identity = jwt_data["sub"]
    return users_service.get_by_id(id=identity)
