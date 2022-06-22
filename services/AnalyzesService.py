from marshmallow import ValidationError
from sqlalchemy import null
from app import db
from models.AnalyzesModel import Analyzes, AnalyzesSchema


class AnalyzesService():

    def __init__(self) -> None:
        self.analyzes_schema = AnalyzesSchema()

    def get_all_analyzes(self, dump: bool = True):
        try:
            analyzes = db.session.query(Analyzes).all()

            if len(analyzes) > 0:
                return self.analyzes_schema.dump(analyzes, many=True) if dump else analyzes
            else:
                return 'Analyzes not found'
        except Exception as e:
            print(e)
            return 'Failed to get analyzes'

    def get_analyze_by_id(self, analyze_id: int, dump: bool = True):
        try:
            analyze = db.session.query(Analyzes).where(
                Analyzes.analyze_id == analyze_id).first()

            if isinstance(analyze, analyze):
                return self.analyzes_schema.dump(analyze) if dump else analyze
            else:
                return 'Analyze not found'
        except Exception as err:
            print(err)
            return 'Failed to get analyze'

    def create_analyze(self, analyze: Analyzes, dump: bool = True):
        try:
            db.session.add(analyze)
            db.session.commit()
            return self.analyzes_schema.dump(analyze) if dump else analyze
        except Exception as err:
            print(err)
            return 'Failed to create new analyze'

    def update_analyze(self, analyze_id: int, updated_analyze: Analyzes, dump: bool = True):
        analyze = self.get_analyze_by_id(analyze_id=analyze_id, dump=False)

        if not isinstance(analyze, Analyzes):
            return analyze

        analyze.analyze_name = updated_analyze.analyze_name
        analyze.analyze_description = updated_analyze.analyze_description
        analyze.analyze_support = updated_analyze.analyze_support
        analyze.analyze_lift = updated_analyze.analyze_lift
        analyze.analyze_confidence = updated_analyze.analyze_confidence
        analyze.analyze_rules_length = updated_analyze.analyze_rules_length
        # analyze.analyze_file_path = updated_analyze.analyze_file_path
        analyze.report_id = updated_analyze.report_id

        try:
            db.session.commit()
            return self.analyzes_schema.dump(analyze) if dump else analyze
        except Exception as err:
            print(err)
            return 'Failed to update analyze'

    def delete_analyze(self, analyze_id: int, dump: bool = True):
        analyze = self.get_analyze_by_id(analyze_id=analyze_id, dump=False)

        if not isinstance(analyze, Analyzes):
            return None

        try:
            db.session.delete(analyze)
            db.session.commit()
            return self.analyzes_schema.dump(analyze) if dump else analyze
        except Exception:
            return None

    def map_analyze(self, analyze_dict: dict):
        try:
            analyze = self.analyzes_schema.load(analyze_dict)
            analyze_name = analyze_dict['analyze_name']
            analyze_description = analyze_dict['analyze_description']
            analyze_support = analyze_dict['analyze_support']
            analyze_lift = analyze_dict['analyze_lift']
            analyze_confidence = analyze_dict['analyze_confidence']
            analyze_rules_length = analyze_dict['analyze_rules_length']
            # analyze_file_path = analyze_dict['analyze_file_path']
            report_id = analyze_dict['report_id']
            analyze = Analyzes(analyze_name=analyze_name, analyze_description=analyze_description,
                               analyze_support=analyze_support, analyze_lift=analyze_lift,
                               analyze_confidence=analyze_confidence, analyze_rules_length=analyze_rules_length, report_id=report_id)
            return analyze
        except ValidationError as err:
            return err.messages
