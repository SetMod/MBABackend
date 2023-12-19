from datetime import datetime
import os
from pathlib import Path
import pandas as pd
from app.exceptions import CustomBadRequest, CustomNotFound
from app.utils import generate_unique_filename
import model.MBAnalyze as mba
from app.config import APP_ANALYZES_FOLDER
from app.logger import logger
from app.db import db
from app.models import AnalyzeStatus, Analyzes, Datasources, Visualizations
from app.schemas import AnalyzesSchema
from app.services.GenericService import GenericService
from app.AnalyzeOptions import AnalyzeOptions

# from app.services.FileDatasourcesService import FileDatasourcesService
# from app.services.VisualizationsService import VisualizationsService


class AnalyzesService(GenericService):
    # files_service = FileDatasourcesService()
    # visualizations_service = VisualizationsService()

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

    def analyze(self, id: int, analyze_options: AnalyzeOptions):
        logger.info(f"Analyzing analyze with id='{id}'")

        analyze: Analyzes = self.get_by_id(id)

        # mba = MBAnalyze(
        #     id=file.id,
        #     file_path=file.file_path,
        #     support=analyze.support,
        #     lift=analyze.lift,
        #     confidence=analyze.confidence,
        #     rules_length=analyze.rules_length,
        # )
        # association_rules = mba.analyze()

        # file_path = Path(analyze.file_path)

        # if analyze.file_path and file_path.exists() and analyze_options.recreate:
        #     os.remove(analyze.file_path)
        # elif file_path.exists():
        #     err_msg = "File path already exists"
        #     logger.warning(err_msg)
        #     raise CustomBadRequest(err_msg)

        unique_filename = generate_unique_filename(
            file_prefix="fd", file_extension="csv"
        )

        unique_file_path = APP_ANALYZES_FOLDER.joinpath(unique_filename)

        if unique_file_path.exists():
            err_msg = "File path already exists"
            logger.warning(err_msg)
            raise CustomBadRequest(err_msg)

        if not APP_ANALYZES_FOLDER.exists():
            logger.info(f"Creating analyzes dir at '{APP_ANALYZES_FOLDER.as_posix()}'")
            os.makedirs(APP_ANALYZES_FOLDER)

        analyze.file_path = unique_file_path.as_posix()

        analyze.started_date = datetime.utcnow()
        analyze.status = AnalyzeStatus.STARTED
        self.commit()

        analyze.status = AnalyzeStatus.IN_PROGRESS
        self.commit()
        # analyze
        try:
            logger.info(
                f"Reading data with pandas from '{analyze.datasource.file_path}'"
            )
            df = pd.read_csv(analyze.datasource.file_path)

            preprocessed_df = mba.preprocess(df=df[:1000])

            df_set = mba.transform(df=preprocessed_df)

            frequent_itemsets = mba.get_frequent_itemsets(
                df=df_set,
                min_support=analyze.support,
                rules_max_length=analyze.rules_length,
                algorithm=mba.Algorithm.FPGROWTH,
            )

            if frequent_itemsets.empty:
                err_msg = (
                    "Frequent itemsets are empty. No data to form association rules"
                )
                logger.warning(err_msg)
                raise Exception(err_msg)

            association_rules = mba.get_association_rules(
                frequent_itemsets=frequent_itemsets,
                metric=mba.Metric.SUPPORT,
                metric_min_threshold=analyze.support,
            )

            if association_rules.empty:
                err_msg = "Association rules are empty. Please, specify different thresholds for metrics, exiting"
                logger.warning(err_msg)
                raise Exception(err_msg)

            ######################################
            # Save association rules to CSV file #
            ######################################

            association_rules["antecedents"] = association_rules["antecedents"].apply(
                lambda x: ", ".join(x)
            )
            association_rules["consequents"] = association_rules["consequents"].apply(
                lambda x: ", ".join(x)
            )
            association_rules.to_csv(analyze.file_path, index=False)

            analyze.status = AnalyzeStatus.FINISHED

            #################
            # Update logic and move to visualization service
            # visualization #
            #################

            # top_highest_cost_items = mba.get_top_highest_cost_items(df=preprocessed_df)
            # transactions_number_per_month = mba.get_transactions_number_per_month(
            #     df=preprocessed_df
            # )

            # top_items = mba.get_top_frequent_itemsets(frequent_itemsets)
            # top_rules = mba.get_top_association_rules(association_rules)
            # visualizations_data = [
            #     top_items,
            #     top_rules,
            #     transactions_number_per_month,
            #     top_highest_cost_items,
            # ]

            # for visualization_data in visualizations_data:
            #     new_visualization = Visualizations(
            #         name="Untitled",
            #         image_file_path="None",
            #         report_id=analyze.report_id,
            #     )
            #     self.visualizations_service.create_visualization(
            #         visualization=new_visualization,
            #         visualization_data=visualization_data,
            #     )

            # analyze.file_path = "None"

            # db.session.add(analyze)
            # db.session.commit()

            # file_path = os.path.join(APP_ANALYZES_FOLDER, f"ar_{analyze.id}.csv")

            # if os.path.exists(file_path):
            #     logger.warn(f"File {file_path} already exists")

            # # Move file path, and other related data to Files model and store foreign key
            # analyze.file_path = file_path
            # association_rules.to_csv(file_path, index=False)

            # analyze.status = AnalyzeStatus.FINISHED

        except Exception as err:
            err_msg = f"Failed to analyze data for analyze with id='{id}'"
            analyze.status = AnalyzeStatus.FAILED
            logger.error(err_msg)
            logger.exception(err)

        analyze.finished_date = datetime.utcnow()
        self.commit()

        return analyze

    def download_file(self, id: int):
        analyze: Analyzes = self.get_by_id(id)

        if not os.path.exists(analyze.file_path):
            err_msg = f"File datasource file  doesn't exists at '{analyze.file_path}'"
            logger.warning(err_msg)
            raise CustomNotFound(err_msg)

        return analyze

    def delete_analyze(self, id: int):
        analyze = self.get_by_id(id=id, dump=False)

        if not isinstance(analyze, Analyzes):
            return None

        if os.path.exists(analyze.file_path):
            os.remove(analyze.file_path)

        db.session.delete(analyze)
        self.commit()

        return analyze
