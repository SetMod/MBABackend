from datetime import datetime
from app import db, ma


class Reports(db.Model):
    __tablename__ = "reports"

    id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(100), nullable=False)

    data_points = db.Column("data_points", db.Text, nullable=False)

    create_date = db.Column("create_date", db.DateTime, default=datetime.utcnow)

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

    organization_id = db.Column(
        "organization_id", db.Integer, db.ForeignKey("organizations.id"), nullable=False
    )

    user = db.relationship("Users", backref="user_reports")
    organization = db.relationship("Organizations", backref="organization_reports")

    def __repr__(self):
        return f"<Report(id={self.id},name={self.name},create_date={self.create_date},user_id={self.user_id},organization_id={self.organization_id})>"


class ReportsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reports

    user_id = ma.auto_field()
    organization_id = ma.auto_field()
