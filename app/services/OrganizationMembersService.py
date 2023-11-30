from typing import List
from app.logger import logger
from app.db import db
from app.models import OrganizationMembers, Users, Organizations, Reports, Datasources
from app.schemas import OrganizationMembersSchema
from app.services import GenericService


class OrganizationMembersService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=OrganizationMembersSchema(), model_class=OrganizationMembers
        )

    def get_user(self, id: int) -> Users:
        logger.info(f"Get {self.model_class._name()} user")

        organization_member: OrganizationMembers = self.get_by_id(id)
        user: Users = organization_member.user

        logger.info(f"Found {self.model_class._name()} user: {user}")

        return user

    def get_organization(self, id: int) -> Organizations:
        logger.info(f"Get {self.model_class._name()} organization")

        organization_member: OrganizationMembers = self.get_by_id(id)
        organization: Organizations = organization_member.organization

        logger.info(f"Found {self.model_class._name()} organization: {organization}")

        return organization

    def get_all_datasources(self, id: int) -> List[Datasources]:
        logger.info(f"Get {self.model_class._name()} datasources")

        report: OrganizationMembers = self.get_by_id(id)
        datasources: List[Datasources] = report.datasources

        logger.info(f"Found {self.model_class._name()} datasources: {datasources}")

        return datasources

    def get_all_reports(self, id: int) -> List[Reports]:
        logger.info(f"Get {self.model_class._name()} reports")

        report: OrganizationMembers = self.get_by_id(id)
        reports: List[Reports] = report.reports

        logger.info(f"Found {self.model_class._name()} reports: {reports}")

        return reports
