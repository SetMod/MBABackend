from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import analyzes_service

analyzes_bp = Blueprint(name="analyzes", import_name=__name__)
register_crud_routes(analyzes_bp, analyzes_service)
