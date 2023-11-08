from app.models import AnalyzesSchema, VisualizationsSchema, Reports, ReportsSchema
from app.services import GenericService
from app.init import db


class ReportsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=ReportsSchema(), model_class=Reports)
        self.analyzes_schema = AnalyzesSchema()
        self.visualizations_schema = VisualizationsSchema()

    def get_report_analyzes(self, id: int, dump: bool = True):
        report = db.session.query(Reports).where(Reports.id == id).first()

        if not isinstance(report, Reports):
            return None

        return (
            self.analyzes_schema.dump(report.report_analyzes, many=True)
            if dump
            else report.report_analyzes
        )

    def get_report_visualizations(self, id: int, dump: bool = True):
        report = db.session.query(Reports).where(Reports.id == id).first()

        if not isinstance(report, Reports):
            return None

        return (
            self.visualizations_schema.dump(report.report_visualizations, many=True)
            if dump
            else report.report_visualizations
        )
