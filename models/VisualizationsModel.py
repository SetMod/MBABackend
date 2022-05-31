from datetime import datetime
from app import db, ma


class Visualizations(db.Model):
    __tablename__ = "visualizations"

    visualization_id = db.Column(
        'visualization_id',
        db.Integer,
        primary_key=True)

    visualization_name = db.Column(
        'visualization_name',
        db.String(50),
        nullable=False)

    visualization_image_path = db.Column(
        'visualization_image_path',
        db.String(255),
        nullable=False)

    visualization_create_date = db.Column(
        'visualization_create_date',
        db.DateTime,
        default=datetime.utcnow)

    report_id = db.Column(
        'report_id',
        db.Integer,
        db.ForeignKey("reports.report_id"),
        nullable=False)

    report = db.relationship("Reports", backref="report_visualizations")


class VisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Visualizations
    report_id = ma.auto_field()
