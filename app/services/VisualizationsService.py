import os
from app import VISUALIZATIONS_UPLOAD_FOLDER, db
from app.models import Visualizations, VisualizationsSchema
import pandas as pd


class VisualizationsService:
    def __init__(self) -> None:
        self.visualizations_schema = VisualizationsSchema()

    def get_all_visualizations(self, dump: bool = True):
        try:
            visualizations = db.session.query(Visualizations).all()

            if len(visualizations) > 0:
                return (
                    self.visualizations_schema.dump(visualizations, many=True)
                    if dump
                    else visualizations
                )
            else:
                return "Visualizations not found"
        except Exception as err:
            print(err)
            return "Failed to get visualizations"

    def get_visualization_by_id(self, id: int, dump: bool = True):
        try:
            visualization = (
                db.session.query(Visualizations).where(Visualizations.id == id).first()
            )

            if isinstance(visualization, Visualizations):
                return (
                    self.visualizations_schema.dump(visualization)
                    if dump
                    else visualization
                )
            else:
                return "Visualization not found"
        except Exception as err:
            print(err)
            return "Failed to get visualization"

    def create_visualization(
        self, visualization: Visualizations, data: pd.DataFrame, dump: bool = True
    ):
        try:
            db.session.add(visualization)
            db.session.commit()

            visualization_file_path = os.path.join(
                VISUALIZATIONS_UPLOAD_FOLDER, f"vd_{visualization.id}.csv"
            )

            data.to_csv(visualization_file_path, index=False)
            visualization.image_file_path = visualization_file_path

            db.session.commit()
            return (
                self.visualizations_schema.dump(visualization)
                if dump
                else visualization
            )
        except Exception as err:
            print(err)
            return "Failed to create visualization"

    def update_visualization(
        self, id: int, updated_visualization: Visualizations, dump: bool = True
    ):
        visualization = self.get_visualization_by_id(id=id, dump=False)

        if not isinstance(visualization, Visualizations):
            return visualization

        visualization.name = updated_visualization.name
        visualization.report_id = updated_visualization.report_id
        try:
            db.session.commit()
            return (
                self.visualizations_schema.dump(visualization)
                if dump
                else visualization
            )
        except Exception as err:
            print(err)
            return "Failed to update visualization"

    def delete_visualization(self, id: int, dump: bool = True):
        visualization = self.get_visualization_by_id(id=id, dump=False)

        if not isinstance(visualization, Visualizations):
            return visualization
        try:
            if os.path.exists(visualization.image_file_path):
                os.remove(visualization.image_file_path)
            db.session.delete(visualization)
            db.session.commit()
            return (
                self.visualizations_schema.dump(visualization)
                if dump
                else visualization
            )
        except Exception as err:
            print(err)
            return "Failed to delete visualization"
