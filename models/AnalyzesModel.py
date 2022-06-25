from datetime import datetime
from app import db, ma


class Analyzes(db.Model):
    __tablename__ = "analyzes"

    analyze_id = db.Column(
        'analyze_id',
        db.Integer,
        primary_key=True)

    analyze_name = db.Column(
        'analyze_name',
        db.String(50),
        nullable=False)

    analyze_description = db.Column(
        'analyze_description',
        db.Text,
        nullable=False)

    analyze_support = db.Column(
        'analyze_support',
        db.Float,
        nullable=False)

    analyze_lift = db.Column(
        'analyze_lift',
        db.Float,
        nullable=False)

    analyze_confidence = db.Column(
        'analyze_confidence',
        db.Float,
        nullable=False)

    analyze_rules_length = db.Column(
        'analyze_rules_length',
        db.Integer,
        nullable=False)

    analyze_file_path = db.Column(
        'analyze_file_path',
        db.String(255),
        nullable=False)

    analyze_create_date = db.Column(
        'analyze_create_date',
        db.DateTime,
        default=datetime.utcnow)

    report_id = db.Column(
        'report_id',
        db.Integer,
        db.ForeignKey("reports.report_id"),
        nullable=False)

    report = db.relationship("Reports", backref="report_analyzes")

    def __repr__(self):
        return f'<Analyze(analyze_id={self.analyze_id},analyze_name={self.analyze_name},analyze_support={self.analyze_support},analyze_lift={self.analyze_lift},analyze_confidence={self.analyze_confidence},analyze_rules_length={self.analyze_rules_length},analyze_create_date={self.analyze_create_date},report_id={self.report_id})>'


class AnalyzesSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Analyzes
        include_fk = True
