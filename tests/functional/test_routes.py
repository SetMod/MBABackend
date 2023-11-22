from flask.testing import FlaskClient
from app.logger import logger


class TestRolesRoute:
    base_api = "/api/v1/roles"

    def test_get_all(self, client: FlaskClient):
        response = client.get(f"{self.base_api}", follow_redirects=True)
        roles_list = response.json
        logger.info(roles_list)

        assert isinstance(roles_list, list)

    def test_get_all_with_params(self, client: FlaskClient):
        response = client.get(f"{self.base_api}?name=User", follow_redirects=True)
        roles_list = response.json
        logger.info(roles_list)

        assert isinstance(roles_list, dict)

    # def test_get_all_with_params_2(self, client: FlaskClient):
    #     logger.info("Find me here")
    #     response = client.get(f"{self.base_api}?soft_deleted=False", follow_redirects=True)
    #     roles_list = response.json
    #     logger.info(roles_list)

    #     assert isinstance(roles_list, list)

    def test_get_all_with_bad_params(self, client: FlaskClient):
        logger.info("Find me here2")
        response = client.get(
            f"{self.base_api}?soft_deleted=True", follow_redirects=True
        )
        res_data = response.json

        assert response.content_type == "application/json"
        assert response.status_code == 404
        assert isinstance(res_data, dict)

    def test_get_by_id(self, client: FlaskClient):
        role_id = 1
        response = client.get(f"{self.base_api}/{role_id}")
        role_dict = response.json

        assert isinstance(role_dict, dict)
        assert "id" in role_dict
        assert "name" in role_dict
        assert "description" in role_dict
        assert "updated_date" in role_dict
        assert "created_date" in role_dict
        assert "deleted_date" in role_dict
        assert "soft_deleted" in role_dict

    def test_get_users(self, client: FlaskClient):
        role_id = 1
        response = client.get(f"{self.base_api}/{role_id}/users")
        users_list = response.json

        assert isinstance(users_list, list)

    def test_create(self, client: FlaskClient):
        role_dict = {"name": "Developers", "description": "Roles for developers"}
        response = client.post(
            f"{self.base_api}/",
            json=role_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token"),
            },
        )
        role = response.json
        logger.info(response.data)
        assert isinstance(role, dict)
        assert role["name"] == "Developers"

    def test_update(self, client: FlaskClient):
        role_id = 3
        role_dict = {"description": "Role for developers"}
        response = client.put(
            f"{self.base_api}/{role_id}",
            json=role_dict,
            headers={"Content-Type": "application/json"},
        )
        role = response.json

        assert isinstance(role, dict)
        assert role["name"] == "Developers"

    def test_soft_delete(self, client: FlaskClient):
        role_id = 3
        response = client.delete(f"{self.base_api}/{role_id}/soft")
        role = response.json

        assert isinstance(role, dict)
        assert role["id"] == 3
        assert role["name"] == "Developers"
        assert role["soft_deleted"] == True
        assert role["deleted_date"] != None

    def test_delete(self, client: FlaskClient):
        role_id = 3
        response = client.delete(f"{self.base_api}/{role_id}")
        role = response.json

        assert isinstance(role, dict)
        assert role["id"] == 3
        assert role["name"] == "Developers"


# class TestUsersRoute:
#     base_api = "/api/v1/users"

#     def test_login(self, client: FlaskClient):
#         user = {"username": "johndoe", "password": "s3cr3TP@@$w0Rd"}
#         res = client.post(
#             "/api/v1/auth/login",
#             json=user,
#         )
#         logger.info("Login response data:")
#         logger.info(res.json)
#         logger.info(res.headers)

#     # def test_login(self, client: FlaskClient):
#     #     res = client.get(
#     #         "/api/v1/auth/logout",
#     #     )
#     #     logger.info("Logout response data:")
#     #     logger.info(res.json)
#     #     logger.info(res.headers)

#     def test_get_all(self, client: FlaskClient):
#         response = client.get(f"{self.base_api}", follow_redirects=True)
#         users_list = response.json
#         logger.info(users_list)

#         assert isinstance(users_list, list)

#     def test_get_all_with_params(self, client: FlaskClient):
#         response = client.get(
#             f"{self.base_api}?username=johndoe", follow_redirects=True
#         )
#         users_list = response.json
#         logger.info(users_list)

#         assert isinstance(users_list, dict)

#     # def test_get_all_with_params_2(self, client: FlaskClient):
#     #     response = client.get("{self.base_api}?soft_deleted=False", follow_redirects=True)
#     #     roles_list = response.json
#     #     logger.info(roles_list)

#     #     assert isinstance(roles_list, list)

#     def test_get_all_with_bad_params(self, client: FlaskClient):
#         response = client.get(
#             f"{self.base_api}?soft_deleted=True", follow_redirects=True
#         )
#         res_data = response.json

#         assert response.content_type == "application/json"
#         assert response.status_code == 404
#         assert isinstance(res_data, dict)

#     def test_get_by_id(self, client: FlaskClient):
#         user_id = 1
#         response = client.get(f"{self.base_api}/{user_id}")
#         role_dict = response.json

#         assert isinstance(role_dict, dict)
#         assert "id" in role_dict
#         assert "username" in role_dict
#         assert "updated_date" in role_dict
#         assert "created_date" in role_dict
#         assert "deleted_date" in role_dict
#         assert "soft_deleted" in role_dict

