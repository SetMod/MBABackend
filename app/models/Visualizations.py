from datetime import datetime
from sqlalchemy import true
from app import db, ma


class Visualizations(db.Model):
    __tablename__ = "visualizations"

    id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(50), nullable=False)

    image_file_path = db.Column("image_file_path", db.String(255), nullable=False)

    create_date = db.Column("create_date", db.DateTime, default=datetime.utcnow)

    report_id = db.Column(
        "report_id", db.Integer, db.ForeignKey("reports.id"), nullable=False
    )

    report = db.relationship("Reports", backref="report_visualizations")


class VisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visualizations
        include_fk = true
