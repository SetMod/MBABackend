from flask import Blueprint
from app.routes.GenericRoute import GenericRoute
from app.services import VisualizationsService


class VisualizationsRoute(GenericRoute):
    bp = Blueprint(name="visualizations", import_name=__name__)
    visualizations_svc = VisualizationsService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.visualizations_svc)
        super().register_routes()
