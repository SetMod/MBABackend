from typing import List
from app.exceptions import CustomBadRequest
from app.logger import logger
from app.models import (
    Roles,
    Users,
    Organizations,
    Reports,
    Datasources,
)
from app.schemas import UsersSchema
from app.services.GenericService import GenericService


class UsersService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=UsersSchema(), model_class=Users)

    def get_role(self, id: int) -> Roles:
        logger.info(f"Getting {self.model_class._name()} role")

        user: Users = self.get_by_id(id)
        role: Roles = user.role

        logger.info(f"Found {self.model_class._name()} role: {role}")

        return role

    def get_all_organizations(self, id: int) -> List[Organizations]:
        logger.info(f"Getting {self.model_class._name()} organizations")

        user: Users = self.get_by_id(id)
        organizations: List[Organizations] = user.organizations

        logger.info(f"Found {self.model_class._name()} organizations: {organizations}")

        return organizations

    def get_all_reports(self, id: int) -> List[Reports]:
        logger.info(f"Getting {self.model_class._name()} reports")

        user: Users = self.get_by_id(id)
        reports: List[Reports] = user.reports

        logger.info(f"Found {self.model_class._name()} reports: {reports}")

        return reports

    def get_all_datasources(self, id: int) -> List[Datasources]:
        logger.info(f"Getting {self.model_class._name()} datasources")

        user: Users = self.get_by_id(id)
        datasources: List[Datasources] = user.datasources

        logger.info(f"Found {self.model_class._name()} datasources: {datasources}")

        return datasources

    def login(self, username: str, password: str) -> Users:
        logger.info(f"Logging in {self.model_class._name()}")

        existing_model: Users = self.get_by_field("username", username)
        correct_password = existing_model.verify_password(password)

        if not correct_password and existing_model:
            msg = f"{self.model_class._name(lower=False)} password is incorrect"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        return existing_model
