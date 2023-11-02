from re import L
from app import db
from app.models.AnalyzesModel import AnalyzesSchema
from app.models.VisualizationsModel import VisualizationsSchema
from app.models.ReportsModel import Reports, ReportsSchema


class ReportsService():

    def __init__(self) -> None:
        self.reports_schema = ReportsSchema()
        self.analyzes_schema = AnalyzesSchema()
        self.visualizations_schema = VisualizationsSchema()

    def get_all_reports(self, dump: bool = True):
        reports = db.session.query(Reports).all()

        if len(reports) > 0:
            return self.reports_schema.dump(reports, many=True) if dump else reports
        else:
            return None

    def get_report_by_id(self, report_id: int, dump: bool = True):
        report = db.session.query(Reports).where(
            Reports.report_id == report_id).first()

        if isinstance(report, Reports):
            return self.reports_schema.dump(report) if dump else report
        else:
            return None

    def get_report_analyzes(self, report_id: int, dump: bool = True):
        report = db.session.query(Reports).where(
            Reports.report_id == report_id).first()

        if report is not None and len(report.report_analyzes) > 0:
            return self.analyzes_schema.dump(report.report_analyzes, many=True) if dump else report.report_analyzes
        else:
            return None

    def get_report_visualizations(self, report_id: int, dump: bool = True):
        report = db.session.query(Reports).where(
            Reports.report_id == report_id).first()

        if report is not None and len(report.report_visualizations) > 0:
            return self.visualizations_schema.dump(report.report_visualizations, many=True) if dump else report.report_visualizations
        else:
            return None

    def create_report(self, report: Reports, dump: bool = True):
        try:
            db.session.add(report)
            db.session.commit()
            return self.reports_schema.dump(report) if dump else report
        except Exception:
            return None

    def update_report(self, report_id: int, updated_report: Reports, dump: bool = True):
        report = self.get_report_by_id(report_id=report_id, dump=False)

        try:
            if isinstance(report, Reports):
                report.report_name = updated_report.report_name
                report.report_data = updated_report.report_data
                report.user_id = updated_report.user_id
                report.organization_id = updated_report.organization_id
                db.session.commit()
                return self.reports_schema.dump(report) if dump else report
            else:
                return None
        except Exception:
            return None

    def delete_report(self, report_id: int, dump: bool = True):
        report = self.get_report_by_id(report_id=report_id, dump=False)
        try:
            if isinstance(report, Reports):
                db.session.delete(report)
                db.session.commit()
                return self.reports_schema.dump(report) if dump else report
            else:
                return None
        except Exception:
            return None

    def map_report(self, report_dict: dict):
        try:
            report = self.reports_schema.load(report_dict)
            report_name = report_dict['report_name']
            report_data = report_dict['report_data']
            user_id = report_dict['user_id']
            organization_id = report_dict['organization_id']
            report = Reports(report_name=report_name, report_data=report_data,
                             user_id=user_id, organization_id=organization_id)
            return report
        except Exception:
            return None
