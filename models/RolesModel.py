from app import db, ma


class Roles(db.Model):
    __tablename__ = "roles"

    role_id = db.Column(
        'role_id',
        db.Integer,
        primary_key=True)

    role_name = db.Column(
        'role_name',
        db.String(50),
        unique=True,
        nullable=False)

    role_description = db.Column(
        'role_description',
        db.Text,
        nullable=False)

    def __repr__(self):
        return f'<Role(role_id={self.role_id},role_name={self.role_name},role_description={self.role_description})>'


class RolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
