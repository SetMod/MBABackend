from datetime import datetime
from typing import List
from app.exceptions import CustomBadRequest, CustomNotFound
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

    def create(self, new_model_dict: dict) -> OrganizationMembers:
        logger.info(f"Creating new {self.model_class._name()}")

        self.get_by_unique_fields(new_model_dict, must_exist=False)
        new_model: OrganizationMembers = self.map_model(new_model_dict)
        user = db.session.execute(
            db.select(Users).where(Users.id == new_model.user_id)
        ).scalar_one_or_none()
        org = db.session.execute(
            db.select(Organizations).where(
                Organizations.id == new_model.organization_id
            )
        ).scalar_one_or_none()

        if not user or not org:
            msg = f"{self.model_class._name(lower=False)} with user_id='{new_model.user_id}' and organization_id='{new_model.organization_id}' not found"
            logger.warning(msg)
            raise CustomNotFound(msg)

        db.session.add(new_model)
        self.commit()

        logger.info(
            f"Successfully created new {new_model._name()} with id='{new_model.id}'"
        )

        return new_model

    def update(self, id: int, updated_model_dict: dict) -> OrganizationMembers:
        logger.info(f"Updating {self.model_class._name()} with id='{id}'")

        existing_model: OrganizationMembers = self.get_by_id(id)
        # self.get_by_unique_fields(updated_model_dict, must_exist=False)

        existing_model_dict = self.to_json(existing_model)
        for field in existing_model_dict.keys():
            if field in updated_model_dict:
                existing_model_dict[field] = updated_model_dict[field]

        updated_model: OrganizationMembers = self.map_model(existing_model_dict)
        user = db.session.execute(
            db.select(Users).where(Users.id == updated_model.user_id)
        ).scalar_one_or_none()
        org = db.session.execute(
            db.select(Organizations).where(
                Organizations.id == updated_model.organization_id
            )
        ).scalar_one_or_none()

        if not user or not org:
            msg = f"{self.model_class._name(lower=False)} with user_id='{updated_model.user_id}' and organization_id='{updated_model.organization_id}' not found"
            logger.warning(msg)
            raise CustomNotFound(msg)

        for field in existing_model_dict:
            value = getattr(updated_model, field)
            setattr(existing_model, field, value)

        existing_model.updated_date = datetime.utcnow()
        self.commit()

        logger.info(
            f"Successfully updated {existing_model._name()} with id='{existing_model.id}'"
        )

        return existing_model

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
