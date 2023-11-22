# from datetime import datetime
# from typing import List
# import pytest
# from sqlalchemy import ChunkedIteratorResult, Row, Sequence
# from app.logger import logger
# from app.exceptions import CustomNotFound, CustomBadRequest
# from app.models import Roles, Users
# from flask_sqlalchemy import SQLAlchemy


# class TestRoles:
#     def test_get_all(self):
#         roles = Roles.get_all()
#         assert isinstance(roles, list)
#         assert len(roles) == 2

#     def test_get_by_id(self):
#         role: Roles = Roles.get_by_id(1)
#         assert isinstance(role, Roles)
#         assert role.id == 1
#         assert role.name == "User"

#     def test_get_by_bad_id(self):
#         with pytest.raises(CustomNotFound):
#             role: Roles = Roles.get_by_id(10)
#         with pytest.raises(CustomBadRequest):
#             role: Roles = Roles.get_by_id("ads")

#     def test_get_by_field(self):
#         role: Roles = Roles.get_by_field("name", "Admin")
#         assert isinstance(role, Roles)
#         assert role.id == 2
#         assert role.name == "Admin"

#     def test_get_by_non_existing_field(self):
#         with pytest.raises(CustomBadRequest):
#             role: Roles = Roles.get_by_field("names", "Admin")

#     def test_get_by_bad_fields(self):
#         roles: List[Roles] = Roles.get_by_fields({"soft_deleted": False}, many=True)
#         assert isinstance(roles, list)
#         assert isinstance(roles[0], Roles)
#         assert roles[0].soft_deleted == False

#     def test_get_by_unique_fields(self):
#         role: Roles = Roles.get_by_unique_fields({"name": "Admin"}, must_exist=True)
#         assert isinstance(role, Roles)
#         assert role.id == 2
#         assert role.name == "Admin"

#     def test_get_by_non_unique_fields(self):
#         role = Roles.get_by_unique_fields({"names": "Admin"})
#         assert role == None
#         role: Roles = Roles.get_by_unique_fields(
#             {"soft_deleted": True}, must_exist=True
#         )
#         assert role == None

#     def test_create(self):
#         role_dict = {"name": "Developers", "description": "Roles for developers"}
#         role: Roles = Roles.create(role_dict)

#         assert role.id == 3
#         assert role.name == "Developers"
#         assert role.description == "Roles for developers"

#     def test_create_existing_role(self):
#         role_dict = {"name": "Developers", "description": "Roles for developers"}
#         with pytest.raises(CustomBadRequest):
#             role: Roles = Roles.create(role_dict)

#     def test_update(self):
#         existing_role: Roles = Roles.get_by_id(3)
#         update_role_dict = {"name": "Viewer", "description": "Roles for viewers"}
#         role: Roles = existing_role.update(update_role_dict)

#         assert role.id == 3
#         assert role.name == "Viewer"
#         assert role.description == "Roles for viewers"

#     def test_update_description(self):
#         existing_role: Roles = Roles.get_by_id(3)
#         update_role_dict = {"description": "Role for viewers"}
#         role: Roles = existing_role.update(update_role_dict)

#         assert role.id == 3
#         assert role.name == "Viewer"
#         assert role.description == "Role for viewers"

#     def test_update_non_existing_role(self):
#         with pytest.raises(CustomNotFound):
#             existing_role: Roles = Roles.get_by_id(123)
#             update_role_dict = {"name": "Viewer", "description": "Roles for viewers"}
#             role: Roles = existing_role.update(update_role_dict)

#     def test_update_existing_role(self):
#         with pytest.raises(CustomBadRequest):
#             existing_role: Roles = Roles.get_by_id(3)
#             update_role_dict = {"name": "Viewer", "description": "Roles for viewers"}
#             role: Roles = existing_role.update(update_role_dict)

#     def test_get_users(self):
#         existing_role: Roles = Roles.get_by_id(2)
#         role_users: List[Users] = existing_role.users
#         logger.info(f"Role users: {role_users}")

#         assert isinstance(role_users, list)
#         assert len(role_users) == 1

#     def test_get_users_empty(self):
#         existing_role: Roles = Roles.get_by_id(3)
#         role_users: List[Users] = existing_role.users
#         logger.info(f"Role users: {role_users}")

#         assert isinstance(role_users, list)
#         assert len(role_users) == 0

#     def test_soft_delete(self):
#         existing_role: Roles = Roles.get_by_id(3)
#         role: Roles = existing_role.soft_delete()

#         assert role.id == 3
#         assert role.soft_deleted == True
#         assert role.deleted_date != None
#         assert isinstance(role.deleted_date, datetime)

#     def test_delete(self):
#         existing_role: Roles = Roles.get_by_id(3)
#         role: Roles = existing_role.delete()

#         assert role.id == 3
#         assert role.name == "Viewer"

#         with pytest.raises(CustomNotFound):
#             existing_role: Roles = Roles.get_by_id(3)


# class TestUsers:
#     def test_get_all(self):
#         users = Users.get_all()

#         assert isinstance(users, list)
#         assert len(users) == 2

#     def test_get_by_id(self):
#         user: Users = Users.get_by_id(1)

#         assert isinstance(user, Users)

#     def test_get_by_fields(self):
#         users: List[Users] = Users.get_by_fields({"first_name": "John"}, many=True)

#         assert isinstance(users, list)
#         assert isinstance(users[0], Users)
#         assert users[0].first_name == "John"

#     def test_get_by_field(self):
#         user: Users = Users.get_by_fields({"first_name": "John"}, many=False)

#         assert isinstance(user, Users)
#         assert user.first_name == "John"

#     def test_get_by_unique_fields(self):
#         user: Users = Users.get_by_unique_fields(
#             {"username": "johndoe"}, must_exist=True
#         )

#         assert isinstance(user, Users)
#         assert user.username == "johndoe"

#     def test_create(self):
#         user = {
#             "first_name": "Bob",
#             "second_name": "Ross",
#             "username": "bobross",
#             "active": True,
#             "email": "bob.ross@gmail.com",
#             "phone": "+123789123978",
#             "password": "jkZJK#@kn1x23",
#             "role_id": 1,
#         }
#         new_user: Users = Users.create(user)

#         assert isinstance(new_user, Users)
#         assert new_user.id == 3
#         assert new_user.first_name == "Bob"
#         assert new_user.second_name == "Ross"
#         assert new_user.username == "bobross"
#         assert new_user.active == True
#         assert new_user.role_id == 1

#     def test_update(self):
#         existing_user: Users = Users.get_by_id(3)
#         updated_user_dict = {"username": "bob_ross"}
#         updated_user: Users = existing_user.update(updated_user_dict)

#         assert isinstance(updated_user, Users)
#         assert updated_user.id == 3
#         assert updated_user.username == "bob_ross"

#     def test_soft_delete(self):
#         existing_user: Users = Users.get_by_id(3)
#         user: Users = existing_user.soft_delete()

#         assert isinstance(user, Users)
#         assert user.id == 3
#         assert user.soft_deleted == True
#         assert user.deleted_date != None
#         assert isinstance(user.deleted_date, datetime)

#     def test_delete(self):
#         existing_user: Users = Users.get_by_id(3)
#         user: Users = existing_user.delete()

#         assert isinstance(user, Users)
#         assert user.id == 3
#         assert user.username == "bob_ross"

#         with pytest.raises(CustomNotFound):
#             user: Roles = Users.get_by_id(3)
