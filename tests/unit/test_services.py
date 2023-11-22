from datetime import datetime
from typing import List
import pytest
from app.exceptions import CustomBadRequest, CustomNotFound
from app.models import Datasources, Organizations, Reports, Roles, Users
from app.services import RolesService, UsersService


class TestRolesService:
    def test_get_all(self, roles_service: RolesService):
        roles = roles_service.get_all()

        assert isinstance(roles, list)
        assert len(roles) == 2

        roles = roles_service.to_json(roles)
        role_dict = roles[0]

        assert isinstance(roles[0], dict)
        assert "id" in role_dict
        assert "name" in role_dict
        assert "description" in role_dict
        assert "updated_date" in role_dict
        assert "created_date" in role_dict
        assert "deleted_date" in role_dict
        assert "soft_deleted" in role_dict

    def test_get_by_id(self, roles_service: RolesService):
        role = roles_service.get_by_id(1)

        assert isinstance(role, Roles)

        role = roles_service.to_json(role)

        assert isinstance(role, dict)
        assert "id" in role
        assert "name" in role
        assert "description" in role
        assert "updated_date" in role
        assert "created_date" in role
        assert "deleted_date" in role
        assert "soft_deleted" in role

    def test_get_by_non_existing_id(self, roles_service: RolesService):
        with pytest.raises(CustomNotFound):
            role = roles_service.get_by_id(10)

    def test_get_by_field(self, roles_service: RolesService):
        role = roles_service.get_by_field("name", "Admin")

        assert isinstance(role, Roles)

        role = roles_service.to_json(role)

        assert isinstance(role, dict)
        assert "id" in role
        assert role["name"] == "Admin"

    def test_get_by_non_existing_field(self, roles_service: RolesService):
        with pytest.raises(CustomBadRequest):
            role = roles_service.get_by_field("names", "Admin")

    def test_get_by_non_existing_field_value(self, roles_service: RolesService):
        with pytest.raises(CustomNotFound):
            role = roles_service.get_by_field("name", "Administrators")

    def test_get_by_fields(self, roles_service: RolesService):
        roles: List[Roles] = roles_service.get_by_fields(
            {"soft_deleted": False}, many=True
        )
        roles = roles_service.to_json(roles)

        assert isinstance(roles, list)
        assert isinstance(roles[0], dict)
        assert "id" in roles[0]
        assert "name" in roles[0]
        assert "description" in roles[0]
        assert roles[0]["soft_deleted"] == False

    def test_get_all_users(self, roles_service: RolesService):
        users: List[Users] = roles_service.get_all_users(1)

        assert isinstance(users, list)
        assert isinstance(users[0], Users)
        assert users[0].role_id == 1

    def test_create(self, roles_service: RolesService):
        editor_role = Roles(name="Editor", description="Role for editors")
        editor_role_dict = roles_service.to_json(editor_role)
        new_role = roles_service.create(editor_role_dict)
        new_role = roles_service.to_json(new_role)

        assert isinstance(new_role, dict)
        assert "id" in new_role
        assert "name" in new_role
        assert "description" in new_role
        assert new_role["name"] == "Editor"

    def test_create_from_dict(self, roles_service: RolesService):
        owner_role_dict = {"name": "Owner", "description": "Role for owners"}
        new_role = roles_service.create(owner_role_dict)

        assert isinstance(new_role, Roles)

        new_role = roles_service.to_json(new_role)

        assert isinstance(new_role, dict)
        assert "id" in new_role
        assert "name" in new_role
        assert "description" in new_role
        assert new_role["name"] == "Owner"

    def test_map_model(self, roles_service: RolesService):
        editor_role_dict = {"name": "Owner", "description": "Role for owners"}
        editor_role = roles_service.map_model(editor_role_dict)

        assert isinstance(editor_role, Roles)
        assert editor_role.name == "Owner"
        assert editor_role.description == "Role for owners"

    def test_map_bad_model(self, roles_service: RolesService):
        editor_role_dict = {"names": "Owner", "descriptions": "Role for owners"}

        with pytest.raises(CustomBadRequest):
            editor_role = roles_service.map_model(editor_role_dict)

    def test_create_existing_role(self, roles_service: RolesService):
        editor_role_dict = {"name": "Owner", "description": "Role for owners"}

        with pytest.raises(CustomBadRequest):
            new_role = roles_service.create(editor_role_dict)

    def test_update(self, roles_service: RolesService):
        creator_role = Roles(name="Creator", description="Role for creators")
        creator_role_dict = roles_service.to_json(creator_role)

        updated_role: Roles = roles_service.update(4, creator_role_dict)
        updated_role = roles_service.to_json(updated_role)

        assert isinstance(updated_role, dict)
        assert "id" in updated_role
        assert updated_role["id"] == 4
        assert "name" in updated_role
        assert "description" in updated_role
        assert updated_role["name"] == "Creator"

    def test_update_existing_role(self, roles_service: RolesService):
        creator_role_dict = {"name": "Creator", "description": "Role for creators"}

        with pytest.raises(CustomBadRequest):
            updated_role = roles_service.update(3, creator_role_dict)

    def test_soft_delete(self, roles_service: RolesService):
        role: Roles = roles_service.soft_delete(4)

        assert role.id == 4
        assert role.name == "Creator"
        assert role.soft_deleted == True
        assert isinstance(role.deleted_date, datetime)

    def test_delete(self, roles_service: RolesService):
        role: Roles = roles_service.delete(4)

        assert role.id == 4
        assert role.name == "Creator"

        with pytest.raises(CustomNotFound):
            existing_role = roles_service.get_by_id(4)


