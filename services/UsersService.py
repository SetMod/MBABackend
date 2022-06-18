from marshmallow import ValidationError
from models.FilesModel import FilesSchema
from models.OrganizationsModel import OrganizationsSchema
from models.ReportsModel import ReportsSchema
from models.UsersModel import Users, UsersSchema
from services.RolesService import RolesService
from services.UsersOrganizationsService import UsersOrganizationsService
from app import db


class UsersService():

    def __init__(self) -> None:
        self.roles_service = RolesService()
        self.reports_schema = ReportsSchema()
        self.organizations_schema = OrganizationsSchema()
        self.users_organizations_service = UsersOrganizationsService()
        self.users_schema = UsersSchema()
        self.files_schema = FilesSchema()

    def get_all_users(self, dump: bool = True):
        users = db.session.query(Users).all()

        if len(users) > 0:
            return self.users_schema.dump(users, many=True) if dump else users
        else:
            return None

    def get_user_by_id(self, user_id: int, dump: bool = True):
        user = db.session.query(Users).where(Users.user_id == user_id).first()

        if isinstance(user, Users):
            return self.users_schema.dump(user) if dump else user
        else:
            return None

    def get_user_by_credentials(self, user_username: str, user_password: str, dump: bool = True):
        user = db.session.query(Users).where(
            Users.user_username == user_username, Users.user_password == user_password).first()

        if isinstance(user, Users):
            return self.users_schema.dump(user) if dump else user
        else:
            return None

    def get_users_by_role(self, role_name: str, dump: bool = True):
        role = self.roles_service.get_role_by_name(role_name, dump=False)

        if role is not None and len(role.role_users) > 0:
            return self.users_schema.dump(role.role_users, many=True) if dump else role.role_users
        else:
            return None

    def get_user_organizations(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if user is not None and len(user.user_organizations) > 0:
            return self.organizations_schema.dump(user.user_organizations, many=True) if dump else user.user_organizations
        else:
            return None

    def get_user_files(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if user is not None and len(user.user_files) > 0:
            return self.files_schema.dump(user.user_files, many=True) if dump else user.user_files
        else:
            return None

    def get_user_reports(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if user is not None and len(user.user_reports) > 0:
            return self.reports_schema.dump(user.user_reports, many=True) if dump else user.user_reports
        else:
            return None

    def create_user(self, user: Users, dump: bool = True):
        try:
            db.session.add(user)
            db.session.commit()
            return self.users_schema.dump(user) if dump else user
        except Exception:
            return None

    def update_user(self, user_id: int, updated_user: Users, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        try:
            if isinstance(user, Users):
                user.user_first_name = updated_user.user_first_name
                user.user_second_name = updated_user.user_second_name
                user.user_email = updated_user.user_email
                user.user_phone = updated_user.user_phone
                user.user_username = updated_user.user_username
                user.user_password = updated_user.user_password
                user.role_id = updated_user.role_id
                db.session.commit()
                return self.users_schema.dump(user) if dump else user
            else:
                return None
        except Exception:
            return None

    def delete_user(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        try:
            if isinstance(user, Users):
                db.session.delete(user)
                db.session.commit()
                return self.users_schema.dump(user) if dump else user
            else:
                return None
        except Exception:
            return None

    def map_user(self, user_dict: dict):
        try:
            user = self.users_schema.load(user_dict)
            user_first_name = user_dict['user_first_name']
            user_second_name = user_dict['user_second_name']
            user_email = user_dict['user_email']
            user_phone = user_dict['user_phone']
            user_username = user_dict['user_username']
            user_password = user_dict['user_password']
            role_id = user_dict['role_id']
            user = Users(user_first_name=user_first_name, user_second_name=user_second_name, user_email=user_email, user_phone=user_phone,
                         user_username=user_username, user_password=user_password, role_id=role_id)
            return user
        except ValidationError as err:
            return err.messages
