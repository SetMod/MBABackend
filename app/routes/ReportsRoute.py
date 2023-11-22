from flask import Blueprint
from app.routes.GenericRoute import GenericRoute
from app.services import ReportsService


class ReportsRoute(GenericRoute):
    bp = Blueprint(name="reports", import_name=__name__)
    reports_svc = ReportsService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.reports_svc)
        super().register_routes()