class TestUsersService:
    def test_get_all(self, users_service: UsersService):
        users: List[Users] = users_service.get_all()

        assert isinstance(users, list)
        assert len(users) == 2

        users_list = users_service.to_json(users)
        user_dict = users_list[0]

        assert isinstance(user_dict, dict)
        assert "id" in user_dict
        assert "first_name" in user_dict
        assert "second_name" in user_dict
        assert "username" in user_dict
        assert "email" in user_dict
        assert "phone" in user_dict
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

    def test_get_role(self, users_service: UsersService):
        role: Roles = users_service.get_role(1)

        assert isinstance(role, Roles)

    def test_get_all_organizations(self, users_service: UsersService):
        organizations: List[Organizations] = users_service.get_all_organizations(1)

        assert isinstance(organizations, list)
        assert len(organizations) == 0

    def test_get_all_reports(self, users_service: UsersService):
        reports: List[Reports] = users_service.get_all_reports(1)

        assert isinstance(reports, list)
        assert len(reports) == 0

    def test_get_all_datasources(self, users_service: UsersService):
        datasources: List[Datasources] = users_service.get_all_datasources(1)

        assert isinstance(datasources, list)
        assert len(datasources) == 0

    def test_create(self, users_service: UsersService):
        user = {
            "first_name": "Bob",
            "second_name": "Ross",
            "username": "bobross",
            "active": True,
            "email": "bob.ross@gmail.com",
            "phone": "+123789123978",
            "password": "jkZJK#@kn1x23",
            "role_id": 1,
        }
        new_user: Users = users_service.create(user)

        assert isinstance(new_user, Users)
        assert new_user.id == 3
        assert new_user.first_name == "Bob"
        assert new_user.second_name == "Ross"
        assert new_user.username == "bobross"
        assert new_user.active == True
        assert new_user.role_id == 1

    def test_map_model(self, users_service: UsersService):
        user = {
            "first_name": "Bob",
            "second_name": "Ross",
            "username": "bobross",
            "active": True,
            "email": "bob.ross@gmail.com",
            "phone": "+123789123978",
            "password_hash": "jkjl1j123jklKJklnzx12",
            "role_id": 1,
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
            "role_id": 1,
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
