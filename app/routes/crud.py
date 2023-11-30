from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.services import GenericService


def register_crud_routes(
    generic_blueprint: Blueprint,
    generic_service: GenericService,
    jwt_optional: bool = False,
):
    @generic_blueprint.get("/")
    @jwt_required(optional=jwt_optional)
    def get_all():
        logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")
        bool_map = {"true": True, "false": False}

        if request.args:
            args = request.args.to_dict()
            for key, val in args.items():
                args[key] = bool_map[val.lower()] if val.lower() in bool_map else val

            model = generic_service.get_by_fields(args, many=True)

            return jsonify(generic_service.to_json(model)), 200
        else:
            models = generic_service.get_all()

            return jsonify(generic_service.to_json(models)), 200

    @generic_blueprint.get("/<int:id>")
    @jwt_required(optional=jwt_optional)
    def get_by_id(id: int):
        logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

        model = generic_service.get_by_id(id)

        return jsonify(generic_service.to_json(model)), 200

    @generic_blueprint.post("/")
    @jwt_required(optional=jwt_optional)
    def create():
        logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

        model_dict = request.json
        new_model = generic_service.create(model_dict)

        return jsonify(generic_service.to_json(new_model)), 201

    @generic_blueprint.put("/<int:id>")
    @jwt_required(optional=jwt_optional)
    def update(id: int):
        logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

        model_dict = request.json
        updated_model = generic_service.update(id=id, updated_model_dict=model_dict)

        return jsonify(generic_service.to_json(updated_model)), 200

    @generic_blueprint.delete("/<int:id>")
    @jwt_required(optional=jwt_optional)
    def delete(id: int):
        logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

        deleted_model = generic_service.delete(id=id)

        return jsonify(generic_service.to_json(deleted_model)), 200

    @generic_blueprint.delete("/<int:id>/soft")
    @jwt_required(optional=jwt_optional)
    def soft_delete(id: int):
        logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

        deleted_model = generic_service.soft_delete(id=id)

        return jsonify(generic_service.to_json(deleted_model)), 200
