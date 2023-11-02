from marshmallow import ValidationError
from models.OrganizationRolesModel import OrganizationRoles, OrganizationRolesSchema
from app import db


class OrganizationRolesService:

    def __init__(self) -> None:
        self.organization_roles_schema = OrganizationRolesSchema()

    def get_all_organization_roles(self, dump: bool = True):
        organization_roles = db.session.query(OrganizationRoles).all()

        if len(organization_roles) > 0:
            return self.organization_roles_schema.dump(organization_roles, many=True) if dump else organization_roles
        else:
            return None

    def get_organization_role_by_id(self, organization_role_id: int, dump: bool = True):
        organization_role = db.session.query(OrganizationRoles).where(
            OrganizationRoles.organization_role_id == organization_role_id).first()

        if isinstance(organization_role, OrganizationRoles):
            return self.organization_roles_schema.dump(organization_role) if dump else organization_role
        else:
            return None

    def get_organization_role_by_name(self, name: str, dump: bool = True) -> OrganizationRoles:
        organization_role = db.session.query(OrganizationRoles).where(
            OrganizationRoles.organization_role_name == name).first()

        if isinstance(organization_role, OrganizationRoles):
            return self.organization_roles_schema.dump(organization_role) if dump else organization_role
        else:
            return None

    def create_organization_role(self, organization_role, dump: bool = True):
        try:
            db.session.add(organization_role)
            db.session.commit()
            return self.organization_roles_schema.dump(organization_role) if dump else organization_role
        except Exception:
            return None

    def update_organization_role(self, organization_role_id, updated_organization_role: OrganizationRoles, dump: bool = True):
        organization_role = self.get_organization_role_by_id(
            organization_role_id, dump=False)

        try:
            if type(organization_role) is OrganizationRoles:
                organization_role.organization_role_name = updated_organization_role.organization_role_name
                organization_role.organization_role_description = updated_organization_role.organization_role_description
                db.session.commit()
                return self.organization_roles_schema.dump(organization_role) if dump else organization_role
            else:
                return None
        except Exception:
            return None

    def delete_organization_role(self, organization_role_id: int, dump: bool = True):
        organization_role = self.get_organization_role_by_id(
            organization_role_id, dump=False)

        try:
            if type(organization_role) is OrganizationRoles:
                db.session.delete(organization_role)
                db.session.commit()
                return self.organization_roles_schema.dump(organization_role) if dump else organization_role
            else:
                return None
        except Exception:
            return None

    def map_organization_role(self, organization_role_dict: dict):
        try:
            organization_role = self.organization_roles_schema.load(
                organization_role_dict)
            organization_role_name = organization_role_dict['organization_role_name']
            organization_role_description = organization_role_dict['organization_role_description']
            organization_role = OrganizationRoles(
                organization_role_name=organization_role_name, organization_role_description=organization_role_description)
            return organization_role
        except ValidationError:
            return None
