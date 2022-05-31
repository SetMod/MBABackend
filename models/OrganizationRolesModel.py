from app import db, ma


class OrganizationRoles(db.Model):
    __tablename__ = "organization_roles"

    organization_role_id = db.Column(
        'organization_role_id',
        db.Integer,
        primary_key=True)

    organization_role_name = db.Column(
        'organization_role_name',
        db.String(50),
        unique=True,
        nullable=False)

    organization_role_description = db.Column(
        'organization_role_description',
        db.Text,
        nullable=False)


class OrganizationRolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = OrganizationRoles
