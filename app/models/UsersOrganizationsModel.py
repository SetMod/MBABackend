from app import db, ma


class UsersOrganizations(db.Model):
    __tablename__ = "users_organizations"

    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey("users.user_id"),
        primary_key=True)

    organization_id = db.Column(
        'organization_id',
        db.Integer,
        db.ForeignKey("organizations.organization_id"),
        primary_key=True)

    organization_role_id = db.Column(
        'organization_role_id',
        db.Integer,
        db.ForeignKey("organization_roles.organization_role_id"))

    # user = db.relationship(
    #     "Users", backref='user_organizations')

    # organization = db.relationship(
    #     "Organizations", backref='organization_users')

    organization_role = db.relationship(
        'OrganizationRoles', backref='users_organizations')

    def __init__(self, user_id: int, organization_id: int, organization_role_id: int):
        self.user_id = user_id
        self.organization_id = organization_id
        self.organization_role_id = organization_role_id

    def __repr__(self):
        return f'<UsersOrganizations(user_id={self.user_id},organization_id={self.organization_id},organization_role_id={self.organization_role_id})>'


class UsersOrganizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = UsersOrganizations
        include_fk = True


# users_organizations_table = db.Table('users_organizations',
#                                      db.Column('user_id',
#                                                db.Integer,
#                                                db.ForeignKey("users.user_id"),
#                                                primary_key=True),
#                                      db.Column('organization_id',
#                                                db.Integer,
#                                                db.ForeignKey(
#                                                    "organizations.organization_id"),
#                                                primary_key=True),
#                                      db.Column(
#                                          'organization_role_id',
#                                          db.Integer,
#                                          db.ForeignKey("organization_roles.organization_role_id")))


# class UsersOrganizationsSchema(ma.SQLAlchemyAutoSchema):
#     class Meta():
#         table = users_organizations_table
#         include_fk = True
