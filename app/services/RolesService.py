from app.services import GenericService
from app.models import (
    Roles,
    RolesSchema,
)


class RolesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=RolesSchema(), model_class=Roles)
