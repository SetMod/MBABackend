from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from flask import Flask
from typing import List
import pytest
import os


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
def create_users(db: SQLAlchemy):
    from app.models import Users, Roles

    user1 = Users()
    user1.first_name = "John"
    user1.second_name = "Doe"
    user1.username = "johndoe"
    user1.active = True
    user1.email = "john.doe@gmail.com"
    user1.phone = "+3801234567"
    user1.password = "s3cr3TP@@$w0Rd"
    user1.role = Roles.USER.name

    user2 = Users()
    user2.first_name = "John"
    user2.second_name = "Smith"
    user2.username = "johns"
    user2.active = True
    user2.email = "john.smith@gmail.com"
    user2.phone = "+380123456780123"
    user2.password = "Rx123@@$w0Rd"
    user2.role = Roles.ADMIN.name

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


@pytest.fixture(scope="session")
def create_organization_members(db: SQLAlchemy):
    from app.models import OrganizationMembers, OrganizationRoles

    member1 = OrganizationMembers()
    member1.user_id = 1
    member1.organization_id = 1
    member1.active = True
    member1.role = OrganizationRoles.OWNER

    member2 = OrganizationMembers()
    member2.user_id = 2
    member2.organization_id = 1
    member2.active = True
    member2.role = OrganizationRoles.ADMIN

    db.session.add(member1)
    db.session.add(member2)

    db.session.commit()

    return [member1, member2]


@pytest.fixture(scope="session")
def create_datasources(db: SQLAlchemy):
    from app.config import APP_UPLOAD_FOLDER
    from app.models import FileDatasources, DatasourceTypes

    datasource1 = FileDatasources()
    datasource1.name = "Transactions Datasource"
    datasource1.type = DatasourceTypes.FILE
    datasource1.file_path = APP_UPLOAD_FOLDER.joinpath("test.csv").resolve().as_posix()
    datasource1.creator_id = 1

    db.session.add(datasource1)

    db.session.commit()

    return [datasource1]


@pytest.fixture(scope="session")
def create_reports(db: SQLAlchemy):
    from app.models import GenericReports, ReportTypes

    report1 = GenericReports()
    report1.name = "Transactions Report"
    report1.type = ReportTypes.GENERIC
    report1.creator_id = 1

    db.session.add(report1)

    db.session.commit()

    return [report1]


@pytest.fixture(scope="session")
def create_visualizations(db: SQLAlchemy):
    from app.config import APP_VISUALIZATIONS_FOLDER
    from app.models import (
        FileVisualizations,
        DataVisualizations,
        VisualizationTypes,
    )

    visualization1 = DataVisualizations()
    visualization1.name = "Transactions visualization 1"
    visualization1.type = VisualizationTypes.DATA_POINTS
    visualization1.data_points = "[1,6,2,9,2]"
    visualization1.file_path = (
        APP_VISUALIZATIONS_FOLDER.joinpath("viz_1.png").resolve().as_posix()
    )
    visualization1.report_id = 1

    visualization2 = FileVisualizations()
    visualization2.name = "Transactions visualization 2"
    visualization2.type = VisualizationTypes.FILE
    visualization2.file_path = (
        APP_VISUALIZATIONS_FOLDER.joinpath("viz_2.png").resolve().as_posix()
    )
    visualization2.report_id = 1

    db.session.add(visualization1)
    db.session.add(visualization2)

    db.session.commit()

    return [visualization1]


@pytest.fixture(scope="session", autouse=True)
def create_models(
    create_users,
    create_organizations,
    create_organization_members,
    create_datasources,
    create_reports,
    create_visualizations,
):
    pass


@pytest.fixture(scope="session")
def login(client: FlaskClient):
    from app.logger import logger

    user = {"username": "johndoe", "password": "s3cr3TP@@$w0Rd"}
    res = client.post(
        "/api/v1/users/auth/login",
        json=user,
    )
    logger.info(res.json)
    logger.info(res.headers)

    access_token = res.json["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    return headers


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


@pytest.fixture(scope="module")
def organization_members_schema():
    from app.schemas import OrganizationMembersSchema

    organization_members_schema = OrganizationMembersSchema()
    return organization_members_schema


@pytest.fixture(scope="module")
def organization_members_service():
    from app.services import OrganizationMembersService

    organization_members_service = OrganizationMembersService()
    return organization_members_service


@pytest.fixture(scope="module")
def datasources_schema():
    from app.schemas import DatasourcesSchema

    datasources_schema = DatasourcesSchema()
    return datasources_schema


@pytest.fixture(scope="module")
def datasources_service():
    from app.services import DatasourcesService

    datasources_service = DatasourcesService()
    return datasources_service


@pytest.fixture(scope="module")
def reports_schema():
    from app.schemas import ReportsSchema

    reports_schema = ReportsSchema()
    return reports_schema


@pytest.fixture(scope="module")
def reports_service():
    from app.services import ReportsService

    reports_service = ReportsService()
    return reports_service
