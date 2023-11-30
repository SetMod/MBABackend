from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import DatasourcesService

datasources_svc = DatasourcesService()
datasources_bp = Blueprint(name="datasources", import_name=__name__)
register_crud_routes(datasources_bp, datasources_svc)