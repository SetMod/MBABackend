from app.models import GenericModel
from app.init import db, ma


class Users(db.Model, GenericModel):
    __tablename__ = "users"

    first_name = db.Column("first_name", db.String(100), nullable=False)

    second_name = db.Column("second_name", db.String(100), nullable=False)

    email = db.Column("email", db.String(255), unique=True, nullable=False)

    phone = db.Column("phone", db.String(18), unique=True)

    username = db.Column("username", db.String(50), unique=True, nullable=False)

    password = db.Column("password", db.String(50), nullable=False)

    role_id = db.Column(
        "role_id", db.Integer, db.ForeignKey("roles.id"), nullable=False
    )

    user_role = db.relationship("Roles", backref="role_users")
    user_organizations = db.relationship(
        "UsersOrganizations", backref="user", cascade="save-update, merge, delete"
    )
    # user_organizations = db.relationship("Organizations", secondary=users_organizations_table,
    #                                      backref="members", cascade='save-update, merge, delete')

    def __repr__(self):
        return f"<User(id={self.id},first_name={self.first_name},second_name={self.second_name},email={self.email},username={self.username},create_date={self.create_date},role_id={self.role_id})>"


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True

    # role = ma.Nested(RolesSchema)
    # user_role = ma.HyperlinkRelated('roles.get_role_by_id', 'role_id')
    # role_id = ma.auto_field()
