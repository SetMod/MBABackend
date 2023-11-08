from app.models import OrganizationRoles, OrganizationRolesSchema
from app.services import GenericService


class OrganizationRolesService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=OrganizationRolesSchema(), model_class=OrganizationRoles
        )
