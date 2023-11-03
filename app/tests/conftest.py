import pytest
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

UPLOAD_FOLDER = 'D:\\test_data'
ANALYZES_UPLOAD_FOLDER = 'D:\\test_data\\analyzes'
VISUALIZATIONS_UPLOAD_FOLDER = 'D:\\test_data\\visualizations'
ALLOWED_EXTENSIONS = {'csv'}
os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_ENV'] = 'development'


@pytest.fixture(scope='session')
def app(request):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../test_database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "s3crEt"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
    CORS(app)

    return app


@pytest.fixture(scope='session')
def db(app: Flask):
    db = SQLAlchemy(app)
    return db


@pytest.fixture(scope='session')
def ma(app: Flask):
    ma = Marshmallow(app)
    return ma


@pytest.fixture(scope='session')
def client(app: Flask):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
def roles(request, db):
    class Roles(db.Model):
        __tablename__ = "roles"
        role_id = db.Column('role_id', db.Integer, primary_key=True)
        name = db.Column('name', db.String(50),
                              unique=True, nullable=False)
        description = db.Column(
            'description', db.Text, nullable=False)

        def __repr__(self):
            return f'<Role(role_id={self.role_id},name={self.name},description={self.description})>'
    # Create tables
    db.create_all()

    @request.addfinalizer
    def drop_tables():
        db.drop_all()

    return Roles


@pytest.fixture(scope='module')
def roles_schema(ma, roles):
    class RolesSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = roles
    roles_schema = RolesSchema()
    return roles_schema


# @pytest.fixture(scope='module')
# def users(request, db):
#     class Users(db.Model):
#         __tablename__ = "users"

#         user_id = db.Column('user_id', db.Integer, primary_key=True)
#         first_name = db.Column(
#             'first_name', db.String(100), nullable=False)
#         second_name = db.Column(
#             'second_name', db.String(100), nullable=False)
#         email = db.Column('email', db.String(
#             255), unique=True, nullable=False)
#         phone = db.Column('phone', db.String(18), unique=True)
#         username = db.Column('username', db.String(
#             50), unique=True, nullable=False)
#         password = db.Column(
#             'password', db.String(50), nullable=False)
#         create_date = db.Column(
#             'create_date', db.DateTime, default=datetime.utcnow)
#         role_id = db.Column('role_id', db.Integer, db.ForeignKey(
#             "roles.role_id"), nullable=False)

#         user_role = db.relationship("Roles", backref="role_users")
#         user_organizations = db.relationship(
#             "UsersOrganizations", backref="user", cascade='save-update, merge, delete')

#         def __repr__(self):
#             return f'<User(user_id={self.user_id},first_name={self.first_name},second_name={self.second_name},email={self.email},username={self.username},create_date={self.create_date},role_id={self.role_id})>'

#     # Create tables
#     db.create_all()

#     @request.addfinalizer
#     def drop_tables():
#         db.drop_all()

#     return Users


# @pytest.fixture(scope='module')
# def users_schema(ma, users):
#     class UsersSchema(ma.SQLAlchemyAutoSchema):
#         class Meta:
#             model = users
#             include_fk = True
#     return UsersSchema
