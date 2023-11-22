from app.db import ma
from app.models import (
    OrganizationRoles,
    Roles,
    Organizations,
    Users,
    Reports,
    Datasources,
    FileDatasources,
    Visualizations,
    DataVisualizations,
    FileVisualizations,
    Analyzes,
)


class OrganizationRolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrganizationRoles


class RolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Roles


class OrganizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organizations


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True

    # role = ma.Nested(RolesSchema)
    # user_role = ma.HyperlinkRelated('roles.get_role_by_id', 'role_id')
    # role_id = ma.auto_field()


class ReportsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reports

    user_id = ma.auto_field()
    organization_id = ma.auto_field()


class DatasourcesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Datasources

    user_id = ma.auto_field()
    organization_id = ma.auto_field()


class FileDatasourcesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FileDatasources

    datasource_id = ma.auto_field()


class VisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Visualizations
        include_fk = True


class DataVisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DataVisualizations
        include_fk = True

    visualization_id = ma.auto_field()


class FileVisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FileVisualizations
        include_fk = True

    visualization_id = ma.auto_field()


class AnalyzesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Analyzes
        include_fk = True

    report_id = ma.auto_field()
