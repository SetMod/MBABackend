from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.routes.common import register_crud_routes
from app.services import reports_service, visualizations_service

reports_bp = Blueprint(name="reports", import_name=__name__)
jwt_optional = False
register_crud_routes(reports_bp, reports_service, jwt_optional)


@reports_bp.get("/<int:id>/visualizations")
@jwt_required(optional=jwt_optional)
def get_all_visualizations(id: int):
    user_visualizations = reports_service.get_all_visualizations(id)

    return jsonify(visualizations_service.to_json(user_visualizations)), 200
