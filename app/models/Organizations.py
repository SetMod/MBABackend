from app.models import GenericModel
from app.init import db, ma


class Organizations(db.Model, GenericModel):
    __tablename__ = "organizations"

    name = db.Column("name", db.String(200), unique=True, nullable=False)

    description = db.Column("description", db.Text, nullable=False)

    email = db.Column("email", db.String(255), unique=True, nullable=False)

    phone = db.Column("phone", db.String(18), unique=True)

    members = db.relationship(
        "UsersOrganizations",
        backref="organization",
        cascade="save-update, merge, delete",
    )

    def __repr__(self):
        return f"<Organization(id={self.id},name={self.name},description={self.description},email={self.email},phone={self.phone},create_date={self.create_date})>"


class OrganizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Organizations
