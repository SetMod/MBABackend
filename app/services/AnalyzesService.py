import os
import pandas as pd
from marshmallow import ValidationError
from app import ANALYZES_UPLOAD_FOLDER, db
from app.MBAnalyze import MBAnalyze
from models.AnalyzesModel import Analyzes, AnalyzesSchema
from models.FilesModel import Files
from models.VisualizationsModel import Visualizations
from services.FilesService import FilesService
from services.VisualizationsService import VisualizationsService


class AnalyzesService():

    def __init__(self) -> None:
        self.files_service = FilesService()
        self.visualizations_service = VisualizationsService()
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

            if isinstance(analyze, Analyzes):
                return self.analyzes_schema.dump(analyze) if dump else analyze
            else:
                return 'Analyze not found'
        except Exception as err:
            print(err)
            return 'Failed to get analyze'

    def create_analyze(self, analyze: Analyzes, file_id: int, dump: bool = True):
        file = self.files_service.get_file_by_id(file_id, dump=False)
        if not isinstance(file, Files):
            return file

        mba = MBAnalyze(file_id=file.file_id, file_path=file.file_path, support=analyze.analyze_support,
                        lift=analyze.analyze_lift, confidence=analyze.analyze_confidence, rules_length=analyze.analyze_rules_length)
        # association_rules = mba.analyze()

        # analyze
        df = pd.read_csv(mba.file_path)
        print('Starting preprocessing...')
        preprocessed_df = mba.preprocess(df[:1000])
        print('DF INFO: ', preprocessed_df.info())
        print('DONE\n')
        print('Starting transforming...')
        df_set = mba.transform(df)
        print('DF SET INFO: ', df_set.info())
        print('DONE\n')
        print('Starting fpgrowth analyze...')
        frequent_itemsets = mba.create_frequent_itemsets(df_set)
        print('DONE\n')
        print('Starting creation of association rules...')
        association_rules = mba.create_association_rules(frequent_itemsets)
        print('DONE\n')

        if association_rules.empty:
            return 'No association rules were generated with specified options'

        # visualization
        [transactions_month_ser, transactions_cost_item] = mba.analyze_preprocess_data(
            preprocessed_df)
        top_items = mba.analyze_frequent_itemsets(frequent_itemsets)
        top_rules = mba.analyze_association_rules(association_rules)
        visualizations_data = [top_items, top_rules,
                               transactions_month_ser, transactions_cost_item]
        # print(transactions_month_ser.to_json(orient='split'))
        # print(transactions_month_ser.to_json(orient='split'))
        # print(top_items.to_json(orient='split'))
        # print(top_rules.to_json(orient='split'))
        for visualization_data in visualizations_data:
            new_visualization = Visualizations(
                visualization_name='Untitled', visualization_image_path='None', report_id=analyze.report_id)
            self.visualizations_service.create_visualization(
                new_visualization, visualization_data)

        analyze.analyze_file_path = 'None'
        try:
            db.session.add(analyze)
            db.session.commit()

            analyze_file_path = os.path.join(
                ANALYZES_UPLOAD_FOLDER, f'ar_{analyze.analyze_id}.csv')

            association_rules.to_csv(analyze_file_path, index=False)
            analyze.analyze_file_path = analyze_file_path

            db.session.commit()
            # return self.analyzes_schema.dump(analyze) if dump else analyze
            return association_rules
        except Exception as err:
            print(err)
            return 'Failed to create analyze'

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
            if os.path.exists(analyze.analyze_file_path):
                os.remove(analyze.analyze_file_path)
            db.session.delete(analyze)
            db.session.commit()
            return self.analyzes_schema.dump(analyze) if dump else analyze
        except Exception as err:
            print(err)
            return 'Failed to delete analyze'

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
