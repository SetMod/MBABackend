from datetime import datetime
from typing import List
import pytest
from app.exceptions import CustomBadRequest, CustomNotFound
from app.models import (
    Datasources,
    OrganizationMembers,
    OrganizationRoles,
    Organizations,
    Reports,
    Roles,
    Users,
)
from app.services import OrganizationMembersService, OrganizationsService, UsersService


class TestUsersService:
    def test_get_all(self, users_service: UsersService):
        users: List[Users] = users_service.get_all()

        assert isinstance(users, list)
        assert len(users) > 1

        users_list = users_service.to_json(users)
        user_dict = users_list[0]

        assert isinstance(user_dict, dict)
        assert "id" in user_dict
        assert "first_name" in user_dict
        assert "second_name" in user_dict
        assert "username" in user_dict
        assert "email" in user_dict
        assert "phone" in user_dict
        assert "role" in user_dict
        assert "active" in user_dict
        assert "updated_date" in user_dict
        assert "created_date" in user_dict
        assert "deleted_date" in user_dict
        assert "soft_deleted" in user_dict

    def test_get_by_id(self, users_service: UsersService):
        user = users_service.get_by_id(1)

        assert isinstance(user, Users)

        user_dict = users_service.to_json(user)

        assert isinstance(user_dict, dict)
        assert "id" in user_dict
        assert "first_name" in user_dict
        assert "second_name" in user_dict
        assert "username" in user_dict
        assert "password_hash" in user_dict

    def test_get_by_non_existing_id(self, users_service: UsersService):
        with pytest.raises(CustomNotFound):
            user = users_service.get_by_id(10)

    def test_get_by_field(self, users_service: UsersService):
        user = users_service.get_by_field("username", "johndoe")

        assert isinstance(user, Users)

        user_dict = users_service.to_json(user)

        assert isinstance(user_dict, dict)
        assert "id" in user_dict
        assert user_dict["username"] == "johndoe"

    def test_get_by_non_existing_field(self, users_service: UsersService):
        with pytest.raises(CustomBadRequest):
            user = users_service.get_by_field("names", "Admin")

    def test_get_by_non_existing_field_value(self, users_service: UsersService):
        with pytest.raises(CustomNotFound):
            user = users_service.get_by_field("username", "asdfasdfasdf")

    def test_get_by_fields(self, users_service: UsersService):
        users: List[Users] = users_service.get_by_fields(
            {"soft_deleted": False}, many=True
        )
        users_list = users_service.to_json(users)

        assert isinstance(users_list, list)
        assert isinstance(users_list[0], dict)
        assert "id" in users_list[0]
        assert "username" in users_list[0]
        assert users_list[0]["soft_deleted"] == False

    def test_get_all_organizations(self, users_service: UsersService):
        organizations: List[Organizations] = users_service.get_all_organizations(1)

        assert isinstance(organizations, list)
        assert len(organizations) == 1

    def test_get_all_reports(self, users_service: UsersService):
        reports: List[Reports] = users_service.get_all_reports(1)

        assert isinstance(reports, list)
        assert len(reports) >= 1

    def test_get_all_datasources(self, users_service: UsersService):
        datasources: List[Datasources] = users_service.get_all_datasources(1)

        assert isinstance(datasources, list)
        assert len(datasources) >= 1

    def test_create(self, users_service: UsersService):
        user = {
            "first_name": "Bob",
            "second_name": "Ross",
            "username": "bobross",
            "active": True,
            "email": "bob.ross@gmail.com",
            "phone": "+123789123978",
            "password": "jkZJK#@kn1x23",
            "role": Roles.USER.name,
        }
        new_user: Users = users_service.create(user)

        assert isinstance(new_user, Users)
        assert new_user.id == 3
        assert new_user.first_name == "Bob"
        assert new_user.second_name == "Ross"
        assert new_user.username == "bobross"
        assert new_user.active == True
        assert new_user.role == Roles.USER

    def test_map_model(self, users_service: UsersService):
        user = {
            "first_name": "Bob",
            "second_name": "Ross",
            "username": "bobross",
            "active": True,
            "email": "bob.ross@gmail.com",
            "phone": "+123789123978",
            "password": "jkF123jkl#z",
            "role": Roles.ADMIN.name,
        }
        user = users_service.map_model(user)

        assert isinstance(user, Users)
        assert user.first_name == "Bob"
        assert user.second_name == "Ross"

    def test_create_existing_user(self, users_service: UsersService):
        user = {
            "first_name": "Bob",
            "second_name": "Ross",
            "username": "bobross",
            "active": True,
            "email": "bob.ross@gmail.com",
            "phone": "+123789123978",
            "password": "jkZJK#@kn1x23",
            "role": Roles.ADMIN.name,
        }
        with pytest.raises(CustomBadRequest):
            new_user: Users = users_service.create(user)

    def test_update(self, users_service: UsersService):
        updated_user_dict = {"username": "bob_ross"}
        updated_user: Users = users_service.update(3, updated_user_dict)

        assert isinstance(updated_user, Users)
        assert updated_user.id == 3
        assert updated_user.username == "bob_ross"

    def test_update_existing_user(self, users_service: UsersService):
        updated_user_dict = {"username": "bob_ross"}

        with pytest.raises(CustomBadRequest):
            user: Users = users_service.update(3, updated_user_dict)

    def test_soft_delete(self, users_service: UsersService):
        user: Users = users_service.soft_delete(3)

        assert user.id == 3
        assert user.username == "bob_ross"
        assert user.soft_deleted == True
        assert isinstance(user.deleted_date, datetime)

    def test_delete(self, users_service: UsersService):
        user: Users = users_service.delete(3)

        assert user.id == 3
        assert user.username == "bob_ross"

        with pytest.raises(CustomNotFound):
            user = users_service.get_by_id(4)


