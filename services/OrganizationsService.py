from app import db
from marshmallow import ValidationError
from models.FilesModel import FilesSchema
from models.OrganizationRolesModel import OrganizationRoles, OrganizationRolesSchema
from models.OrganizationsModel import Organizations, OrganizationsSchema
from models.ReportsModel import ReportsSchema
from models.UsersModel import Users, UsersSchema
from models.UsersOrganizationsModel import UsersOrganizations
from services.OrganizationRolesService import OrganizationRolesService
from services.UsersService import UsersService


class OrganizationsService():

    def __init__(self) -> None:
        self.users_service = UsersService()
        self.organization_roles_service = OrganizationRolesService()
        self.organizations_schema = OrganizationsSchema()
        self.organization_roles_schema = OrganizationRolesSchema()
        self.users_schema = UsersSchema()
        self.files_schema = FilesSchema()
        self.reports_schema = ReportsSchema()

    def get_all_organizations(self, dump: bool = True):
        try:
            organizations = db.session.query(Organizations).all()

            if len(organizations) > 0:
                return self.organizations_schema.dump(organizations, many=True) if dump else organizations
            else:
                return 'Organizations not found'
        except Exception as err:
            print(err)
            return 'Failed to get organizations'

    def get_organization_by_id(self, organization_id: int, dump: bool = True):
        try:
            organization = db.session.query(Organizations).where(
                Organizations.organization_id == organization_id).first()

            if isinstance(organization, Organizations):
                return self.organizations_schema.dump(organization) if dump else organization
            else:
                return 'Organization not found'
        except Exception as err:
            print(err)
            return 'Failed to get organization'

    def get_user_organizations(self, user_id: int, dump: bool = True):
        try:
            user = self.users_service.get_user_by_id(user_id, dump=False)

            if not isinstance(user, Users):
                return user

            organizations_and_roles = db.session.query(Organizations, OrganizationRoles).select_from(Organizations).join(UsersOrganizations).filter(
                Organizations.organization_id == UsersOrganizations.organization_id, UsersOrganizations.user_id == user_id, OrganizationRoles.organization_role_id == UsersOrganizations.organization_role_id).all()

            def organizations_dump(organization: Organizations, organization_role: OrganizationRoles):
                org = self.organizations_schema.dump(organization)
                org_role = self.organization_roles_schema.dump(
                    organization_role)
                return {**org, **org_role}

            if len(organizations_and_roles) > 0:
                return [organizations_dump(org, org_role)
                        for org, org_role in organizations_and_roles] if dump else organizations_and_roles
            else:
                return 'Organizations not found'
        except Exception as err:
            print(err)
            return 'Failed to get user organizations'

    def get_organization_users(self, organization_id: int, dump: bool = True):
        try:
            organization = self.get_organization_by_id(
                organization_id, dump=False)

            if isinstance(organization, str):
                return organization

            users_and_roles = db.session.query(Users, OrganizationRoles).select_from(Users).join(UsersOrganizations).filter(
                Users.user_id == UsersOrganizations.user_id, UsersOrganizations.organization_id == organization_id, OrganizationRoles.organization_role_id == UsersOrganizations.organization_role_id).all()

            def users_dump(user: Users, organization_role: OrganizationRoles):
                usr = self.users_schema.dump(user)
                org_role = self.organization_roles_schema.dump(
                    organization_role)
                return {**usr, **org_role}

            if len(users_and_roles) > 0:
                return [users_dump(usr, org_role)
                        for usr, org_role in users_and_roles] if dump else users_and_roles
            else:
                return 'Users not found'
        except Exception as err:
            print(err)
            return 'Failed to get organization users'

    def get_organization_reports(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if isinstance(organization, str):
            return organization

        if organization is not None and len(organization.organization_reports) > 0:
            return self.reports_schema.dump(organization.organization_reports, many=True) if dump else organization.organization_reports
        else:
            return 'No organization reports was found'

    def get_organization_files(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if isinstance(organization, str):
            return organization

        if len(organization.organization_files) > 0:
            return self.files_schema.dump(organization.organization_files, many=True) if dump else organization.organization_files
        else:
            return 'No organization files was found'

    def get_organization_by_name(self, organization_name: str, dump: bool = True):
        try:
            organization = db.session.query(Organizations).where(
                Organizations.organization_name == organization_name).first()

            if isinstance(organization, Organizations):
                return self.organizations_schema.dump(organization) if dump else organization
            else:
                return 'Organization not found'
        except Exception as err:
            print(err)
            return 'Failed to get organization'

    def get_organization_by_email(self, email: str, dump: bool = True):
        try:
            organization = db.session.query(Organizations).where(
                Organizations.organization_email == email).first()

            if isinstance(organization, Organizations):
                return self.organizations_schema.dump(organization) if dump else organization
            else:
                return 'Organization not found'
        except Exception as err:
            print(err)
            return 'Failed to get organization'

    def get_organization_by_phone(self, phone: str, dump: bool = True):
        try:
            organization = db.session.query(Organizations).where(
                Organizations.organization_phone == phone).first()

            if isinstance(organization, Organizations):
                return self.organizations_schema.dump(organization) if dump else organization
            else:
                return 'Organization not found'
        except Exception as err:
            print(err)
            return 'Failed to get organization'

    def create_organization(self, new_organization: Organizations, dump: bool = True):
        existing_organization = self.get_organization_by_name(
            new_organization.organization_name, dump=False)
        if isinstance(existing_organization, Organizations):
            return f'Name is already taken'

        existing_organization = self.get_organization_by_email(
            new_organization.organization_email, dump=False)
        if isinstance(existing_organization, Organizations):
            return 'Email is already taken'

        if new_organization.organization_phone:
            existing_organization = self.get_organization_by_phone(
                new_organization.organization_phone, dump=False)
            if isinstance(existing_organization, Organizations):
                return f'Phone is already taken'

        try:
            db.session.add(new_organization)
            db.session.commit()
            return self.organizations_schema.dump(new_organization) if dump else new_organization
        except Exception as err:
            print(err)
            return 'Failed to create new organization'

    def add_user_to_organization(self, user_organization: UsersOrganizations, dump: bool = True):
        user = self.users_service.get_user_by_id(
            user_organization.user_id, dump=False)
        organization = self.get_organization_by_id(
            user_organization.organization_id, dump=False)
        organization_role = self.organization_roles_service.get_organization_role_by_id(
            user_organization.organization_role_id, dump=False)

        if user is None or organization is None or organization_role is None:
            return None

        try:
            # user.user_organizations.append(organization)
            db.session.add(user_organization)
            db.session.commit()
            # added_user_organization = self.users_organizations_service.get_user_organization(
            #     user_organization.user_id, user_organization.organization_id)
            # print(added_user_organization)

            # added_user_organization.organization_role_id = user_organization.organization_role_id
            # db.session.commit()
            return self.organizations_schema.dump(user.user_organizations, many=True) if dump else user.user_organizations
            # return self.users_schema.dump(user) if dump else user
        except Exception as err:
            print(err)
            return None

    def update_organization(self, organization_id: int, updated_organization: Organizations, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if not isinstance(organization, Organizations):
            return organization

        existing_organization = self.get_organization_by_name(
            updated_organization.organization_name, dump=False)
        if isinstance(existing_organization, Organizations):
            return f'Name is already taken'

        existing_organization = self.get_organization_by_email(
            updated_organization.organization_email, dump=False)
        if isinstance(existing_organization, Organizations):
            return 'Email is already taken'

        if updated_organization.organization_phone:
            existing_organization = self.get_organization_by_phone(
                updated_organization.organization_phone, dump=False)
            if isinstance(existing_organization, Organizations):
                return f'Phone is already taken'

        organization.organization_name = updated_organization.organization_name
        organization.organization_description = updated_organization.organization_description
        organization.organization_email = updated_organization.organization_email
        organization.organization_phone = updated_organization.organization_phone
        try:
            db.session.commit()
            return self.organizations_schema.dump(organization) if dump else organization
        except Exception as err:
            print(err)
            return 'Failed to update organization'

    def delete_user_from_organization(self,  user_id: int, organization_id: int, dump: bool = True):
        user = self.users_service.get_user_by_id(user_id, dump=False)
        organization = self.get_organization_by_id(
            organization_id, dump=False)
        user_organization = db.session.query(UsersOrganizations).where(
            UsersOrganizations.user_id == user_id).where(UsersOrganizations.organization_id == organization_id).first()
        if user is None or organization is None:
            return None

        try:
            # user.user_organizations.remove(organization)
            db.session.delete(user_organization)
            db.session.commit()
            return self.organizations_schema.dump(user.user_organizations, many=True) if dump else user.user_organizations
            # return self.users_schema.dump(user) if dump else user
        except Exception as err:
            print(err)
            return None

    def delete_organization(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if not isinstance(organization, Organizations):
            return organization

        try:
            db.session.delete(organization)
            db.session.commit()
            return self.organizations_schema.dump(organization) if dump else organization
        except Exception as err:
            print(err)
            return 'Failed to delete organization'

    def map_organization(self, organization_dict: dict):
        try:
            organization = self.organizations_schema.load(organization_dict)
            organization_name = organization_dict['organization_name']
            organization_description = organization_dict['organization_description']
            organization_email = organization_dict['organization_email']
            organization_phone = organization_dict['organization_phone']
            organization = Organizations(organization_name=organization_name, organization_description=organization_description,
                                         organization_email=organization_email, organization_phone=organization_phone)
            return organization
        except ValidationError as err:
            print(err)
            return err.messages
        except Exception as err:
            print(err)
            return 'Failed to map organization'
