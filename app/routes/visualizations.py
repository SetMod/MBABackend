from typing import List
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.routes.common import register_crud_routes
from app.logger import logger
from app.services import visualizations_service

visualizations_bp = Blueprint(name="visualizations", import_name=__name__)
jwt_optional = False
register_crud_routes(visualizations_bp, visualizations_service, jwt_optional)


@visualizations_bp.post("/many")
@jwt_required(optional=jwt_optional)
def create_many():
    logger.info(f"{request.remote_addr} - {request.method} {request.full_path}")

    visualizations_list: List[dict] = request.json
    for visualization_dict in visualizations_list:
        if "id" in visualization_dict:
            visualization_dict.pop("id")
        new_model = visualizations_service.create(visualization_dict)

    return "", 201
