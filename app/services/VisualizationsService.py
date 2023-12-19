from app.models import Visualizations
from app.schemas import VisualizationsSchema
from app.services.GenericService import GenericService
from app.config import APP_VISUALIZATIONS_FOLDER
from werkzeug.utils import secure_filename
from app.logger import logger
from pathlib import Path
from app.db import db
import pandas as pd


class VisualizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=VisualizationsSchema(), model_class=Visualizations)

    def create_file(self, new_file_visualization_dict: dict) -> Visualizations:
        logger.info(f"Creating new {self.model_class._name}")

        self.get_by_unique_fields(new_file_visualization_dict, must_exist=False)

        new_file_visualization: Visualizations = self.map_model(
            new_file_visualization_dict
        )

        visualization_file_path = APP_VISUALIZATIONS_FOLDER.joinpath(
            secure_filename(f"vd_{new_file_visualization.id}.csv"),
        )

        new_file_visualization.file_path = visualization_file_path
        db.session.add(new_file_visualization)
        self.commit()

        # logger.info(
        #     f"Creating {self.model_class._name()} file: {new_file_visualization.file_path}"
        # )
        # data.to_csv(visualization_file_path, index=False)

        logger.info(
            f"Successfully created new {self.model_class._name()} with id='{new_file_visualization.id}'"
        )

        return new_file_visualization

    def delete_file(self, id: int) -> Visualizations:
        logger.info(f"Deleting {self.model_class._name()} with id='{id}'")

        existing_file_visualization: Visualizations = self.get_by_id(id)
        if os.path.exists(existing_file_visualization.file_path):
            logger.info(
                f"Deleting {self.model_class._name()} file: {existing_file_visualization.file_path}"
            )
            os.remove(existing_file_visualization.file_path)

        db.session.delete(existing_file_visualization)
        self.commit()

        logger.info(
            f"Successfully deleted {self.model_class._name()} with id='{existing_file_visualization.id}'"
        )

        return existing_file_visualization
