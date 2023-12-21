from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.exceptions import CustomBadRequest
from app.models import Analyzes
from app.config import APP_ANALYZES_FOLDER
from app.routes.common import register_crud_routes
from app.services import analyzes_service
from app.logger import logger
import os
from app.AnalyzeOptions import analyze_options_schema, AnalyzeOptions

analyzes_bp = Blueprint(name="analyzes", import_name=__name__)
jwt_optional = False
register_crud_routes(analyzes_bp, analyzes_service)


@analyzes_bp.post("/analyze/<int:id>")
@jwt_required(optional=jwt_optional)
def start_analyze(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    analyze_options_dict: dict = request.json
    logger.info(analyze_options_dict)

    analyze_options: AnalyzeOptions = analyze_options_schema.load(analyze_options_dict)

    try:
        analyze = analyzes_service.analyze(id, analyze_options)
    except ValidationError as err:
        err_msg = err.messages
        # err_msg = f"Failed to map {self.model_name()} model due to {err}"
        logger.error(err_msg)
        raise CustomBadRequest(err_msg)

    return jsonify(analyzes_service.to_json(analyze))


@analyzes_bp.get("/analyze/<int:id>/status")
@jwt_required(optional=jwt_optional)
def get_analyze_status(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    analyze = analyzes_service.get_by_id(id)

    analyze_dict = analyzes_service.to_json(analyze)
    return jsonify({"status": analyze_dict["status"]})


@analyzes_bp.get("/download/<int:id>")
@jwt_required(optional=jwt_optional)
def download_file_by_id(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    analyze: Analyzes = analyzes_service.download_file(id)

    file_name = os.path.basename(analyze.file_path)
    return send_from_directory(
        directory=APP_ANALYZES_FOLDER,
        path=file_name,
        # download_name=analyze.name,
        as_attachment=True,
    )


@analyzes_bp.get("/preview/<int:id>")
@jwt_required(optional=jwt_optional)
def preview_file_by_id(id: int):
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    analyze: Analyzes = analyzes_service.download_file(id)

    file_name = os.path.basename(analyze.file_path)
    return send_from_directory(
        directory=APP_ANALYZES_FOLDER,
        path=file_name,
        # download_name=analyze.name,
        as_attachment=True,
    )
