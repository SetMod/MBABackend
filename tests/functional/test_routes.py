from flask.testing import FlaskClient
from app.logger import logger
from app.models import OrganizationRoles, Roles


class TestUsersRoute:
    base_api = "/api/v1/users"

    def test_get_all_without_login(self, client: FlaskClient):
        res = client.get(self.base_api, follow_redirects=True)
        error = res.json
        logger.info(error)

        assert res.status_code == 401
        assert isinstance(error, dict)
        assert (
            error["msg"]
            == 'Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")'
        )

    def test_login(self, client: FlaskClient):
        user = {"username": "johndoe", "password": "s3cr3TP@@$w0Rd"}
        res = client.post(
            f"{self.base_api}/auth/login",
            json=user,
        )
        logger.info(res.json)
        logger.info(res.headers)

    def test_logout(self, client: FlaskClient):
        res = client.get(
            f"{self.base_api}/auth/logout",
        )
        logger.info(res.json)
        logger.info(res.headers)

    def test_who_am_i(self, client: FlaskClient, login: dict):
        res = client.get(
            f"{self.base_api}/auth/who_am_i", headers=login, follow_redirects=True
        )
        user_dict = res.json
        logger.info(user_dict)

        assert isinstance(user_dict, dict)
        assert "id" in user_dict
        assert "username" in user_dict
        assert "updated_date" in user_dict
        assert "created_date" in user_dict
        assert "deleted_date" in user_dict
        assert "soft_deleted" in user_dict
        assert user_dict["username"] == "johndoe"

    def test_get_all(self, client: FlaskClient, login: dict):
        res = client.get(self.base_api, headers=login, follow_redirects=True)
        users_list = res.json
        logger.info(users_list)

        assert isinstance(users_list, list)

    def test_get_all_with_params(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            query_string={"username": "johndoe"},
            headers=login,
            follow_redirects=True,
        )
        users_list = res.json
        logger.info(users_list)

        assert isinstance(users_list, list)

    def test_get_all_with_two_params(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            query_string={"soft_deleted": False, "active": True},
            headers=login,
            follow_redirects=True,
        )
        roles_list = res.json
        logger.info(roles_list)

        assert isinstance(roles_list, list)

    def test_get_all_with_bad_params(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            query_string={"deleted": "true"},
            headers=login,
            follow_redirects=True,
        )
        res_data = res.json

        assert res.content_type == "application/json"
        assert res.status_code == 400
        assert isinstance(res_data, dict)

    def test_get_by_id(self, client: FlaskClient, login: dict):
        user_id = 1
        res = client.get(
            f"{self.base_api}/{user_id}",
            headers=login,
            follow_redirects=True,
        )
        user_dict = res.json

        assert isinstance(user_dict, dict)
        assert "id" in user_dict
        assert "username" in user_dict
        assert "updated_date" in user_dict
        assert "created_date" in user_dict
        assert "deleted_date" in user_dict
        assert "soft_deleted" in user_dict

    def test_get_organizations(self, client: FlaskClient, login: dict):
        user_id = 1
        res = client.get(
            f"{self.base_api}/{user_id}/organizations",
            headers=login,
            follow_redirects=True,
        )
        organizations_list = res.json
        logger.info(organizations_list)

        assert isinstance(organizations_list, list)

    def test_get_reports(self, client: FlaskClient, login: dict):
        user_id = 1
        res = client.get(
            f"{self.base_api}/{user_id}/reports",
            headers=login,
            follow_redirects=True,
        )
        reports_list = res.json
        logger.info(reports_list)

        assert isinstance(reports_list, list)

    def test_get_datasources(self, client: FlaskClient, login: dict):
        user_id = 1
        res = client.get(
            f"{self.base_api}/{user_id}/datasources",
            headers=login,
            follow_redirects=True,
        )
        datasources_list = res.json
        logger.info(datasources_list)

        assert isinstance(datasources_list, list)

    def test_create(self, client: FlaskClient, login: dict):
        user_dict = {
            "first_name": "Bob",
            "second_name": "Ross",
            "username": "bobross",
            "active": True,
            "email": "bob.rosss@gmail.com",
            "phone": "+123789123078",
            "password": "jkZJK#@kn1x23",
            "role": Roles.ADMIN.name,
        }
        logger.info(f"X-CSRF-TOKEN: {client.get_cookie('csrf_access_token')}")
        res = client.post(
            self.base_api,
            json=user_dict,
            # headers={
            #     "Content-Type": "application/json",
            #     "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            # },
            headers=login,
            follow_redirects=True,
        )
        user = res.json
        logger.info(user)

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bobross"
        assert user["role"] == Roles.ADMIN.name

    def test_update(self, client: FlaskClient, login: dict):
        user_id = 3
        user_dict = {"username": "bob_ross", "password": "Nk23@jk983Jkr"}
        res = client.put(
            f"{self.base_api}/{user_id}",
            json=user_dict,
            # headers={
            #     "Content-Type": "application/json",
            #     "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            # },
            headers=login,
            follow_redirects=True,
        )
        user = res.json

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bob_ross"

    def test_soft_delete(self, client: FlaskClient, login: dict):
        user_id = 3
        res = client.delete(
            f"{self.base_api}/{user_id}/soft",
            # headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
            headers=login,
            follow_redirects=True,
        )
        user = res.json

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bob_ross"
        assert user["soft_deleted"] == True
        assert user["deleted_date"] != None

    def test_delete(self, client: FlaskClient, login: dict):
        user_id = 3
        res = client.delete(
            f"{self.base_api}/{user_id}",
            # headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
            headers=login,
            follow_redirects=True,
        )
        user = res.json

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bob_ross"


