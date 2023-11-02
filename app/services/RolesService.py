from marshmallow import ValidationError
from app.models.RolesModel import Roles, RolesSchema
from app import db


class RolesService:

    def __init__(self) -> None:
        self.roles_schema = RolesSchema()

    def get_all_roles(self, dump: bool = True):
        try:
            roles = db.session.query(Roles).all()

            if len(roles) > 0:
                return self.roles_schema.dump(roles, many=True) if dump else roles
            else:
                return 'Roles not found'
        except Exception as err:
            print(err)
            return 'Failed to get roles'

    def get_role_by_id(self, id: int, dump: bool = True):
        try:
            role = db.session.query(Roles).where(Roles.role_id == id).first()

            if isinstance(role, Roles):
                return self.roles_schema.dump(role) if dump else role
            else:
                return 'Role not found'
        except Exception as err:
            print(err)
            return 'Failed to get role'

    def get_role_by_name(self, name: str, dump: bool = True):
        try:
            role = db.session.query(Roles).filter_by(role_name=name).first()

            if isinstance(role, Roles):
                return self.roles_schema.dump(role) if dump else role
            else:
                return 'Role not found'
        except Exception as err:
            print(err)
            return 'Failed to get role'

    def create_role(self, new_role: Roles, dump: bool = True):
        role = self.get_role_by_name(new_role.role_name, dump=False)
        if isinstance(role, Roles):
            return 'Role already exists'

        try:
            db.session.add(new_role)
            db.session.commit()
            return self.roles_schema.dump(new_role) if dump else new_role
        except Exception as err:
            print(err)
            return 'Failed to create a role'

    def update_role(self, role_id: int, updated_role: Roles, dump: bool = True):
        role = self.get_role_by_id(role_id, dump=False)

        if not isinstance(role, Roles):
            return role

        existing_role = self.get_role_by_name(
            updated_role.role_name, dump=False)

        if isinstance(existing_role, Roles):
            return f'Role with name "{updated_role.role_name}" already exists'

        role.role_name = updated_role.role_name
        role.role_description = updated_role.role_description
        try:
            db.session.commit()
            return self.roles_schema.dump(role) if dump else role
        except Exception as err:
            print(err)
            return 'Failed to update a role'

    def delete_role(self, role_id: int, dump: bool = True):
        role = self.get_role_by_id(role_id, dump=False)

        if not isinstance(role, Roles):
            return role

        try:
            db.session.delete(role)
            db.session.commit()
            return self.roles_schema.dump(role) if dump else role
        except Exception as err:
            print(err)
            return 'Failed to delete a role'

    def map_role(self, role_dict: dict):
        try:
            role = self.roles_schema.load(role_dict)
            role_name = role_dict['role_name']
            role_description = role_dict['role_description']
            role = Roles(role_name=role_name,
                         role_description=role_description)
            return role
        except ValidationError as err:
            return err.messages
