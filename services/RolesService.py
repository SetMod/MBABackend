from marshmallow import ValidationError
from models.RolesModel import Roles, RolesSchema
from app import db


class RolesService:

    def __init__(self) -> None:
        self.roles_schema = RolesSchema()

    def get_all_roles(self, dump: bool = True):
        roles = db.session.query(Roles).all()

        if len(roles) > 0:
            return self.roles_schema.dump(roles, many=True) if dump else roles
        else:
            return None

    def get_role_by_id(self, id: int, dump: bool = True):
        role = db.session.query(Roles).where(Roles.role_id == id).first()

        if isinstance(role, Roles):
            return self.roles_schema.dump(role) if dump else role
        else:
            return None

    def get_role_by_name(self, name: str, dump: bool = True) -> Roles:
        role = db.session.query(Roles).filter_by(role_name=name).first()
        return self.roles_schema.dump(role) if dump else role

    def create_role(self, role: Roles, dump: bool = True):
        try:
            db.session.add(role)
            db.session.commit()
            return self.roles_schema.dump(role) if dump else role
        except Exception:
            return None

    def update_role(self, role_id: int, updated_role: Roles, dump: bool = True):
        role = self.get_role_by_id(role_id, dump=False)

        try:
            if isinstance(role, Roles):
                role.role_name = updated_role.role_name
                role.role_description = updated_role.role_description
                db.session.commit()
                return self.roles_schema.dump(role) if dump else role
            else:
                return None
        except Exception:
            return None

    def delete_role(self, role_id: int, dump: bool = True):
        role = self.get_role_by_id(role_id, dump=False)

        try:
            if isinstance(role, Roles):
                db.session.delete(role)
                db.session.commit()
                return self.roles_schema.dump(role) if dump else role
            else:
                return None
        except Exception:
            return None

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
