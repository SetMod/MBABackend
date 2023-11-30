from flask import Blueprint
from app.routes.crud import register_crud_routes
from app.services import ReportsService

reports_svc = ReportsService()
reports_bp = Blueprint(name="reports", import_name=__name__)
register_crud_routes(reports_bp, reports_svc)
