from app.models import (
    UsersOrganizationsSchema,
    OrganizationRolesSchema,
    UsersOrganizations,
)
from app.services import GenericService, OrganizationRolesService
from app.init import db


class UsersOrganizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=UsersOrganizationsSchema(), model_class=UsersOrganizations
        )
        self.organization_roles_schema = OrganizationRolesSchema()
        self.organization_roles_service = OrganizationRolesService()

    def get_user_organization(
        self, user_id: int, organization_id: bool, dump: bool = True
    ):
        user_organization = (
            db.session.query(UsersOrganizations)
            .where(
                UsersOrganizations.user_id == user_id,
                UsersOrganizations.organization_id == organization_id,
            )
            .first()
        )

        if not user_organization:
            return None

        return self.schema.dump(user_organization) if dump else user_organization

    def get_user_organization_role(
        self, user_id: int, organization_id: bool, dump: bool = True
    ):
        user_organization = self.get_user_organization(
            user_id, organization_id, dump=False
        )

        if not user_organization:
            return None

        organization_role = self.organization_roles_service.get_organization_role_by_id(
            user_organization.organization_role_id, dump=dump
        )

        return organization_role