class TestOrganizationsRoute:
    base_api = "/api/v1/organizations"

    def test_get_all(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            headers=login,
            follow_redirects=True,
        )
        orgs_list = res.json
        logger.info(orgs_list)

        assert res.status_code == 200
        assert res.content_type == "application/json"
        assert isinstance(orgs_list, list)

    def test_get_all_with_params(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            query_string={"name": "LocalStore"},
            headers=login,
            follow_redirects=True,
        )
        orgs_list = res.json
        logger.info(orgs_list)

        assert res.status_code == 200
        assert res.content_type == "application/json"
        assert isinstance(orgs_list, list)

    def test_get_all_with_two_params(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            query_string={"name": "Enter", "soft_deleted": False},
            headers=login,
            follow_redirects=True,
        )
        orgs_list = res.json
        logger.info(orgs_list)

        assert res.status_code == 200
        assert res.content_type == "application/json"
        assert isinstance(orgs_list, list)

    def test_get_all_with_bad_params(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            query_string={"deleted": False},
            headers=login,
            follow_redirects=True,
        )
        res_data = res.json

        assert res.status_code == 400
        assert res.content_type == "application/json"
        assert isinstance(res_data, dict)

    def test_get_by_id(self, client: FlaskClient, login: dict):
        org_id = 1
        res = client.get(
            f"{self.base_api}/{org_id}",
            headers=login,
            follow_redirects=True,
        )
        role_dict = res.json

        assert isinstance(role_dict, dict)
        assert "id" in role_dict
        assert "name" in role_dict
        assert "description" in role_dict
        assert "updated_date" in role_dict
        assert "created_date" in role_dict
        assert "deleted_date" in role_dict
        assert "soft_deleted" in role_dict


