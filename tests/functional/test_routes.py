from flask.testing import FlaskClient
from app.logger import logger
from app.models import OrganizationRoles, Roles


class TestUsersRoute:
    base_api = "/api/v1/users"

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

    def test_get_all_without_login(self, client: FlaskClient):
        response = client.get(f"{self.base_api}", follow_redirects=True)
        error = response.json
        logger.info(error)

        assert response.status_code == 401
        assert isinstance(error, dict)
        assert (
            error["msg"]
            == 'Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token_cookie")'
        )

    def test_login_again(self, client: FlaskClient):
        user = {"username": "johndoe", "password": "s3cr3TP@@$w0Rd"}
        res = client.post(
            f"{self.base_api}/auth/login",
            json=user,
        )
        logger.info(res.json)
        logger.info(res.headers)

    def test_get_all(self, client: FlaskClient):
        response = client.get(f"{self.base_api}", follow_redirects=True)
        users_list = response.json
        logger.info(users_list)

        assert isinstance(users_list, list)

    def test_get_all_with_params(self, client: FlaskClient):
        response = client.get(
            f"{self.base_api}?username=johndoe", follow_redirects=True
        )
        users_list = response.json
        logger.info(users_list)

        assert isinstance(users_list, list)

    def test_get_all_with_two_params(self, client: FlaskClient):
        response = client.get(
            f"{self.base_api}?soft_deleted=false&active=true", follow_redirects=True
        )
        roles_list = response.json
        logger.info(roles_list)

        assert isinstance(roles_list, list)

    def test_get_all_with_bad_params(self, client: FlaskClient):
        response = client.get(f"{self.base_api}?deleted=true", follow_redirects=True)
        res_data = response.json

        assert response.content_type == "application/json"
        assert response.status_code == 400
        assert isinstance(res_data, dict)

    def test_get_by_id(self, client: FlaskClient):
        user_id = 1
        response = client.get(f"{self.base_api}/{user_id}")
        role_dict = response.json

        assert isinstance(role_dict, dict)
        assert "id" in role_dict
        assert "username" in role_dict
        assert "updated_date" in role_dict
        assert "created_date" in role_dict
        assert "deleted_date" in role_dict
        assert "soft_deleted" in role_dict

    def test_get_organizations(self, client: FlaskClient):
        user_id = 1
        response = client.get(f"{self.base_api}/{user_id}/organizations")
        organizations_list = response.json

        assert isinstance(organizations_list, list)

    def test_get_reports(self, client: FlaskClient):
        user_id = 1
        response = client.get(f"{self.base_api}/{user_id}/reports")
        reports_list = response.json

        assert isinstance(reports_list, list)

    def test_get_datasources(self, client: FlaskClient):
        user_id = 1
        response = client.get(f"{self.base_api}/{user_id}/datasources")
        datasources_list = response.json

        assert isinstance(datasources_list, list)

    def test_create(self, client: FlaskClient):
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
        response = client.post(
            f"{self.base_api}/",
            json=user_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            },
        )
        user = response.json
        logger.info(user)

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bobross"
        assert user["role"] == Roles.ADMIN.name

    def test_update(self, client: FlaskClient):
        user_id = 3
        user_dict = {"username": "bob_ross", "password": "Nk23@jk983Jkr"}
        response = client.put(
            f"{self.base_api}/{user_id}",
            json=user_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            },
        )
        user = response.json

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bob_ross"

    def test_soft_delete(self, client: FlaskClient):
        user_id = 3
        response = client.delete(
            f"{self.base_api}/{user_id}/soft",
            headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
        )
        user = response.json

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bob_ross"
        assert user["soft_deleted"] == True
        assert user["deleted_date"] != None

    def test_delete(self, client: FlaskClient):
        user_id = 3
        response = client.delete(
            f"{self.base_api}/{user_id}",
            headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
        )
        user = response.json

        assert isinstance(user, dict)
        assert user["id"] == 3
        assert user["username"] == "bob_ross"


