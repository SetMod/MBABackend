from typing import List
from app.models import Roles
from app.schemas import RolesSchema


class TestRolesSchema:
    def test_schema_dump(self, roles_schema: RolesSchema, create_roles: List[Roles]):
        user_role = create_roles[0]
        dump_role = roles_schema.dump(user_role)

        assert isinstance(dump_role, dict)
        assert dump_role["id"] == 1
        assert dump_role["name"] == "User"
        assert dump_role["description"] == "Roles for users"
        assert dump_role["soft_deleted"] == False

    def test_schema_dump_many(
        self, roles_schema: RolesSchema, create_roles: List[Roles]
    ):
        dump_role = roles_schema.dump(create_roles, many=True)

        assert isinstance(dump_role, list)
        assert isinstance(dump_role[0], dict)

    def test_schema_load(self, roles_schema: RolesSchema):
        user_role = {"name": "User", "description": "Role for users"}
        loaded_role = roles_schema.load(user_role)

        assert isinstance(loaded_role, dict)
        assert loaded_role["name"] == "User"
        assert loaded_role["description"] == "Role for users"
