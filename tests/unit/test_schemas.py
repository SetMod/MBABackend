from typing import List

from marshmallow import ValidationError
from app.models import Roles, Users
from app.schemas import UsersSchema
import pytest

class TestUsersSchema:
    def test_schema_dump(self, users_schema: UsersSchema, create_users: List[Users]):
        user = create_users[0]
        user_dict = users_schema.dump(user)

        assert isinstance(user_dict, dict)
        assert user_dict["id"] == 1
        assert user_dict["first_name"] == "John"
        assert user_dict["second_name"] == "Doe"
        assert user_dict["username"] == "johndoe"
        assert user_dict["role"] == Roles.USER.name

    def test_schema_dump_many(
        self, users_schema: UsersSchema, create_users: List[Roles]
    ):
        users_list = users_schema.dump(create_users, many=True)

        assert isinstance(users_list, list)
        assert isinstance(users_list[0], dict)

    def test_schema_load(self, users_schema: UsersSchema):
        user_dict = {
            "first_name": "John",
            "second_name": "Doe",
            "username": "johndoe",
            "active": True,
            "email": "john.doe@gmail.com",
            "phone": "+3801234567",
            "password": "s3cr3TP@@$w0Rd",
            "role": Roles.USER.name,
        }
        user = users_schema.load(user_dict)

        assert isinstance(user, dict)
        assert user["first_name"] == "John"
        assert user["second_name"] == "Doe"
        assert user["username"] == "johndoe"
        assert user["role"] == Roles.USER

    def test_schema_load_with_missing_password(self, users_schema: UsersSchema):
        user_dict = {
            "first_name": "John",
            "second_name": "Doe",
            "username": "johndoe",
            "active": True,
            "email": "john.doe@gmail.com",
            "phone": "+3801234567",
            # "password": "s3cr3TP@@$w0Rd",
            "role": Roles.USER.name,
        }
        with pytest.raises(ValidationError) as err:
            user = users_schema.load(user_dict)

        assert err.match("Missing 'password' required field")
