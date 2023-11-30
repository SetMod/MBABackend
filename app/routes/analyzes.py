from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import AnalyzesService

analyzes_svc = AnalyzesService()
analyzes_bp = Blueprint(name="analyzes", import_name=__name__)
register_crud_routes(analyzes_bp, analyzes_svc)
