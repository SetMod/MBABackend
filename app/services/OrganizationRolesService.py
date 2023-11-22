from app.models import OrganizationRoles
from app.schemas import OrganizationRolesSchema
from app.services.GenericService import GenericService


class OrganizationRolesService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=OrganizationRolesSchema(), model_class=OrganizationRoles
        )
