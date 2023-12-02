from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import visualizations_service

visualizations_bp = Blueprint(name="visualizations", import_name=__name__)
register_crud_routes(visualizations_bp, visualizations_service)