class TestOrganizationsService:
    def test_get_all(self, organizations_service: OrganizationsService):
        organizations: List[Organizations] = organizations_service.get_all()

        assert isinstance(organizations, list)
        assert len(organizations) == 2

        organizations_list = organizations_service.to_json(organizations)
        organization_dict = organizations_list[0]

        assert isinstance(organization_dict, dict)
        assert "id" in organization_dict
        assert "name" in organization_dict
        assert "description" in organization_dict
        assert "email" in organization_dict
        assert "phone" in organization_dict
        assert "updated_date" in organization_dict
        assert "created_date" in organization_dict
        assert "deleted_date" in organization_dict
        assert "soft_deleted" in organization_dict

    def test_get_by_id(self, organizations_service: OrganizationsService):
        organization = organizations_service.get_by_id(1)

        assert isinstance(organization, Organizations)

        organization_dict = organizations_service.to_json(organization)

        assert isinstance(organization_dict, dict)
        assert "id" in organization_dict
        assert "name" in organization_dict

    def test_get_by_non_existing_id(self, organizations_service: OrganizationsService):
        with pytest.raises(CustomNotFound):
            organization = organizations_service.get_by_id(10)

    def test_get_by_field(self, organizations_service: OrganizationsService):
        organization = organizations_service.get_by_field("name", "Enter")

        assert isinstance(organization, Organizations)

        organization_dict = organizations_service.to_json(organization)

        assert isinstance(organization_dict, dict)
        assert "id" in organization_dict
        assert organization_dict["name"] == "Enter"

    def test_get_by_non_existing_field(
        self, organizations_service: OrganizationsService
    ):
        with pytest.raises(CustomBadRequest):
            organization = organizations_service.get_by_field("names", "Admin")

    def test_get_by_non_existing_field_value(
        self, organizations_service: OrganizationsService
    ):
        with pytest.raises(CustomNotFound):
            organization = organizations_service.get_by_field("name", "asdfasdfasdf")

    def test_get_by_fields(self, organizations_service: OrganizationsService):
        organizations: List[Organizations] = organizations_service.get_by_fields(
            {"soft_deleted": False}, many=True
        )
        organizations_list = organizations_service.to_json(organizations)

        assert isinstance(organizations_list, list)
        assert isinstance(organizations_list[0], dict)
        assert "id" in organizations_list[0]
        assert "name" in organizations_list[0]
        assert organizations_list[0]["soft_deleted"] == False

    def test_get_all_members(self, organizations_service: OrganizationsService):
        members: List[OrganizationMembers] = organizations_service.get_all_members(1)

        assert isinstance(members, list)
        assert len(members) >= 1

    def test_get_all_reports(self, organizations_service: OrganizationsService):
        reports: List[Reports] = organizations_service.get_all_reports(1)

        assert isinstance(reports, list)
        assert len(reports) >= 1

    def test_get_all_datasources(self, organizations_service: OrganizationsService):
        datasources: List[Datasources] = organizations_service.get_all_datasources(1)

        assert isinstance(datasources, list)
        assert len(datasources) >= 1

    def test_create(self, organizations_service: OrganizationsService):
        organization = {
            "name": "Test",
            "description": "Test description",
            "email": "test@email.com",
            "phone": "+1237891216456",
        }
        new_organization: Organizations = organizations_service.create(organization)

        assert isinstance(new_organization, Organizations)
        assert new_organization.id == 3
        assert new_organization.name == "Test"
        assert new_organization.description == "Test description"
        assert new_organization.email == "test@email.com"
        assert new_organization.phone == "+1237891216456"

    def test_create_existing_organization(
        self, organizations_service: OrganizationsService
    ):
        organization = {
            "name": "Test",
            "description": "Test description",
            "email": "test@email.com",
            "phone": "+1237891216456",
        }
        with pytest.raises(CustomBadRequest):
            new_organization: Organizations = organizations_service.create(organization)

    def test_update(self, organizations_service: OrganizationsService):
        updated_organization_dict = {"name": "Test2"}
        updated_organization: Organizations = organizations_service.update(
            3, updated_organization_dict
        )

        assert isinstance(updated_organization, Organizations)
        assert updated_organization.id == 3
        assert updated_organization.name == "Test2"

    def test_update_existing_organization(
        self, organizations_service: OrganizationsService
    ):
        updated_organization_dict = {"name": "Test2"}

        with pytest.raises(CustomBadRequest):
            organization: Organizations = organizations_service.update(
                3, updated_organization_dict
            )

    def test_soft_delete(self, organizations_service: OrganizationsService):
        organization: Organizations = organizations_service.soft_delete(3)

        assert organization.id == 3
        assert organization.name == "Test2"
        assert organization.soft_deleted == True
        assert isinstance(organization.deleted_date, datetime)

    def test_delete(self, organizations_service: OrganizationsService):
        organization: Organizations = organizations_service.delete(3)

        assert organization.id == 3
        assert organization.name == "Test2"

        with pytest.raises(CustomNotFound):
            organization = organizations_service.get_by_id(4)


