from app.models import GenericModel
from app.init import db, ma


class Roles(db.Model, GenericModel):
    __tablename__ = "roles"

    name = db.Column("name", db.String(50), unique=True, nullable=False)

    description = db.Column("description", db.Text, nullable=False)

    def __repr__(self):
        return f"<Role(id={self.id},name={self.name},description={self.description})>"


class RolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
