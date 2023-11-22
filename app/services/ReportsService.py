from typing import List
from app.logger import logger
from app.models import Reports, Visualizations
from app.schemas import ReportsSchema
from app.services.GenericService import GenericService


class ReportsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=ReportsSchema(), model_class=Reports)

    def get_all_visualizations(self, id: int) -> List[Visualizations]:
        logger.info(f"Get {self.model_class._name()} visualizations")

        report: Reports = self.get_by_id(id)
        visualizations: List[Visualizations] = report.visualizations

        logger.info(
            f"Found {self.model_class._name()} visualizations: {visualizations}"
        )

        return visualizations
