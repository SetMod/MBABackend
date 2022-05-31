from marshmallow import ValidationError
from models.FilesModel import FilesSchema
from models.OrganizationsModel import Organizations, OrganizationsSchema
from app import db
from models.ReportsModel import ReportsSchema
from models.UsersModel import UsersSchema


class OrganizationsService():

    def __init__(self) -> None:
        self.organizations_schema = OrganizationsSchema()
        self.users_schema = UsersSchema()
        self.files_schema = FilesSchema()
        self.reports_schema = ReportsSchema()

    def get_all_organizations(self, dump: bool = True):
        organizations = db.session.query(Organizations).all()

        if len(organizations) > 0:
            return self.organizations_schema.dump(organizations, many=True) if dump else organizations
        else:
            return None

    def get_organization_by_id(self, organization_id: int, dump: bool = True):
        organization = db.session.query(Organizations).where(
            Organizations.organization_id == organization_id).first()

        if isinstance(organization, Organizations):
            return self.organizations_schema.dump(organization) if dump else organization
        else:
            return None

    def get_organization_users(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if organization is not None and len(organization.organization_users) > 0:
            return self.users_schema.dump(organization.organization_users, many=True) if dump else organization.organization_users
        else:
            return None

    def get_organization_files(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if organization is not None and len(organization.organization_files) > 0:
            return self.files_schema.dump(organization.organization_files, many=True) if dump else organization.organization_files
        else:
            return None

    def get_organization_reports(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        if organization is not None and len(organization.organization_reports) > 0:
            return self.reports_schema.dump(organization.organization_reports, many=True) if dump else organization.organization_reports
        else:
            return None

    # def get_users_by_organization_roles(self, role_name: str):
    #     role = self.roles_service.get_role_by_name(role_name)
    #     return self.users_schema.dump(role.users, many=True)

    def create_organization(self, organization: Organizations, dump: bool = True):
        try:
            db.session.add(organization)
            db.session.commit()
            return self.organizations_schema.dump(organization) if dump else organization
        except Exception:
            return None

    def update_organization(self, organization_id: int, updated_organization: Organizations, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        try:
            if isinstance(organization, Organizations):
                organization.organization_name = updated_organization.organization_name
                organization.organization_description = updated_organization.organization_description
                organization.organization_email = updated_organization.organization_email
                organization.organization_phone = updated_organization.organization_phone
                db.session.commit()
                return self.organizations_schema.dump(organization) if dump else organization
            else:
                return None
        except Exception:
            return None

    def delete_organization(self, organization_id: int, dump: bool = True):
        organization = self.get_organization_by_id(organization_id, dump=False)

        try:
            if isinstance(organization, Organizations):
                db.session.delete(organization)
                db.session.commit()
                return self.organizations_schema.dump(organization) if dump else organization
            else:
                return None
        except Exception:
            return None

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
            return err.messages
