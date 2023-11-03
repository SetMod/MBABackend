from datetime import datetime
from app import db, ma


class Analyzes(db.Model):
    __tablename__ = "analyzes"

    id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(50), nullable=False)

    description = db.Column("description", db.Text, nullable=False)

    support = db.Column("support", db.Float, nullable=False)

    lift = db.Column("lift", db.Float, nullable=False)

    confidence = db.Column("confidence", db.Float, nullable=False)

    rules_length = db.Column("rules_length", db.Integer, nullable=False)

    file_path = db.Column("file_path", db.String(255), nullable=False)

    create_date = db.Column("create_date", db.DateTime, default=datetime.utcnow)

    report_id = db.Column(
        "report_id", db.Integer, db.ForeignKey("reports.id"), nullable=False
    )

    report = db.relationship("Reports", backref="report_analyzes")

    def __repr__(self):
        return f"<Analyze(id={self.id},name={self.name},support={self.support},lift={self.lift},confidence={self.confidence},rules_length={self.rules_length},create_date={self.create_date},report_id={self.report_id})>"


class AnalyzesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Analyzes
        include_fk = True
