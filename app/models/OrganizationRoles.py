from app import db, ma


class OrganizationRoles(db.Model):
    __tablename__ = "organization_roles"

    id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(50), unique=True, nullable=False)

    description = db.Column("description", db.Text, nullable=False)

    def __repr__(self):
        return f"<OrganizationRole(id={self.id},name={self.name}>"


class OrganizationRolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrganizationRoles
