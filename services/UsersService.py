from marshmallow import ValidationError
from models.FilesModel import FilesSchema
from models.OrganizationsModel import OrganizationsSchema
from models.ReportsModel import ReportsSchema
from models.RolesModel import RolesSchema
from models.UsersModel import Users, UsersSchema
from services.OrganizationRolesService import OrganizationRolesService
from services.RolesService import RolesService
from services.UsersOrganizationsService import UsersOrganizationsService
from app import db


class UsersService():

    def __init__(self) -> None:
        self.users_organizations_service = UsersOrganizationsService()
        self.organization_roles_service = OrganizationRolesService()
        self.roles_service = RolesService()
        self.reports_schema = ReportsSchema()
        self.organizations_schema = OrganizationsSchema()
        self.users_schema = UsersSchema()
        self.roles_schema = RolesSchema()
        self.files_schema = FilesSchema()

    def get_all_users(self, dump: bool = True):
        try:
            users = db.session.query(Users).all()

            if len(users) > 0:
                return self.users_schema.dump(users, many=True) if dump else users
            else:
                return 'Users not found'
        except Exception as err:
            print(err)
            return 'Failed to get users'

    def get_user_by_id(self, user_id: int, dump: bool = True):
        try:
            user = db.session.query(Users).where(
                Users.user_id == user_id).first()

            if isinstance(user, Users):
                return self.users_schema.dump(user) if dump else user
            else:
                return 'User not found'
        except Exception as err:
            print(err)
            return 'Failed to get user'

    def get_user_role(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)
        if isinstance(user, str):
            return user

        return self.roles_schema.dump(user.user_role) if dump else user.user_role

    def get_user_by_credentials(self, user_username: str, user_password: str, dump: bool = True):
        try:
            user = db.session.query(Users).where(
                Users.user_username == user_username, Users.user_password == user_password).first()

            if isinstance(user, Users):
                return self.users_schema.dump(user) if dump else user
            else:
                return 'User not found'
        except Exception as err:
            print(err)
            return 'Failed to get user'

    def get_users_by_role(self, role_name: str, dump: bool = True):
        role = self.roles_service.get_role_by_name(role_name, dump=False)

        if isinstance(role, str):
            return role

        if len(role.role_users) > 0:
            return self.users_schema.dump(role.role_users, many=True) if dump else role.role_users
        else:
            return 'Users not found'

    def get_user_organizations(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if isinstance(user, str):
            self.o
            return user

        for organization in user.user_organizations:
            print(organization)

        if len(user.user_organizations) > 0:
            return self.organizations_schema.dump(user.user_organizations, many=True) if dump else user.user_organizations
        else:
            return 'No user organizations was found'

    def get_user_reports(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if isinstance(user, str):
            return user

        if len(user.user_reports) > 0:
            return self.reports_schema.dump(user.user_reports, many=True) if dump else user.user_reports
        else:
            return 'No user reports was found'

    def get_user_files(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if isinstance(user, str):
            return user

        if len(user.user_files) > 0:
            return self.files_schema.dump(user.user_files, many=True) if dump else user.user_files
        else:
            return 'No user files was found'

    def get_user_by_username(self, username: str, dump: bool = True):
        try:
            user = db.session.query(Users).where(
                Users.user_username == username).first()

            if isinstance(user, Users):
                return self.users_schema.dump(user) if dump else user
            else:
                return 'User not found'
        except Exception as err:
            print(err)
            return 'Failed to get user'

    def get_user_by_email(self, email: str, dump: bool = True):
        try:
            user = db.session.query(Users).where(
                Users.user_email == email).first()

            if isinstance(user, Users):
                return self.users_schema.dump(user) if dump else user
            else:
                return 'User not found'
        except Exception as err:
            print(err)
            return 'Failed to get user'

    def get_user_by_phone(self, phone: str, dump: bool = True):
        try:
            user = db.session.query(Users).where(
                Users.user_phone == phone).first()

            if isinstance(user, Users):
                return self.users_schema.dump(user) if dump else user
            else:
                return 'User not found'
        except Exception as err:
            print(err)
            return 'Failed to get user'

    def create_user(self, new_user: Users, dump: bool = True):
        existing_user = self.get_user_by_username(
            new_user.user_username, dump=False)
        if isinstance(existing_user, Users):
            return f'Username is already taken'

        existing_user = self.get_user_by_email(new_user.user_email, dump=False)
        if isinstance(existing_user, Users):
            return 'Email is already taken'

        if new_user.user_phone:
            existing_user = self.get_user_by_phone(
                new_user.user_phone, dump=False)
            if isinstance(existing_user, Users):
                return f'Phone is already taken'

        try:
            db.session.add(new_user)
            db.session.commit()
            return self.users_schema.dump(new_user) if dump else new_user
        except Exception as err:
            print(err)
            return 'Failed to create a user'

    def update_user(self, user_id: int, updated_user: Users, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)

        if not isinstance(user, Users):
            return user

        existing_user = self.get_user_by_username(
            updated_user.user_username, dump=False)
        if isinstance(existing_user, Users):
            return f'Username is already taken'

        existing_user = self.get_user_by_email(
            updated_user.user_email, dump=False)
        if isinstance(existing_user, Users):
            return 'Email is already taken'

        if updated_user.user_phone:
            existing_user = self.get_user_by_phone(
                updated_user.user_phone, dump=False)
            if isinstance(existing_user, Users):
                return f'Phone is already taken'

        user.user_first_name = updated_user.user_first_name
        user.user_second_name = updated_user.user_second_name
        user.user_email = updated_user.user_email
        user.user_phone = updated_user.user_phone
        user.user_username = updated_user.user_username
        user.user_password = updated_user.user_password
        user.role_id = updated_user.role_id
        try:
            db.session.commit()
            return self.users_schema.dump(user) if dump else user
        except Exception as err:
            print(err)
            return 'Failed to create a user'

    def delete_user(self, user_id: int, dump: bool = True):
        user = self.get_user_by_id(user_id, dump=False)
        if not isinstance(user, Users):
            return user

        try:
            db.session.delete(user)
            db.session.commit()
            return self.users_schema.dump(user) if dump else user
        except Exception as err:
            print(err)
            return 'Failed to delete a user'

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
