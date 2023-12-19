from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from app.models import DatasourceTypes, Datasources
from app.routes.common import register_crud_routes
from app.schemas import DatasourcesFullSchema
from app.services import datasources_service
from app.config import APP_UPLOAD_FOLDER
from app.logger import logger
from app.exceptions import CustomBadRequest
import json
import os

datasources_bp = Blueprint(name="datasources", import_name=__name__)
jwt_optional = False
register_crud_routes(datasources_bp, datasources_service, jwt_optional)


@datasources_bp.get("/full")
@jwt_required(optional=jwt_optional)
def get_full():
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    datasources = datasources_service.get_all()
    return (
        jsonify(DatasourcesFullSchema().dump(datasources, many=True)),
        200,
    )


@datasources_bp.get("/<int:id>/full")
@jwt_required(optional=jwt_optional)
def get_by_id_full(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    datasource = datasources_service.get_by_id(id)

    return jsonify(DatasourcesFullSchema().dump(datasource)), 200


@datasources_bp.post("/upload")
@jwt_required(optional=jwt_optional)
def create_file():
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    file = request.files.get("file")
    file_datasource_dict = request.form.get("file_datasource")

    if file is None:
        err_msg = "No 'file' part in request"
        logger.warning(err_msg)
        raise CustomBadRequest(err_msg)

    if file_datasource_dict is None:
        err_msg = "No 'file_datasource' part in request form"
        logger.warning(err_msg)
        raise CustomBadRequest(err_msg)

    file_datasource_dict = json.loads(file_datasource_dict)
    if "id" in file_datasource_dict:
        file_datasource_dict.pop("id")

    new_file_datasource = datasources_service.create_file(file_datasource_dict, file)

    return jsonify(datasources_service.to_json(new_file_datasource))


@datasources_bp.get("/download/<int:id>")
@jwt_required(optional=jwt_optional)
def download_file_by_id(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    file_datasource: Datasources = datasources_service.get_by_id(id)

    file_path = os.path.basename(file_datasource.file_path)

    return send_from_directory(
        directory=APP_UPLOAD_FOLDER,
        path=file_path,
        # download_name=file_datasource.name,
        as_attachment=True,
    )
