from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logger import logger
from app.schemas import AnalyzesFullSchema, DatasourcesFullSchema, ReportsFullSchema
from app.services import (
    GenericService,
    reports_service,
    datasources_service,
    analyzes_service,
)


def register_crud_routes(
    bp: Blueprint,
    svc: GenericService,
    jwt_optional: bool = False,
    add_get_all: bool = True,
    add_get_by_id: bool = True,
    add_create: bool = True,
    add_update: bool = True,
    add_delete: bool = True,
    add_soft_delete: bool = True,
):
    if add_get_all:

        @bp.get("/")
        @jwt_required(optional=jwt_optional)
        def get_all():
            logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")
            bool_map = {"true": True, "false": False}

            if request.args:
                args = request.args.to_dict()
                for key, val in args.items():
                    args[key] = (
                        bool_map[val.lower()] if val.lower() in bool_map else val
                    )
                many = args.pop("many", True)

                model = svc.get_by_fields(args, many=many)

                return jsonify(svc.to_json(model)), 200
            else:
                models = svc.get_all()

                return jsonify(svc.to_json(models)), 200

    if add_get_by_id:

        @bp.get("/<int:id>")
        @jwt_required(optional=jwt_optional)
        def get_by_id(id: int):
            logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

            model = svc.get_by_id(id)

            return jsonify(svc.to_json(model)), 200

    if add_create:

        @bp.post("/")
        @jwt_required(optional=jwt_optional)
        def create():
            logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

            model_dict = request.json
            if "id" in model_dict:
                model_dict.pop("id")

            new_model = svc.create(model_dict)

            return jsonify(svc.to_json(new_model)), 201

    if add_update:

        @bp.put("/<int:id>")
        @jwt_required(optional=jwt_optional)
        def update(id: int):
            logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

            model_dict = request.json
            if "id" in model_dict:
                model_dict.pop("id")

            updated_model = svc.update(id=id, updated_model_dict=model_dict)

            return jsonify(svc.to_json(updated_model)), 200

    if add_delete:

        @bp.delete("/<int:id>")
        @jwt_required(optional=jwt_optional)
        def delete(id: int):
            logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

            deleted_model = svc.delete(id=id)

            return jsonify(svc.to_json(deleted_model)), 200

    if add_soft_delete:

        @bp.delete("/<int:id>/soft")
        @jwt_required(optional=jwt_optional)
        def soft_delete(id: int):
            logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

            deleted_model = svc.soft_delete(id=id)

            return jsonify(svc.to_json(deleted_model)), 200


def register_get_full_routes(
    bp: Blueprint,
    svc: GenericService,
    jwt_optional: bool = False,
    add_get_all_datasources: bool = True,
    add_get_all_analyzes: bool = True,
    add_get_all_reports: bool = True,
):
    if add_get_all_datasources:

        @bp.get("/<int:id>/datasources")
        @jwt_required(optional=jwt_optional)
        def get_all_datasources(id: int):
            datasources = svc.get_all_datasources(id)

            return jsonify(datasources_service.to_json(datasources)), 200

        @bp.get("/<int:id>/datasources/full")
        @jwt_required(optional=jwt_optional)
        def get_all_datasources_full(id: int):
            datasources = svc.get_all_datasources(id)

            return (
                jsonify(DatasourcesFullSchema().dump(datasources, many=True)),
                200,
            )

    if add_get_all_analyzes:

        @bp.get("/<int:id>/analyzes")
        @jwt_required(optional=jwt_optional)
        def get_all_analyzes(id: int):
            analyzes = svc.get_all_analyzes(id)

            return jsonify(analyzes_service.to_json(analyzes)), 200

        @bp.get("/<int:id>/analyzes/full")
        @jwt_required(optional=jwt_optional)
        def get_all_analyzes_full(id: int):
            analyzes = svc.get_all_analyzes(id)

            return jsonify(AnalyzesFullSchema().dump(analyzes, many=True)), 200

    if add_get_all_reports:

        @bp.get("/<int:id>/reports")
        @jwt_required(optional=jwt_optional)
        def get_all_reports(id: int):
            reports = svc.get_all_reports(id)

            return jsonify(reports_service.to_json(reports)), 200

        @bp.get("/<int:id>/reports/full")
        @jwt_required(optional=jwt_optional)
        def get_all_reports_full(id: int):
            reports = svc.get_all_reports(id)

            return jsonify(ReportsFullSchema().dump(reports, many=True)), 200