#     def test_get_role(self, client: FlaskClient):
#         user_id = 1
#         response = client.get(f"{self.base_api}/{user_id}/role")
#         role_dict = response.json

#         assert isinstance(role_dict, dict)
#         assert "id" in role_dict
#         assert "name" in role_dict
#         assert "description" in role_dict

#     def test_get_organizations(self, client: FlaskClient):
#         user_id = 1
#         response = client.get(f"{self.base_api}/{user_id}/organizations")
#         organizations_list = response.json

#         assert isinstance(organizations_list, list)

#     def test_get_reports(self, client: FlaskClient):
#         user_id = 1
#         response = client.get(f"{self.base_api}/{user_id}/reports")
#         reports_list = response.json

#         assert isinstance(reports_list, list)

#     def test_get_datasources(self, client: FlaskClient):
#         user_id = 1
#         response = client.get(f"{self.base_api}/{user_id}/datasources")
#         datasources_list = response.json

#         assert isinstance(datasources_list, list)

#     def test_create(self, client: FlaskClient):
#         user_dict = {
#             "first_name": "Bob",
#             "second_name": "Ross",
#             "username": "bobross",
#             "active": True,
#             "email": "bob.ross@gmail.com",
#             "phone": "+123789123978",
#             "password": "jkZJK#@kn1x23",
#             "role_id": 1,
#         }
#         response = client.post(
#             f"{self.base_api}/",
#             json=user_dict,
#             headers={"Content-Type": "application/json"},
#         )
#         user = response.json
#         logger.info(user)
#         assert isinstance(user, dict)
#         assert user["id"] == 3
#         assert user["username"] == "bobross"

#     def test_update(self, client: FlaskClient):
#         user_id = 3
#         user_dict = {"username": "bob_ross"}
#         response = client.put(
#             f"{self.base_api}/{user_id}",
#             json=user_dict,
#             headers={"Content-Type": "application/json"},
#         )
#         user = response.json

#         assert isinstance(user, dict)
#         assert user["id"] == 3
#         assert user["username"] == "bob_ross"

#     def test_soft_delete(self, client: FlaskClient):
#         user_id = 3
#         response = client.delete(f"{self.base_api}/{user_id}/soft")
#         user = response.json

#         assert isinstance(user, dict)
#         assert user["id"] == 3
#         assert user["username"] == "bob_ross"
#         assert user["soft_deleted"] == True
#         assert user["deleted_date"] != None

#     def test_delete(self, client: FlaskClient):
#         user_id = 3
#         response = client.delete(f"{self.base_api}/{user_id}")
#         user = response.json

#         assert isinstance(user, dict)
#         assert user["id"] == 3
#         assert user["username"] == "bob_ross"


# # class TestOrganizationsRoute:
# #     base_api = "/api/v1/organizations"

# #     def test_get_all(self, client: FlaskClient):
# #         response = client.get(self.base_api, follow_redirects=True)
# #         users_list = response.json
# #         logger.info(users_list)

# #         assert isinstance(users_list, list)

# #     def test_get_all_with_params(self, client: FlaskClient):
# #         response = client.get(f"{self.base_api}?name=LocalStore", follow_redirects=True)
# #         users_list = response.json
# #         logger.info(users_list)

# #         assert isinstance(users_list, dict)

# #     # def test_get_all_with_params_2(self, client: FlaskClient):
# #     #     logger.info("Find me here")
# #     #     response = client.get("/api/v1/roles?soft_deleted=False", follow_redirects=True)
# #     #     roles_list = response.json
# #     #     logger.info(roles_list)

# #     #     assert isinstance(roles_list, list)

# #     def test_get_all_with_bad_params(self, client: FlaskClient):
# #         response = client.get(
# #             f"{self.base_api}?soft_deleted=True", follow_redirects=True
# #         )
# #         res_data = response.json

# #         assert response.content_type == "application/json"
# #         assert response.status_code == 404
# #         assert isinstance(res_data, dict)

# #     def test_get_by_id(self, client: FlaskClient):
# #         org_id = 1
# #         response = client.get(f"{self.base_api}/{org_id}")
# #         role_dict = response.json

# #         assert isinstance(role_dict, dict)
# #         assert "id" in role_dict
# #         assert "name" in role_dict
# #         assert "description" in role_dict
# #         assert "updated_date" in role_dict
# #         assert "created_date" in role_dict
# #         assert "deleted_date" in role_dict
# #         assert "soft_deleted" in role_dict

# #     def test_get_members(self, client: FlaskClient):
# #         org_id = 1
# #         response = client.get(
# #             f"{self.base_api}/{org_id}/members", follow_redirects=True
# #         )
# #         members_list = response.json

# #         assert isinstance(members_list, list)

# #     def test_get_member_by_id(self, client: FlaskClient):
# #         org_id = 1
# #         user_id = 1
# #         response = client.get(
# #             f"{self.base_api}/{org_id}/members/{user_id}", follow_redirects=True
# #         )
# #         assert response.status_code == 404

# #     # def test_add_member(self, client: FlaskClient):
# #     #     org_id = 1
# #     #     member = {"user_id": 1, "organization_id": 1}
# #     #     response = client.get(f"{self.base_api}/{org_id}/member/")
# #     #     members_list = response.json

# #     #     assert isinstance(members_list, list)
