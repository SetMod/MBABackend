from app.logger import logger
from app.models import Roles, Users
from app.schemas import RolesSchema
from app.services.GenericService import GenericService
from typing import List


class RolesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=RolesSchema(), model_class=Roles)

    def get_all_users(self, id: int) -> List[Users]:
        logger.info(f"Getting {self.model_class._name()} users")

        existing_model: Roles = self.get_by_id(id)
        users: List[Users] = existing_model.users

        logger.info(f"Found {self.model_class._name()} users: {users}")
        return users
