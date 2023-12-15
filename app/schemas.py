from app.db import ma
from marshmallow import ValidationError, fields, validates_schema
from marshmallow_sqlalchemy import auto_field
from marshmallow_oneofschema import OneOfSchema
from app.models import (
    AnalyzeStatus,
    DatasourceTypes,
    OrganizationMembers,
    OrganizationRoles,
    Organizations,
    ReportTypes,
    Roles,
    Users,
    Reports,
    Datasources,
    FileDatasources,
    VisualizationTypes,
    Visualizations,
    DataVisualizations,
    FileVisualizations,
    Analyzes,
    Algorithm,
)
from app.utils import password_check


class UsersSchema(ma.SQLAlchemyAutoSchema):
    role = fields.Enum(Roles)
    password_hash = fields.String(required=False)
    password = fields.String(required=False, load_only=True, validate=password_check)

    class Meta:
        model = Users
        include_fk = True
        # load_only = ["password_hash"]
        # dump_only = ["password_hash"]

    @validates_schema
    def validate_password_fields(self, data, **kwargs):
        password = data.get("password")
        password_hash = data.get("password_hash")

        # if password and password_hash:
        #     raise ValidationError("Both password and password_hash cannot be present simultaneously")

        if not password and not password_hash:
            raise ValidationError("Missing 'password' required field")
            # raise ValidationError("Either 'password' or 'password_hash' field is required")


class OrganizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organizations


class OrganizationMembersSchema(ma.SQLAlchemyAutoSchema):
    role = fields.Enum(OrganizationRoles)

    class Meta:
        model = OrganizationMembers
        include_fk = True


class OrganizationMembersFullSchema(OrganizationMembersSchema):
    # user = auto_field(many=True)
    # user = fields.Nested(UsersSchema, many=True)

    # user = auto_field()
    # organization = auto_field()

    user = fields.Nested(UsersSchema)
    organization = fields.Nested(OrganizationsSchema)


class DatasourcesSchema(ma.SQLAlchemyAutoSchema):
    type = fields.Enum(DatasourceTypes)

    class Meta:
        model = Datasources
        include_fk = True


class DatasourcesFullSchema(DatasourcesSchema):
    creator = fields.Nested(OrganizationMembersFullSchema)


class FileDatasourcesSchema(DatasourcesSchema):
    class Meta:
        model = FileDatasources
        include_fk = True
        load_instance = True


class FileDatasourcesFullSchema(FileDatasourcesSchema):
    creator = fields.Nested(OrganizationMembersFullSchema)


class DatasourcesTypeSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {DatasourceTypes.FILE.name: FileDatasourcesSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, FileDatasources):
            return DatasourceTypes.FILE.name
        else:
            raise ValueError(f"Unknown object type: {obj.__class__}")


class DatasourcesTypeFullSchema(DatasourcesTypeSchema):
    type_schemas = {DatasourceTypes.FILE.name: FileDatasourcesFullSchema}


class AnalyzesSchema(ma.SQLAlchemyAutoSchema):
    status = fields.Enum(AnalyzeStatus)
    algorithm = fields.Enum(Algorithm)

    class Meta:
        model = Analyzes
        include_fk = True


class AnalyzesFullSchema(AnalyzesSchema):
    creator = fields.Nested(OrganizationMembersFullSchema)
    datasource = fields.Nested(DatasourcesTypeFullSchema)


class ReportsSchema(ma.SQLAlchemyAutoSchema):
    type = fields.Enum(ReportTypes)

    class Meta:
        model = Reports
        include_fk = True


class ReportsFullSchema(ReportsSchema):
    creator = fields.Nested(OrganizationMembersFullSchema)


class VisualizationsSchema(ma.SQLAlchemyAutoSchema):
    type = fields.Enum(VisualizationTypes)

    class Meta:
        model = Visualizations
        include_fk = True


class DataVisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DataVisualizations
        include_fk = True


class FileVisualizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FileVisualizations
        include_fk = True
