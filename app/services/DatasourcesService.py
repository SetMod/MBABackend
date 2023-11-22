from app.models import Datasources
from app.schemas import DatasourcesSchema
from app.services.GenericService import GenericService


class DatasourcesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=DatasourcesSchema(), model_class=Datasources)