class TestOrganizationMembersRoute:
    base_api = f"/api/v1/organizations"

    def test_get_all(self, client: FlaskClient, login: dict):
        res = client.get(
            self.base_api,
            headers=login,
            follow_redirects=True,
        )
        members_list = res.json
        logger.info(members_list)

        assert isinstance(members_list, list)

    def test_get_all_with_params(self, client: FlaskClient, login: dict):
        org_id = 1
        res = client.get(
            f"{self.base_api}/{org_id}/members",
            query_string={"role": "ADMIN"},
            headers=login,
            follow_redirects=True,
        )
        members_list = res.json
        logger.info(members_list)

        assert isinstance(members_list, list)
        assert isinstance(members_list[0], dict)
        assert members_list[0]["role"] == OrganizationRoles.ADMIN.name

    def test_get_by_id(self, client: FlaskClient, login: dict):
        member_id = 1
        org_id = 1
        res = client.get(
            f"{self.base_api}/{org_id}/members/{member_id}",
            headers=login,
            follow_redirects=True,
        )
        member_dict = res.json
        logger.info(member_dict)

        assert isinstance(member_dict, dict)
        assert "id" in member_dict
        assert "user_id" in member_dict
        assert "organization_id" in member_dict
        assert "active" in member_dict
        assert "role" in member_dict
        assert "updated_date" in member_dict
        assert "created_date" in member_dict
        assert "deleted_date" in member_dict
        assert "soft_deleted" in member_dict

    def test_get_non_existing_member_by_id(self, client: FlaskClient, login: dict):
        member_id = 212
        org_id = 1
        res = client.get(
            f"{self.base_api}/{org_id}/members/{member_id}",
            headers=login,
            follow_redirects=True,
        )
        error = res.json

        assert res.status_code == 404
        assert isinstance(error, dict)

    def test_create(self, client: FlaskClient, login: dict):
        member_dict = {
            "user_id": 2,
            "active": False,
            "role": "OWNER",
        }
        org_id = 2
        res = client.post(
            f"{self.base_api}/{org_id}/members",
            json=member_dict,
            # headers={
            #     "Content-Type": "application/json",
            #     "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            # },
            headers=login,
            follow_redirects=True,
        )
        member = res.json
        logger.info(member_dict)

        assert res.status_code == 201
        assert isinstance(member, dict)

    def test_create_existing_member(self, client: FlaskClient, login: dict):
        member_dict = {
            "user_id": 2,
            "active": False,
            "role": "VIEWER",
        }
        org_id = 1
        res = client.post(
            f"{self.base_api}/{org_id}/members",
            json=member_dict,
            # headers={
            #     "Content-Type": "application/json",
            #     "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            # },
            headers=login,
            follow_redirects=True,
        )
        member = res.json
        logger.info(member_dict)

        assert res.status_code == 400
        assert isinstance(member, dict)

    def test_create_non_existing_org_and_user(self, client: FlaskClient, login: dict):
        member_dict = {
            "user_id": 33,
            "active": False,
            "role": "VIEWER",
        }
        org_id = 11
        res = client.post(
            f"{self.base_api}/{org_id}/members",
            json=member_dict,
            # headers={
            #     "Content-Type": "application/json",
            #     "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            # },
            headers=login,
            follow_redirects=True,
        )
        member = res.json
        logger.info(member_dict)

        assert res.status_code == 404
        assert isinstance(member, dict)

    def test_update(self, client: FlaskClient, login: dict):
        user_id = 2
        member_dict = {"active": False}
        org_id = 1
        res = client.put(
            f"{self.base_api}/{org_id}/members/{user_id}",
            json=member_dict,
            # headers={
            #     "Content-Type": "application/json",
            #     "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            # },
            headers=login,
            follow_redirects=True,
        )
        member = res.json

        assert res.status_code == 200
        assert isinstance(member, dict)
        assert member["user_id"] == 2
        assert member["organization_id"] == 1
        assert member["active"] == False

    def test_soft_delete(self, client: FlaskClient, login: dict):
        user_id = 2
        org_id = 2
        res = client.delete(
            f"{self.base_api}/{org_id}/members/{user_id}/soft",
            # headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
            headers=login,
            follow_redirects=True,
        )
        member = res.json

        assert res.status_code == 200
        assert isinstance(member, dict)
        assert member["user_id"] == 2
        assert member["organization_id"] == 2
        assert member["soft_deleted"] == True
        assert member["deleted_date"] != None

    def test_delete(self, client: FlaskClient, login: dict):
        user_id = 2
        org_id = 2
        res = client.delete(
            f"{self.base_api}/{org_id}/members/{user_id}",
            # headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
            headers=login,
            follow_redirects=True,
        )
        member = res.json

        assert res.status_code == 200
        assert isinstance(member, dict)
        assert member["user_id"] == 2
        assert member["organization_id"] == 2
