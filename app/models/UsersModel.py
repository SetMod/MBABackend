from datetime import datetime
from app import db, ma


class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        'user_id',
        db.Integer,
        primary_key=True)

    user_first_name = db.Column(
        'user_first_name',
        db.String(100),
        nullable=False)

    user_second_name = db.Column(
        'user_second_name',
        db.String(100),
        nullable=False)

    user_email = db.Column(
        'user_email',
        db.String(255),
        unique=True,
        nullable=False)

    user_phone = db.Column(
        'user_phone',
        db.String(18),
        unique=True)

    user_username = db.Column(
        'user_username',
        db.String(50),
        unique=True,
        nullable=False)

    user_password = db.Column(
        'user_password',
        db.String(50),
        nullable=False)

    user_create_date = db.Column(
        'user_create_date',
        db.DateTime,
        default=datetime.utcnow)

    role_id = db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey("roles.role_id"),
        nullable=False)

    user_role = db.relationship("Roles", backref="role_users")
    user_organizations = db.relationship(
        "UsersOrganizations", backref="user", cascade='save-update, merge, delete')
    # user_organizations = db.relationship("Organizations", secondary=users_organizations_table,
    #                                      backref="organization_users", cascade='save-update, merge, delete')

    def __repr__(self):
        return f'<User(user_id={self.user_id},user_first_name={self.user_first_name},user_second_name={self.user_second_name},user_email={self.user_email},user_username={self.user_username},user_create_date={self.user_create_date},role_id={self.role_id})>'


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True

    # role = ma.Nested(RolesSchema)
    # user_role = ma.HyperlinkRelated('roles.get_role_by_id', 'role_id')
    # role_id = ma.auto_field()
