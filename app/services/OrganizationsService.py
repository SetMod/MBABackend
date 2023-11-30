from typing import List
from app.exceptions import CustomBadRequest, CustomNotFound
from app.logger import logger
from app.db import db
from app.models import (
    Datasources,
    OrganizationMembers,
    Organizations,
    Reports,
    Users,
)
from app.schemas import OrganizationsSchema
from app.services import GenericService, GenericService


class OrganizationsService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=OrganizationsSchema(), model_class=Organizations)

    def get_all_members(self, id: int) -> List[OrganizationMembers]:
        logger.info(f"Getting {self.model_class._name()} members")

        organization: Organizations = self.get_by_id(id)
        # members: List[Users] = organization.members
        members: List[OrganizationMembers] = (
            db.session.execute(
                db.select(OrganizationMembers).where(
                    OrganizationMembers.organization_id == organization.id
                )
            )
            .scalars()
            .all()
        )

        logger.info(f"Found {self.model_class._name()} members: {members}")

        return members

    def get_all_reports(self, id: int) -> List[Reports]:
        logger.info(f"Getting {self.model_class._name()} reports")

        organization: Organizations = self.get_by_id(id)
        # reports: List[Reports] = organization.reports
        reports: List[Reports] = (
            db.session.execute(
                db.select(Reports)
                .join(OrganizationMembers)
                .where(
                    OrganizationMembers.organization_id == organization.id
                    and Reports.creator_id == OrganizationMembers.id
                )
            )
            .scalars()
            .all()
        )

        logger.info(f"Found {self.model_class._name()} reports: {reports}")

        return reports

    def get_all_datasources(self, id: int) -> List[Datasources]:
        logger.info(f"Getting {self.model_class._name()} datasources")

        organization: Organizations = self.get_by_id(id)
        # datasources: List[Datasources] = user.datasources
        datasources: List[Datasources] = (
            db.session.execute(
                db.select(Datasources)
                .join(OrganizationMembers)
                .where(
                    OrganizationMembers.organization_id == organization.id
                    and Datasources.creator_id == OrganizationMembers.id
                )
            )
            .scalars()
            .all()
        )

        logger.info(f"Found {self.model_class._name()} datasources: {datasources}")

        return datasources
