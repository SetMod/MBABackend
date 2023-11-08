from app.models import GenericModel
from app.init import db, ma


class Visualizations(db.Model, GenericModel):
    __tablename__ = "visualizations"

    name = db.Column("name", db.String(50), nullable=False)

    image_file_path = db.Column("image_file_path", db.String(255), nullable=False)

    report_id = db.Column(
        "report_id", db.Integer, db.ForeignKey("reports.id"), nullable=False
    )

    report = db.relationship("Reports", backref="report_visualizations")


class VisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visualizations
        include_fk = True