class TestOrganizationMembersService:
    def test_get_all(self, organization_members_service: OrganizationMembersService):
        organization_members: List[
            OrganizationMembers
        ] = organization_members_service.get_all()

        assert isinstance(organization_members, list)
        assert len(organization_members) == 2

        organization_members_list = organization_members_service.to_json(
            organization_members
        )
        organization_member_dict = organization_members_list[0]

        assert isinstance(organization_member_dict, dict)
        assert "id" in organization_member_dict
        assert "user_id" in organization_member_dict
        assert "organization_id" in organization_member_dict
        assert "active" in organization_member_dict
        assert "role" in organization_member_dict
        assert "updated_date" in organization_member_dict
        assert "created_date" in organization_member_dict
        assert "deleted_date" in organization_member_dict
        assert "soft_deleted" in organization_member_dict

    def test_get_by_id(self, organization_members_service: OrganizationMembersService):
        organization_member = organization_members_service.get_by_id(1)

        assert isinstance(organization_member, OrganizationMembers)

        organization_member_dict = organization_members_service.to_json(
            organization_member
        )

        assert isinstance(organization_member_dict, dict)
        assert "id" in organization_member_dict
        assert "user_id" in organization_member_dict
        assert "organization_id" in organization_member_dict
        assert "active" in organization_member_dict
        assert "role" in organization_member_dict

    def test_get_by_non_existing_id(
        self, organization_members_service: OrganizationMembersService
    ):
        with pytest.raises(CustomNotFound):
            organization_member = organization_members_service.get_by_id(10)

    def test_get_by_field(
        self, organization_members_service: OrganizationMembersService
    ):
        organization_member = organization_members_service.get_by_field("user_id", 1)

        assert isinstance(organization_member, OrganizationMembers)

        organization_member_dict = organization_members_service.to_json(
            organization_member
        )

        assert isinstance(organization_member_dict, dict)
        assert "id" in organization_member_dict

    def test_get_by_non_existing_field(
        self, organization_members_service: OrganizationMembersService
    ):
        with pytest.raises(CustomBadRequest):
            organization_member = organization_members_service.get_by_field(
                "names", "Admin"
            )

    def test_get_by_non_existing_field_value(
        self, organization_members_service: OrganizationMembersService
    ):
        with pytest.raises(CustomNotFound):
            organization_member = organization_members_service.get_by_field(
                "user_id", 123
            )

    def test_get_by_fields(
        self, organization_members_service: OrganizationMembersService
    ):
        organization_members: List[
            OrganizationMembers
        ] = organization_members_service.get_by_fields(
            {"soft_deleted": False}, many=True
        )
        organization_members_list = organization_members_service.to_json(
            organization_members
        )

        assert isinstance(organization_members_list, list)
        assert isinstance(organization_members_list[0], dict)
        assert "id" in organization_members_list[0]
        assert organization_members_list[0]["soft_deleted"] == False

    def test_get_user(self, organization_members_service: OrganizationMembersService):
        user: Users = organization_members_service.get_user(1)

        assert isinstance(user, Users)

    def test_get_organization(
        self, organization_members_service: OrganizationMembersService
    ):
        organization: Organizations = organization_members_service.get_organization(1)

        assert isinstance(organization, Organizations)

    def test_get_all_datasources(
        self, organization_members_service: OrganizationMembersService
    ):
        datasources: List[
            Datasources
        ] = organization_members_service.get_all_datasources(1)

        assert isinstance(datasources, list)
        assert len(datasources) >= 1

    def test_get_all_reports(
        self, organization_members_service: OrganizationMembersService
    ):
        reports: List[Reports] = organization_members_service.get_all_reports(1)

        assert isinstance(reports, list)
        assert len(reports) >= 1

    def test_create(self, organization_members_service: OrganizationMembersService):
        organization_member = {
            "user_id": 2,
            "organization_id": 2,
            "role": "OWNER",
            "active": True,
        }
        new_organization_member: OrganizationMembers = (
            organization_members_service.create(organization_member)
        )

        assert isinstance(new_organization_member, OrganizationMembers)
        assert new_organization_member.id == 3
        assert new_organization_member.user_id == 2
        assert new_organization_member.organization_id == 2
        assert new_organization_member.role == OrganizationRoles.OWNER
        assert new_organization_member.active == True

    def test_create_existing_organization_member(
        self, organization_members_service: OrganizationMembersService
    ):
        organization_member = {
            "user_id": 2,
            "organization_id": 2,
            "role": "OWNER",
            "active": True,
        }
        with pytest.raises(CustomBadRequest):
            new_organization_member: OrganizationMembers = (
                organization_members_service.create(organization_member)
            )

    def test_update(self, organization_members_service: OrganizationMembersService):
        updated_organization_member_dict = {"role": "ADMIN"}
        updated_organization_member: OrganizationMembers = (
            organization_members_service.update(3, updated_organization_member_dict)
        )

        assert isinstance(updated_organization_member, OrganizationMembers)
        assert updated_organization_member.id == 3
        assert updated_organization_member.role == OrganizationRoles.ADMIN

    def test_update_existing_organization_member(
        self, organization_members_service: OrganizationMembersService
    ):
        updated_organization_member_dict = {"role": "TEST"}

        with pytest.raises(CustomBadRequest):
            organization_member: OrganizationMembers = (
                organization_members_service.update(3, updated_organization_member_dict)
            )

    def test_soft_delete(
        self, organization_members_service: OrganizationMembersService
    ):
        organization_member: OrganizationMembers = (
            organization_members_service.soft_delete(3)
        )

        assert organization_member.id == 3
        assert organization_member.soft_deleted == True
        assert isinstance(organization_member.deleted_date, datetime)

    def test_delete(self, organization_members_service: OrganizationMembersService):
        organization_member: OrganizationMembers = organization_members_service.delete(
            3
        )

        assert organization_member.id == 3

        with pytest.raises(CustomNotFound):
            organization_member = organization_members_service.get_by_id(4)
