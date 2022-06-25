import os
from app import VISUALIZATIONS_UPLOAD_FOLDER, db
from models.VisualizationsModel import Visualizations, VisualizationsSchema
import pandas as pd


class VisualizationsService():

    def __init__(self) -> None:
        self.visualizations_schema = VisualizationsSchema()

    def get_all_visualizations(self, dump: bool = True):
        try:
            visualizations = db.session.query(Visualizations).all()

            if len(visualizations) > 0:
                return self.visualizations_schema.dump(visualizations, many=True) if dump else visualizations
            else:
                return 'Visualizations not found'
        except Exception as err:
            print(err)
            return 'Failed to get visualizations'

    def get_visualization_by_id(self, visualization_id: int, dump: bool = True):
        try:
            visualization = db.session.query(Visualizations).where(
                Visualizations.visualization_id == visualization_id).first()

            if isinstance(visualization, Visualizations):
                return self.visualizations_schema.dump(visualization) if dump else visualization
            else:
                return 'Visualization not found'
        except Exception as err:
            print(err)
            return 'Failed to get visualization'

    def create_visualization(self, visualization: Visualizations, data: pd.DataFrame, dump: bool = True):
        try:
            db.session.add(visualization)
            db.session.commit()

            visualization_file_path = os.path.join(
                VISUALIZATIONS_UPLOAD_FOLDER, f'vd_{visualization.visualization_id}.csv')

            data.to_csv(visualization_file_path, index=False)
            visualization.visualization_image_path = visualization_file_path

            db.session.commit()
            return self.visualizations_schema.dump(visualization) if dump else visualization
        except Exception as err:
            print(err)
            return 'Failed to create visualization'

    def update_visualization(self, visualization_id: int, updated_visualization: Visualizations, dump: bool = True):
        visualization = self.get_visualization_by_id(
            visualization_id=visualization_id, dump=False)

        if not isinstance(visualization, Visualizations):
            return visualization

        visualization.visualization_name = updated_visualization.visualization_name
        visualization.report_id = updated_visualization.report_id
        try:
            db.session.commit()
            return self.visualizations_schema.dump(visualization) if dump else visualization
        except Exception as err:
            print(err)
            return 'Failed to update visualization'

    def delete_visualization(self, visualization_id: int, dump: bool = True):
        visualization = self.get_visualization_by_id(
            visualization_id=visualization_id, dump=False)

        if not isinstance(visualization, Visualizations):
            return visualization
        try:
            if os.path.exists(visualization.visualization_image_path):
                os.remove(visualization.visualization_image_path)
            db.session.delete(visualization)
            db.session.commit()
            return self.visualizations_schema.dump(visualization) if dump else visualization
        except Exception as err:
            print(err)
            return 'Failed to delete visualization'