class TestOrganizationsRoute:
    base_api = "/api/v1/organizations"

    def test_get_all(self, client: FlaskClient):
        response = client.get(self.base_api, follow_redirects=True)
        orgs_list = response.json
        logger.info(orgs_list)

        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert isinstance(orgs_list, list)

    def test_get_all_with_params(self, client: FlaskClient):
        response = client.get(f"{self.base_api}?name=LocalStore", follow_redirects=True)
        orgs_list = response.json
        logger.info(orgs_list)

        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert isinstance(orgs_list, list)

    def test_get_all_with_two_params(self, client: FlaskClient):
        response = client.get(
            f"{self.base_api}?name=Enter&soft_deleted=False", follow_redirects=True
        )
        orgs_list = response.json
        logger.info(orgs_list)

        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert isinstance(orgs_list, list)

    def test_get_all_with_bad_params(self, client: FlaskClient):
        response = client.get(f"{self.base_api}?deleted=True", follow_redirects=True)
        res_data = response.json

        assert response.status_code == 400
        assert response.content_type == "application/json"
        assert isinstance(res_data, dict)

    def test_get_by_id(self, client: FlaskClient):
        org_id = 1
        response = client.get(f"{self.base_api}/{org_id}")
        role_dict = response.json

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

    def test_get_all(self, client: FlaskClient):
        response = client.get(self.base_api, follow_redirects=True)
        members_list = response.json
        logger.info(members_list)

        assert isinstance(members_list, list)

    def test_get_all_with_params(self, client: FlaskClient):
        org_id = 1
        response = client.get(
            f"{self.base_api}/{org_id}/members/?role=ADMIN", follow_redirects=True
        )
        members_list = response.json
        logger.info(members_list)

        assert isinstance(members_list, list)
        assert isinstance(members_list[0], dict)
        assert members_list[0]["role"] == OrganizationRoles.ADMIN.name

    def test_get_by_id(self, client: FlaskClient):
        member_id = 1
        org_id = 1
        response = client.get(f"{self.base_api}/{org_id}/members/{member_id}")
        member_dict = response.json
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

    def test_get_non_existing_member_by_id(self, client: FlaskClient):
        member_id = 212
        org_id = 1
        response = client.get(f"{self.base_api}/{org_id}/members/{member_id}")
        error = response.json

        assert response.status_code == 404
        assert isinstance(error, dict)

    def test_create(self, client: FlaskClient):
        member_dict = {
            "user_id": 2,
            "active": False,
            "role": "OWNER",
        }
        org_id = 2
        response = client.post(
            f"{self.base_api}/{org_id}/members/",
            json=member_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            },
        )
        member = response.json
        logger.info(member_dict)

        assert response.status_code == 201
        assert isinstance(member, dict)

    def test_create_existing_member(self, client: FlaskClient):
        member_dict = {
            "user_id": 2,
            "active": False,
            "role": "VIEWER",
        }
        org_id = 1
        response = client.post(
            f"{self.base_api}/{org_id}/members/",
            json=member_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            },
        )
        member = response.json
        logger.info(member_dict)

        assert response.status_code == 400
        assert isinstance(member, dict)

    def test_create_non_existing_org_and_user(self, client: FlaskClient):
        member_dict = {
            "user_id": 33,
            "active": False,
            "role": "VIEWER",
        }
        org_id = 11
        response = client.post(
            f"{self.base_api}/{org_id}/members/",
            json=member_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            },
        )
        member = response.json
        logger.info(member_dict)

        assert response.status_code == 404
        assert isinstance(member, dict)

    def test_update(self, client: FlaskClient):
        user_id = 2
        member_dict = {"active": False}
        org_id = 1
        response = client.put(
            f"{self.base_api}/{org_id}/members/{user_id}",
            json=member_dict,
            headers={
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value,
            },
        )
        member = response.json

        assert response.status_code == 200
        assert isinstance(member, dict)
        assert member["user_id"] == 2
        assert member["organization_id"] == 1
        assert member["active"] == False

    def test_soft_delete(self, client: FlaskClient):
        user_id = 2
        org_id = 2
        response = client.delete(
            f"{self.base_api}/{org_id}/members/{user_id}/soft",
            headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
        )
        member = response.json

        assert response.status_code == 200
        assert isinstance(member, dict)
        assert member["user_id"] == 2
        assert member["organization_id"] == 2
        assert member["soft_deleted"] == True
        assert member["deleted_date"] != None

    def test_delete(self, client: FlaskClient):
        user_id = 2
        org_id = 2
        response = client.delete(
            f"{self.base_api}/{org_id}/members/{user_id}",
            headers={"X-CSRF-TOKEN": client.get_cookie("csrf_access_token").value},
        )
        member = response.json

        assert response.status_code == 200
        assert isinstance(member, dict)
        assert member["user_id"] == 2
        assert member["organization_id"] == 2
