from datetime import datetime
from app.init import db


class GenericModel:
    id = db.Column("id", db.Integer, primary_key=True)

    created_date = db.Column(
        name="created_date", type_=db.DateTime, default=datetime.utcnow
    )

    updated_date = db.Column(name="updated_date", type_=db.DateTime, nullable=True)

    deleted_date = db.Column(name="deleted_date", type_=db.DateTime, nullable=True)

    soft_deleted = db.Column(name="soft_deleted", type_=db.Boolean, default=False)
