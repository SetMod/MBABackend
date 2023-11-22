from typing import List
from sqlalchemy import Table
from app.exceptions import CustomBadRequest, CustomNotFound
from app.logger import logger
from app.db import db
from app.models import (
    Datasources,
    OrganizationRoles,
    Organizations,
    Reports,
    Users,
    organization_members,
)
from app.schemas import OrganizationsSchema
from app.services.GenericService import GenericService
from app.services.OrganizationRolesService import OrganizationRolesService
from app.services.UsersService import UsersService


class OrganizationsService(GenericService):
    users_service = UsersService()
    organization_roles_service = OrganizationRolesService()

    def __init__(self) -> None:
        super().__init__(schema=OrganizationsSchema(), model_class=Organizations)

    def get_all_reports(self, id: int) -> List[Reports]:
        logger.info(f"Getting {self.model_class._name()} reports")

        organization: Organizations = self.get_by_id(id)
        reports: List[Reports] = organization.reports

        logger.info(f"Found {self.model_class._name()} reports: {reports}")

        return reports

    def get_all_datasources(self, id: int) -> List[Datasources]:
        logger.info(f"Getting {self.model_class._name()} datasources")

        organization: Organizations = self.get_by_id(id)
        datasources: List[Datasources] = organization.datasources

        logger.info(f"Found {self.model_class._name()} datasources: {datasources}")

        return datasources

    def get_all_members(self, id: int) -> List[Users]:
        logger.info(f"Getting {self.model_class._name()} members")

        organization: Organizations = self.get_by_id(id)
        members: List[Users] = organization.members

        logger.info(f"Found {self.model_class._name()} members: {members}")

        return members
        # organization = self.get_by_id(id, dump=False)

        # if isinstance(organization, str):
        #     return organization

        # users_and_roles = (
        #     db.session.query(Users, OrganizationRoles)
        #     .select_from(Users)
        #     .join(OrganizationMembers)
        #     .filter(
        #         Users.id == OrganizationMembers.user_id,
        #         OrganizationMembers.organization_id == id,
        #         OrganizationRoles.id == OrganizationMembers.organization_role_id,
        #     )
        #     .all()
        # )

        # return self.__users_dump(users_and_roles) if dump else users_and_roles

    # def __users_dump(self, users_and_roles: List[Row[Tuple[Users, OrganizationRoles]]]):
    #     result = []
    #     for usr, org_role in users_and_roles:
    #         user = self.users_schema.dump(usr)
    #         organization_role = self.organization_roles_schema.dump(org_role)
    #         result.append({**user, **organization_role})
    #     return result

    # def __organizations_dump(
    #     self,
    #     organizations_and_roles: List[Row[Tuple[Organizations, OrganizationRoles]]],
    # ):
    #     result = []
    #     for org, org_role in organizations_and_roles:
    #         organization = self.schema.dump(org)
    #         organization_role = self.organization_roles_schema.dump(org_role)
    #         result.append({**organization, **organization_role})
    #     return result

    def get_organization_member(
        self, organization_id: int, user_id: int, must_exist: bool = True
    ) -> Table:
        logger.info(f"Getting {self.model_class._name()} member")

        organization: Organizations = self.get_by_id(organization_id)
        organization_member = db.session.execute(
            db.select(organization_members).where(
                organization_members.c.organization_id == organization.id
                and organization_members.c.user_id == user_id
            )
        ).scalar_one_or_none()

        if must_exist and not organization_member:
            msg = f"{self.model_class._name(lower=False)} member with id='{user_id}' not found"
            logger.warning(msg)
            raise CustomNotFound(msg)
        elif not must_exist and organization_member:
            msg = f"{self.model_class._name(lower=False)} member with id='{user_id}' already exists"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        logger.info(
            f"Found {self.model_class._name()} organization member: {organization_member}"
        )

        return organization_member

    def get_member_by_id(self, id: int, user_id: int) -> Users:
        logger.info(f"Getting {self.model_class._name()} member where id='{id}'")

        organization_member = self.get_organization_member(id, user_id)
        user: Users = self.users_service.get_by_id(organization_member.c.user_id)

        return user
        # if not isinstance(user, Users):
        #     return user

        # organizations_and_roles = (
        #     db.session.query(Organizations, OrganizationRoles)
        #     .select_from(Organizations)
        #     .join(OrganizationMembers)
        #     .filter(
        #         Organizations.id == OrganizationMembers.organization_id,
        #         OrganizationMembers.user_id == user_id,
        #         OrganizationRoles.id == OrganizationMembers.organization_role_id,
        #     )
        #     .all()
        # )

        # return (
        #     self.__organizations_dump(organizations_and_roles)
        #     if dump
        #     else organizations_and_roles
        # )

    def get_member_organization_role_by_id(
        self, id: int, user_id: int
    ) -> OrganizationRoles:
        logger.info(f"Getting {self.model_class._name()} member role")

        organization_member = self.get_organization_member(id, user_id)
        organization_role: OrganizationRoles = (
            self.organization_roles_service.get_by_id(
                organization_member.c.organization_role_id
            )
        )

        return organization_role

    def add_member(self, id: int, user_id: int, organization_role_id: int) -> Users:
        logger.info(f"Adding {self.model_class._name()} member")

        self.get_organization_member(id, user_id, must_exist=False)
        user: Users = self.users_service.get_by_id(user_id)
        organization_role: OrganizationRoles = (
            self.organization_roles_service.get_by_id(organization_role_id)
        )

        db.session.execute(
            organization_members.insert().values(
                organization_id=id,
                user_id=user.id,
                organization_role_id=organization_role.id,
            )
        )
        self.commit()

        logger.info(
            f"Successfully added to {self._name()} new member with user_id='{user_id}' and organization_role_id='{organization_role_id}'"
        )

        return user
        # organization_role = self.organization_roles_service.get_by_id(
        #     id=new_organization_member.organization_role_id, dump=False
        # )
        # if not isinstance(organization_role, OrganizationRoles):
        #     return None

        # organization_member = self.organization_members_service.get_organization_member(
        #     user_id=new_organization_member.user_id,
        #     organization_id=new_organization_member.organization_id,
        #     dump=False,
        # )
        # if isinstance(organization_member, OrganizationMembers):
        #     return None

        # db.session.add(new_organization_member)
        # db.session.commit()

        # return (
        #     self.organization_members_schema.dump(new_organization_member, many=True)
        #     if dump
        #     else new_organization_member
        # )

    # def update_member(self, user_id: int):
    #     member = self.get_member_by_id(user_id)
    #     user = Users.get_by_id(user_id)
    #     self.members.remove(user)
    #     db.session.commit()

    def remove_member(self, id: int, user_id: int):
        organization_member = self.get_member_by_id(id, user_id)
        organization: Organizations = self.get_by_id(id)
        user = self.users_service.get_by_id(organization_member.c.user_id)

        organization.members.remove(user)
        self.commit()

        logger.info(
            f"Successfully removed {self._name()} member with user_id='{user_id}'"
        )

        return user
        # organization_member = self.organization_members_service.get_organization_member(
        #     user_id=user_id,
        #     organization_id=organization_id,
        #     dump=False,
        # )
        # if not isinstance(organization_member, OrganizationMembers):
        #     return None

        # db.session.delete(organization_member)
        # db.session.commit()
        # return (
        #     self.organization_members_schema.dump(organization_member, many=True)
        #     if dump
        #     else organization_member
        # )
