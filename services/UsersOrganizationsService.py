from marshmallow import ValidationError
from models.OrganizationRolesModel import OrganizationRolesSchema
from models.UsersOrganizationsModel import UsersOrganizations, UsersOrganizationsSchema
from services.OrganizationRolesService import OrganizationRolesService
from sqlalchemy.engine.row import Row
from app import db


class UsersOrganizationsService:
    def __init__(self) -> None:
        self.users_organizations_schema = UsersOrganizationsSchema()
        self.organization_roles_schema = OrganizationRolesSchema()
        self.organization_roles_service = OrganizationRolesService()
        # self.users_schema = UsersSchema()
        # self.organizations_schema = OrganizationsSchema()

    def get_all_users_organizations(self, dump: bool = True):
        # users_organizations = db.session.query(users_organizations_table).all()
        users_organizations = db.session.query(UsersOrganizations).all()

        if len(users_organizations) == 0:
            return None
        else:
            return self.users_organizations_schema.dump(users_organizations, many=True) if dump else users_organizations

    def get_user_organization(self, user_id: int, organization_id: bool, dump: bool = True):
        # user_organization = db.session.query(users_organizations_table).where(
        #     users_organizations_table.c.user_id == user_id, users_organizations_table.c.organization_id == organization_id).first()
        user_organization = db.session.query(UsersOrganizations).where(
            UsersOrganizations.user_id == user_id, UsersOrganizations.organization_id == organization_id).first()

        if isinstance(user_organization, Row):
            return self.users_organizations_schema.dump(user_organization) if dump else user_organization
        else:
            return None

    def get_user_organization_role(self, user_id: int, organization_id: bool, dump: bool = True):
        user_organization = self.get_user_organization(
            user_id, organization_id)

        if user_organization is None:
            return None

        organization_role = self.organization_roles_service.get_organization_role_by_id(
            user_organization['organization_role_id'], dump=False)

        if organization_role is None:
            return None

        return self.organization_roles_schema.dump(organization_role) if dump else organization_role

    # def add_user_to_organizations(self, user_organizations: UsersOrganizations, dump: bool = True):
    #     try:
    #         query = users_organizations_table.insert().values(user_id=user_organizations.user_id,
    #                                                           organizations_id=user_organizations.organization_id, organization_role_id=user_organizations.organization_role_id)
    #         db.engine.execute(query)
    #         db.session.commit()
    #         return self.users_organizations_schema.dump(user_organizations, many=True) if dump else user_organizations
    #     except Exception:
    #         return None

    def map_users_organizations(self, users_organizations_dict: dict):
        try:
            users_organizations = self.users_organizations_schema.load(
                users_organizations_dict)
            user_id = users_organizations_dict['user_id']
            organization_id = users_organizations_dict['organization_id']
            organization_role_id = users_organizations_dict['organization_role_id']
            users_organizations = UsersOrganizations(
                user_id, organization_id, organization_role_id)
            return users_organizations
        except ValidationError as err:
            return err.messages
