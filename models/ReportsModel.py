from datetime import datetime
from app import db, ma


class Reports(db.Model):
    __tablename__ = "reports"

    report_id = db.Column(
        'report_id',
        db.Integer,
        primary_key=True)

    report_name = db.Column(
        'report_name',
        db.String(100),
        nullable=False)

    report_data = db.Column(
        'report_data',
        db.Text,
        nullable=False)

    report_create_date = db.Column(
        'report_create_date',
        db.DateTime,
        default=datetime.utcnow)

    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey("users.user_id"))

    organization_id = db.Column(
        'organization_id',
        db.Integer,
        db.ForeignKey("organizations.organization_id"),
        nullable=False)

    user = db.relationship("Users", backref="user_reports")
    organization = db.relationship(
        "Organizations", backref="organization_reports")

    def __repr__(self):
        return f'<Report(report_id={self.report_id},report_name={self.report_name},report_create_date={self.report_create_date},user_id={self.user_id},organization_id={self.organization_id})>'


class ReportsSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Reports
    user_id = ma.auto_field()
    organization_id = ma.auto_field()
