from app.config import VISUALIZATIONS_UPLOAD_FOLDER
from app.models import Visualizations, VisualizationsSchema
from app.services import GenericService
from app.init import db
import pandas as pd
import os


class VisualizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=VisualizationsSchema(), model_class=Visualizations)

    def create_visualization(
        self, visualization: Visualizations, data: pd.DataFrame, dump: bool = True
    ):
        db.session.add(visualization)
        db.session.commit()

        visualization_file_path = os.path.join(
            VISUALIZATIONS_UPLOAD_FOLDER, f"vd_{visualization.id}.csv"
        )

        data.to_csv(visualization_file_path, index=False)
        visualization.image_file_path = visualization_file_path

        db.session.commit()

        return self.schema.dump(visualization) if dump else visualization

    def delete_visualization(self, id: int, dump: bool = True):
        visualization = self.get_visualization_by_id(id=id, dump=False)

        if not isinstance(visualization, Visualizations):
            return visualization
        if os.path.exists(visualization.image_file_path):
            os.remove(visualization.image_file_path)
        db.session.delete(visualization)
        db.session.commit()

        return self.schema.dump(visualization) if dump else visualization
