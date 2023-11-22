from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from flask import Flask
from typing import List
import pytest
import os

from app.logger import logger


os.environ["APP_DOTENV_PATH"] = ".env.test"


@pytest.fixture(scope="session")
def app():
    from app import create_app

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture(scope="session")
def db(app: Flask):
    from app.db import db

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db


@pytest.fixture(scope="session")
def client(app: Flask):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def create_roles(db: SQLAlchemy):
    from app.models import Roles

    user_role = Roles()
    user_role.name = "User"
    user_role.description = "Roles for users"

    admin_role = Roles()
    admin_role.name = "Admin"
    admin_role.description = "Roles for admins"

    db.session.add(user_role)
    db.session.add(admin_role)

    db.session.commit()

    return [user_role, admin_role]


@pytest.fixture(scope="session")
def create_users(db: SQLAlchemy):
    from app.models import Users

    user1 = Users()
    user1.first_name = "John"
    user1.second_name = "Doe"
    user1.username = "johndoe"
    user1.active = True
    user1.email = "john.doe@gmail.com"
    user1.phone = "+3801234567"
    user1.password = "s3cr3TP@@$w0Rd"
    user1.role_id = 1

    user2 = Users()
    user2.first_name = "John"
    user2.second_name = "Smith"
    user2.username = "johns"
    user2.active = True
    user2.email = "john.smith@gmail.com"
    user2.phone = "+380123456780123"
    user2.password = "Rx123@@$w0Rd"
    user2.role_id = 2

    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    return [user1, user2]


@pytest.fixture(scope="session")
def create_organizations(db: SQLAlchemy):
    from app.models import Organizations

    org1 = Organizations()
    org1.name = "LocalStore"
    org1.description = "LocalStore organization for local stores"
    org1.email = "business@localstore.com"
    org1.phone = "+123123123123"

    org2 = Organizations()
    org2.name = "Enter"
    org2.description = "Enter organization for new businesses"
    org2.email = "support@enter.com"
    org2.phone = "+123123123124"
    db.session.add(org1)
    db.session.add(org2)

    db.session.commit()

    return [org1, org2]


@pytest.fixture(scope="session", autouse=True)
def create_models(create_roles, create_users, create_organizations):
    pass


@pytest.fixture(scope="session", autouse=True)
def login(create_users, client: FlaskClient):
    user = {"username": "johndoe", "password": "s3cr3TP@@$w0Rd"}
    res = client.post(
        "/api/v1/users/auth/login",
        json=user,
    )
    logger.info("Login response data:")
    logger.info(res.json)
    logger.info(res.headers)


@pytest.fixture(scope="module")
def roles_schema():
    from app.schemas import RolesSchema

    roles_schema = RolesSchema()
    return roles_schema


@pytest.fixture(scope="module")
def roles_service():
    from app.services import RolesService

    roles_service = RolesService()
    return roles_service


@pytest.fixture(scope="module")
def users_schema():
    from app.schemas import UsersSchema

    users_schema = UsersSchema()
    return users_schema


@pytest.fixture(scope="module")
def users_service():
    from app.services import UsersService

    users_service = UsersService()
    return users_service


@pytest.fixture(scope="module")
def organizations_schema():
    from app.schemas import OrganizationsSchema

    organizations_schema = OrganizationsSchema()
    return organizations_schema


@pytest.fixture(scope="module")
def organizations_service():
    from app.services import OrganizationsService

    organizations_service = OrganizationsService()
    return organizations_service
