from flask import Blueprint
from app.logger import logger
from app.routes.GenericRoute import GenericRoute
from app.services import DatasourcesService


class DatasourcesRoute(GenericRoute):
    bp = Blueprint(name="datasources", import_name=__name__)
    datasources_svc = DatasourcesService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.datasources_svc)
        super().register_routes()
