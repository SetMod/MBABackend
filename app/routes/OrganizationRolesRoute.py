from flask import Blueprint
from app.routes.GenericRoute import GenericRoute
from app.services import OrganizationRolesService


class OrganizationRolesRoute(GenericRoute):
    bp = Blueprint(name="organization_roles", import_name=__name__)
    organization_roles_svc = OrganizationRolesService()

    def __init__(self) -> None:
        super().__init__(self.bp, self.organization_roles_svc)
        super().register_routes()
