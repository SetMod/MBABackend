from datetime import datetime
from typing import List
from app.db import db
from app.exceptions import CustomBadRequest
from app.logger import logger
from app.models import (
    OrganizationMembers,
    Users,
    Organizations,
    Reports,
    Datasources,
)
from app.schemas import UsersSchema
from app.services.GenericService import GenericService
from app.utils import generate_reset_token, send_reset_email


class UsersService(GenericService):
    reset_tokens = []

    def __init__(self) -> None:
        super().__init__(schema=UsersSchema(), model_class=Users)

    def get_all_organizations(self, id: int) -> List[Organizations]:
        logger.info(f"Getting {self.model_class._name()} organizations")

        user: Users = self.get_by_id(id)
        organizations: List[Organizations] = (
            db.session.execute(
                db.select(Organizations)
                .join(OrganizationMembers)
                .where(
                    OrganizationMembers.user_id == user.id
                    and OrganizationMembers.organization_id == Organizations.id
                )
            )
            .scalars()
            .all()
        )

        logger.info(f"Found {self.model_class._name()} organizations: {organizations}")

        return organizations

    def get_all_reports(self, id: int) -> List[Reports]:
        logger.info(f"Getting {self.model_class._name()} reports")

        user: Users = self.get_by_id(id)
        # reports: List[Reports] = user.reports
        reports: List[Reports] = (
            db.session.execute(
                db.select(Reports)
                .join(OrganizationMembers)
                .where(
                    OrganizationMembers.user_id == user.id
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

        user: Users = self.get_by_id(id)
        # datasources: List[Datasources] = user.datasources
        datasources: List[Datasources] = (
            db.session.execute(
                db.select(Datasources)
                .join(OrganizationMembers)
                .where(
                    OrganizationMembers.user_id == user.id
                    and Datasources.creator_id == OrganizationMembers.id
                )
            )
            .scalars()
            .all()
        )

        logger.info(f"Found {self.model_class._name()} datasources: {datasources}")

        return datasources

    def login(self, username: str, password: str) -> Users:
        logger.info(f"Logging in {self.model_class._name()}")

        existing_user: Users = self.get_by_field("username", username)
        correct_password = existing_user.verify_password(password)

        if not correct_password and existing_user:
            msg = f"{self.model_class._name(lower=False)} password is incorrect"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        existing_user.last_login_date = datetime.utcnow()
        self.commit()

        logger.info("Logged in successfully!")

        return existing_user

    def request_reset(self, username: str, email: str) -> None:
        logger.info(
            f"Requested reset for {self.model_class._name()} with username='{username}'"
        )

        existing_user: Users = self.get_by_fields(
            {"username": username, "email": email}
        )

        token = generate_reset_token()
        self.reset_tokens[username] = token

        send_reset_email(existing_user.email, token)

        logger.info(f"Reset email sent")

    def reset_password(self, username: str, password: str, token: str) -> None:
        logger.info(
            f"Resetting  password for {self.model_class._name()} with username='{username}'"
        )

        if username not in self.reset_tokens or self.reset_tokens[username] != token:
            msg = "Invalid or expired username or token"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        existing_user: Users = self.get_by_field("username", username)

        existing_user.password = password
        self.commit()

        del self.reset_tokens[token]

        logger.info(
            f"Password for {self.model_class._name()} with username='{username}' successfully reset"
        )
