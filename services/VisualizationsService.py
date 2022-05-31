from app import db
from models.VisualizationsModel import Visualizations, VisualizationsSchema


class VisualizationsService():

    def __init__(self) -> None:
        self.visualizations_schema = VisualizationsSchema()

    def get_all_visualizations(self, dump: bool = True):
        visualizations = db.session.query(Visualizations).all()
        return self.visualizations_schema.dump(visualizations, many=True) if dump else visualizations

    def get_visualization_by_id(self, visualization_id: int, dump: bool = True):
        visualization = db.session.query(Visualizations).where(
            Visualizations.visualization_id == visualization_id).first()
        return self.visualizations_schema.dump(visualization) if dump else visualization

    def create_visualization(self, visualization: Visualizations, dump: bool = True):
        db.session.add(visualization)
        db.session.commit()
        return self.visualizations_schema.dump(visualization) if dump else visualization

    def update_visualization(self, visualization_id: int, updated_visualization: Visualizations, dump: bool = True):
        visualization = self.get_visualization_by_id(
            visualization_id=visualization_id, dump=False)
        if isinstance(visualization, Visualizations):
            visualization.visualization_name = updated_visualization.visualization_name
            visualization.visualization_image_path = updated_visualization.visualization_image_path
            visualization.report_id = updated_visualization.report_id
            db.session.commit()
        return self.visualizations_schema.dump(visualization) if dump else visualization

    def delete_visualization(self, visualization_id: int, dump: bool = True):
        visualization = self.get_visualization_by_id(
            visualization_id=visualization_id, dump=False)
        if isinstance(visualization, Visualizations):
            db.session.delete(visualization)
            db.session.commit()
        return self.visualizations_schema.dump(visualization) if dump else visualization
