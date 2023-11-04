from werkzeug.utils import secure_filename
from app.models import (
    Roles,
    RolesSchema,
    UsersOrganizations,
    UsersOrganizationsSchema,
    OrganizationRoles,
    OrganizationRolesSchema,
    Users,
    UsersSchema,
    Organizations,
    OrganizationsSchema,
    Files,
    FilesSchema,
    ReportsSchema,
    Visualizations,
    VisualizationsSchema,
    Analyzes,
    AnalyzesSchema,
)
from app.services import GenericService
from app.config import (
    UPLOAD_FOLDER,
    VISUALIZATIONS_UPLOAD_FOLDER,
    ANALYZES_UPLOAD_FOLDER,
)
from app import db
from app.MBAnalyze import MBAnalyze
from cgi import FieldStorage
import pandas as pd
import os


class RolesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=RolesSchema(), model_class=Roles)


class FilesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=FilesSchema(), model_class=Files)

    def create_file(self, file: Files, csv_file: FieldStorage, dump: bool = True):
        try:
            db.session.add(file)
            db.session.commit()

            file_path = os.path.join(
                UPLOAD_FOLDER, secure_filename(f"file_{file.id}.csv")
            )
            file.file_path = file_path
            csv_file.save(file.file_path)

            db.session.commit()
            return self.files_schema.dump(file) if dump else file
        except Exception as err:
            print(err)
            return "Failed to create file"


class OrganizationRolesService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=OrganizationRolesSchema(), model_class=OrganizationRoles
        )


class UsersOrganizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=UsersOrganizationsSchema(), model_class=UsersOrganizations
        )
        self.organization_roles_schema = OrganizationRolesSchema()
        self.organization_roles_service = OrganizationRolesService()


class UsersService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=UsersSchema(), model_class=Users)
        self.users_organizations_service = UsersOrganizationsService()
        self.organization_roles_service = OrganizationRolesService()
        self.roles_service = RolesService()
        self.reports_schema = ReportsSchema()
        self.organizations_schema = OrganizationsSchema()
        self.roles_schema = RolesSchema()
        self.files_schema = FilesSchema()


class OrganizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=OrganizationsSchema(), model_class=Organizations)
        self.users_service = UsersService()
        self.organization_roles_service = OrganizationRolesService()
        self.users_organizations_service = UsersOrganizationsService()
        self.organization_roles_schema = OrganizationRolesSchema()
        self.users_schema = UsersSchema()
        self.files_schema = FilesSchema()
        self.reports_schema = ReportsSchema()


class VisualizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=VisualizationsSchema(), model_class=Visualizations)

    def create_visualization(
        self, visualization: Visualizations, data: pd.DataFrame, dump: bool = True
    ):
        db.session.add(visualization)
        db.session.commit()

        visualization_file_path = os.path.join(
            VISUALIZATIONS_UPLOAD_FOLDER, f"vd_{visualization.id}.csv"
        )

        data.to_csv(visualization_file_path, index=False)
        visualization.image_file_path = visualization_file_path

        db.session.commit()
        return self.visualizations_schema.dump(visualization) if dump else visualization

    def delete_visualization(self, id: int, dump: bool = True):
        visualization = self.get_visualization_by_id(id=id, dump=False)

        if not isinstance(visualization, Visualizations):
            return visualization
        if os.path.exists(visualization.image_file_path):
            os.remove(visualization.image_file_path)
        db.session.delete(visualization)
        db.session.commit()
        return self.visualizations_schema.dump(visualization) if dump else visualization


class AnalyzesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=AnalyzesSchema(), model_class=Analyzes)
        self.files_service = FilesService()
        self.visualizations_service = VisualizationsService()

    def create_analyze(self, analyze: Analyzes, id: int, dump: bool = True):
        file = self.files_service.get_file_by_id(id, dump=False)
        if not isinstance(file, Files):
            return file

        mba = MBAnalyze(
            id=file.id,
            file_path=file.file_path,
            support=analyze.support,
            lift=analyze.lift,
            confidence=analyze.confidence,
            rules_length=analyze.rules_length,
        )
        # association_rules = mba.analyze()

        # analyze
        df = pd.read_csv(mba.file_path)
        print("Starting preprocessing...")
        preprocessed_df = mba.preprocess(df[:1000])
        print("DF INFO: ", preprocessed_df.info())
        print("DONE\n")
        print("Starting transforming...")
        df_set = mba.transform(df)
        print("DF SET INFO: ", df_set.info())
        print("DONE\n")
        print("Starting fpgrowth analyze...")
        frequent_itemsets = mba.create_frequent_itemsets(df_set)
        print("DONE\n")
        print("Starting creation of association rules...")
        association_rules = mba.create_association_rules(frequent_itemsets)
        print("DONE\n")

        if association_rules.empty:
            return "No association rules were generated with specified options"

        # visualization
        [transactions_month_ser, transactions_cost_item] = mba.analyze_preprocess_data(
            preprocessed_df
        )
        top_items = mba.analyze_frequent_itemsets(frequent_itemsets)
        top_rules = mba.analyze_association_rules(association_rules)
        visualizations_data = [
            top_items,
            top_rules,
            transactions_month_ser,
            transactions_cost_item,
        ]
        # print(transactions_month_ser.to_json(orient='split'))
        # print(transactions_month_ser.to_json(orient='split'))
        # print(top_items.to_json(orient='split'))
        # print(top_rules.to_json(orient='split'))
        for visualization_data in visualizations_data:
            new_visualization = Visualizations(
                name="Untitled",
                image_file_path="None",
                report_id=analyze.report_id,
            )
            self.visualizations_service.create_visualization(
                new_visualization, visualization_data
            )

        analyze.file_path = "None"
        try:
            db.session.add(analyze)
            db.session.commit()

            file_path = os.path.join(ANALYZES_UPLOAD_FOLDER, f"ar_{analyze.id}.csv")

            association_rules.to_csv(file_path, index=False)
            analyze.file_path = file_path

            db.session.commit()
            # return self.schema.dump(analyze) if dump else analyze
            return association_rules
        except Exception as err:
            print(err)
            return "Failed to create analyze"

    def delete_analyze(self, id: int, dump: bool = True):
        analyze = self.get_analyze_by_id(id=id, dump=False)
        if not isinstance(analyze, Analyzes):
            return None

        try:
            if os.path.exists(analyze.file_path):
                os.remove(analyze.file_path)
            db.session.delete(analyze)
            db.session.commit()
            return self.schema.dump(analyze) if dump else analyze
        except Exception as err:
            print(err)
            return "Failed to delete analyze"
