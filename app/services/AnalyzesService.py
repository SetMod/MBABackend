import os
import pandas as pd
import model.MBAnalyze as mba
from app.config import APP_ANALYZES_FOLDER
from app.logger import logger
from app.db import db
from app.models import Analyzes, FileDatasources, Visualizations
from app.schemas import AnalyzesSchema, FileDatasourcesSchema
from app.services.GenericService import GenericService
from app.services.VisualizationsService import VisualizationsService


class AnalyzesService(GenericService):
    files_service = FileDatasourcesSchema()
    visualizations_service = VisualizationsService()

    def __init__(self) -> None:
        super().__init__(schema=AnalyzesSchema(), model_class=Analyzes)

    def get_association_rules(self, id: int):
        analyze = self.get_by_id(id=id, dump=False)

        if not isinstance(analyze, Analyzes):
            return

        if not os.path.exists(analyze.file_path):
            logger.warn(f"File {analyze.file_path} doesn't exists")

        association_rules = pd.read_csv(analyze.file_path)
        return association_rules

    def create_analyze(self, analyze: Analyzes, id: int, dump: bool = True):
        file = self.files_service.get_file_by_id(id, dump=False)
        if not isinstance(file, FileDatasources):
            return file

        # mba = MBAnalyze(
        #     id=file.id,
        #     file_path=file.file_path,
        #     support=analyze.support,
        #     lift=analyze.lift,
        #     confidence=analyze.confidence,
        #     rules_length=analyze.rules_length,
        # )
        # association_rules = mba.analyze()

        # analyze
        df = pd.read_csv(file.file_path)
        preprocessed_df = mba.preprocess(df=df[:1000])
        df_set = mba.transform(df=df)
        frequent_itemsets = mba.get_frequent_itemsets(
            df=df_set,
            min_support=analyze.support,
            rules_max_length=analyze.rules_length,
            algorithm=mba.Algorithm.FPGROWTH,
        )

        if frequent_itemsets.empty:
            logger.warning(
                "Frequent itemsets are empty. No data to form association rules, exiting"
            )
            return

        association_rules = mba.get_association_rules(
            frequent_itemsets=frequent_itemsets,
            metric=mba.Metric.SUPPORT,
            metric_min_threshold=analyze.support,
        )

        if association_rules.empty:
            logger.warning(
                "Association rules are empty. Please, specify different thresholds for metrics, exiting"
            )
            return

        #################
        # visualization #
        #################

        top_highest_cost_items = mba.get_top_highest_cost_items(df=preprocessed_df)
        transactions_number_per_month = mba.get_transactions_number_per_month(
            df=preprocessed_df
        )

        top_items = mba.get_top_frequent_itemsets(frequent_itemsets)
        top_rules = mba.get_top_association_rules(association_rules)
        visualizations_data = [
            top_items,
            top_rules,
            transactions_number_per_month,
            top_highest_cost_items,
        ]

        for visualization_data in visualizations_data:
            new_visualization = Visualizations(
                name="Untitled",
                image_file_path="None",
                report_id=analyze.report_id,
            )
            self.visualizations_service.create_visualization(
                visualization=new_visualization, visualization_data=visualization_data
            )

        analyze.file_path = "None"

        db.session.add(analyze)
        db.session.commit()

        file_path = os.path.join(APP_ANALYZES_FOLDER, f"ar_{analyze.id}.csv")

        if os.path.exists(file_path):
            logger.warn(f"File {file_path} already exists")

        # Move file path, and other related data to Files model and store foreign key
        analyze.file_path = file_path
        association_rules.to_csv(file_path, index=False)

        db.session.commit()

        return self.schema.dump(analyze) if dump else analyze

    def delete_analyze(self, id: int, dump: bool = True):
        analyze = self.get_by_id(id=id, dump=False)

        if not isinstance(analyze, Analyzes):
            return None

        if os.path.exists(analyze.file_path):
            os.remove(analyze.file_path)
        db.session.delete(analyze)
        db.session.commit()

        return self.schema.dump(analyze) if dump else analyze
