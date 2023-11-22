from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.services import GenericService


class GenericRoute:
    def __init__(
        self, blueprint: Blueprint, service: GenericService, jwt_optional: bool = False
    ) -> None:
        self.generic_blueprint = blueprint
        self.generic_service = service
        self.jwt_optional = jwt_optional

    def register_route(self, blueprint: Blueprint, service: GenericService):
        self.generic_blueprint = blueprint
        self.generic_service = service

    def register_routes(self):
        self.get_all()
        self.get_by_id()
        self.create()
        self.update()
        self.delete()
        self.soft_delete()

    def get_all(self):
        @self.generic_blueprint.get("/")
        @jwt_required(optional=self.jwt_optional)
        def get_all():
            if request.args:
                model = self.generic_service.get_by_fields(request.args.to_dict())

                return jsonify(self.generic_service.to_json(model)), 200
            else:
                models = self.generic_service.get_all()

                return jsonify(self.generic_service.to_json(models)), 200

    def get_by_id(self):
        @self.generic_blueprint.get("/<int:id>")
        @jwt_required(optional=self.jwt_optional)
        def get_by_id(id: int):
            model = self.generic_service.get_by_id(id)

            return jsonify(self.generic_service.to_json(model)), 200

    def create(self):
        @self.generic_blueprint.post("/")
        @jwt_required(optional=self.jwt_optional)
        def create():
            model_dict = request.json
            new_model = self.generic_service.create(model_dict)

            return jsonify(self.generic_service.to_json(new_model)), 201

    def update(self):
        @self.generic_blueprint.put("/<int:id>")
        @jwt_required(optional=self.jwt_optional)
        def update(id: int):
            model_dict = request.json
            updated_model = self.generic_service.update(id, model_dict)

            return jsonify(self.generic_service.to_json(updated_model)), 200

    def delete(self):
        @self.generic_blueprint.delete("/<int:id>")
        @jwt_required(optional=self.jwt_optional)
        def delete(id: int):
            deleted_model = self.generic_service.delete(id)

            return jsonify(self.generic_service.to_json(deleted_model)), 200

    def soft_delete(self):
        @self.generic_blueprint.delete("/<int:id>/soft")
        @jwt_required(optional=self.jwt_optional)
        def soft_delete(id: int):
            deleted_model = self.generic_service.soft_delete(id)

            return jsonify(self.generic_service.to_json(deleted_model)), 200
