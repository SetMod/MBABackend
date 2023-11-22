import os
from pathlib import Path
import pandas as pd
from app.config import APP_VISUALIZATIONS_FOLDER
from werkzeug.utils import secure_filename
from app.logger import logger
from app.db import db
from app.models import FileVisualizations
from app.schemas import FileVisualizationsSchema
from app.services.GenericService import GenericService


class FileVisualizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=FileVisualizationsSchema(), model_class=FileVisualizations
        )

    def create(self, new_file_visualization_dict: dict) -> FileVisualizations:
        logger.info(f"Creating new {self.model_class._name}")

        self.get_by_unique_fields(new_file_visualization_dict, must_exist=False)

        new_file_visualization: FileVisualizations = self.map_model(
            new_file_visualization_dict
        )

        visualization_file_path = Path(
            APP_VISUALIZATIONS_FOLDER,
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

    def delete(self, id: int) -> FileVisualizations:
        logger.info(f"Deleting {self.model_class._name()} with id='{id}'")

        existing_file_visualization: FileVisualizations = self.get_by_id(id)
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
