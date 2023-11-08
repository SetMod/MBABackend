from app.models import (
    FilesSchema,
    OrganizationsSchema,
    ReportsSchema,
    RolesSchema,
    Users,
    UsersSchema,
)
from app.services import (
    OrganizationRolesService,
    UsersOrganizationsService,
    GenericService,
    RolesService,
)
from app.init import db


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

    def get_user_role(self, id: int, dump: bool = True):
        user = self.get_by_id(id, dump=False)

        if not isinstance(user, Users):
            return None

        return self.roles_schema.dump(user.user_role) if dump else user.user_role

    def get_user_by_credentials(self, username: str, password: str, dump: bool = True):
        user = (
            db.session.query(Users)
            .where(
                Users.username == username,
                Users.password == password,
            )
            .first()
        )

        if not user:
            return None

        return self.users_schema.dump(user) if dump else user

    def get_users_by_role(self, name: str, dump: bool = True):
        role = self.roles_service.get_by_field(
            field_name="name",
            field_value=name,
            dump=False,
        )

        if not isinstance(role, self.roles_service.model_class):
            return None

        # Add pagination
        return (
            self.users_schema.dump(role.role_users, many=True)
            if dump
            else role.role_users
        )

    def get_user_organizations(self, id: int, dump: bool = True):
        user = self.get_by_id(id, dump=False)

        if not isinstance(user, Users):
            return None

        # Add pagination
        return (
            self.organizations_schema.dump(user.user_organizations, many=True)
            if dump
            else user.user_organizations
        )

    def get_user_reports(self, id: int, dump: bool = True):
        user = self.get_by_id(id, dump=False)

        if not isinstance(user, Users):
            return None

        # Add pagination
        return (
            self.reports_schema.dump(user.user_reports, many=True)
            if dump
            else user.user_reports
        )

    def get_user_files(self, id: int, dump: bool = True):
        user = self.get_by_id(id, dump=False)

        if not isinstance(user, Users):
            return None

        # Add pagination
        return (
            self.files_schema.dump(user.user_files, many=True)
            if dump
            else user.user_files
        )
