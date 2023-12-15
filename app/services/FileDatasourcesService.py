from app.models import FileDatasources
from app.schemas import DatasourcesTypeFullSchema
from app.services.GenericService import GenericService


class FileDatasourcesService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=DatasourcesTypeFullSchema(), model_class=FileDatasources
        )
