from datetime import datetime
from app import db, ma


class Organizations(db.Model):
    __tablename__ = "organizations"

    id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(200), unique=True, nullable=False)

    description = db.Column("description", db.Text, nullable=False)

    email = db.Column("email", db.String(255), unique=True, nullable=False)

    phone = db.Column("phone", db.String(18), unique=True)

    create_date = db.Column("create_date", db.DateTime, default=datetime.utcnow)

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
