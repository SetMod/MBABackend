from app.models import Visualizations
from app.schemas import VisualizationsSchema
from app.services.GenericService import GenericService


class VisualizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=VisualizationsSchema(), model_class=Visualizations)
