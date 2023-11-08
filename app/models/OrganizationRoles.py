from app.models import GenericModel
from app.init import db, ma


class OrganizationRoles(db.Model, GenericModel):
    __tablename__ = "organization_roles"

    name = db.Column("name", db.String(50), unique=True, nullable=False)

    description = db.Column("description", db.Text, nullable=False)

    def __repr__(self):
        return f"<OrganizationRole(id={self.id},name={self.name}>"


class OrganizationRolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrganizationRoles
