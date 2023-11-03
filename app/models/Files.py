from datetime import datetime
from app import db, ma


class Files(db.Model):
    __tablename__ = "files"

    id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(100), nullable=False)

    create_date = db.Column("create_date", db.DateTime, default=datetime.utcnow)

    file_path = db.Column("file_path", db.String(255), unique=True, nullable=False)

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

    organization_id = db.Column(
        "organization_id", db.Integer, db.ForeignKey("organizations.id"), nullable=False
    )

    user = db.relationship("Users", backref="user_files")
    organization = db.relationship("Organizations", backref="organization_files")

    def __repr__(self):
        return f"<File(id={self.id},name={self.name},create_date={self.create_date},user_id={self.user_id},organization_id={self.organization_id})>"


class FilesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Files

    user_id = ma.auto_field()
    organization_id = ma.auto_field()
