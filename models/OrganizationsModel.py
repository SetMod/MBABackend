from datetime import datetime
from app import db, ma


class Organizations(db.Model):
    __tablename__ = "organizations"

    organization_id = db.Column(
        'organization_id',
        db.Integer,
        primary_key=True)

    organization_name = db.Column(
        'organization_name',
        db.String(200),
        unique=True,
        nullable=False)

    organization_description = db.Column(
        'organization_description',
        db.Text,
        nullable=False)

    organization_email = db.Column(
        'organization_email',
        db.String(255),
        unique=True,
        nullable=False)

    organization_phone = db.Column(
        'organization_phone',
        db.String(18),
        unique=True)

    organization_create_date = db.Column(
        'organization_create_date',
        db.DateTime,
        default=datetime.utcnow)

    organization_users = db.relationship(
        "UsersOrganizations", backref='organization')

    def __repr__(self):
        return f'<Organization(organization_id={self.organization_id},organization_name={self.organization_name},organization_description={self.organization_description},organization_email={self.organization_email},organization_phone={self.organization_phone},organization_create_date={self.organization_create_date})>'


class OrganizationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Organizations
