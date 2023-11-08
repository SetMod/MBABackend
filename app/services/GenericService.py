from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError
from flask_sqlalchemy.model import Model
from datetime import datetime
from app.config import logger
from typing import Union
import sqlalchemy as sa
from app.init import db


class GenericService:
    def __init__(self, schema: SQLAlchemyAutoSchema, model_class: type[Model]) -> None:
        self.schema = schema
        self.model_class = model_class

    def get_all(
        self,
        page: Union[int, None] = None,
        per_page: Union[int, None] = None,
        max_per_page: Union[int, None] = None,
        count: bool = True,
        dump: bool = True,
    ) -> Union[list[Model], list[dict]]:
        result = db.session.query(self.model_class).all()
        # result = db.paginate(
        #     select=db.session.query(self.model_class).all(),
        #     page=page,
        #     per_page=per_page,
        #     max_per_page=max_per_page,
        #     count=count,
        # )
        return self.schema.dump(result, many=True) if dump else result

    def get_by_id(self, id: int, dump: bool = True) -> Union[Model, dict, None]:
        result = (
            db.session.query(self.model_class).where(self.model_class.id == id).first()
        )

        if not result:
            return None

        return self.schema.dump(result) if dump else result

    def get_by_field(
        self, field_name: str, field_value, dump: bool = True
    ) -> Union[Model, dict, None]:
        if not hasattr(self.model_class, field_name):
            return None
        value = getattr(self.model_class, field_name)

        # Check if it works
        if not isinstance(value, sa.Column):
            return None

        result = db.session.query(self.model_class).where(value == field_value).first()

        if not result:
            return None

        return self.schema.dump(result) if dump else result

    def get_by_name(self, name: str, dump: bool = True) -> Union[Model, dict, None]:
        result = db.session.query(self.model_class).filter_by(name=name).first()

        if not result:
            return None

        return self.schema.dump(result) if dump else result

    def create(self, model: Model, dump: bool = True) -> Union[Model, dict]:
        db.session.add(model)
        db.session.commit()
        return self.schema.dump(model) if dump else model

    def update(
        self, id: int, updated_model: Model, dump: bool = True
    ) -> Union[Model, dict, None]:
        model = self.get_by_id(id, dump=False)

        if not isinstance(model, self.model_class):
            return model

        for attr_name in dir(updated_model):
            attr_skip_list = ["id", "metadata", "query", "query_class", "registry"]
            if attr_name.startswith("__") or attr_name.startswith("_sa_"):
                continue
            if not hasattr(model, attr_name):
                continue
            if attr_name in attr_skip_list:
                continue

            attr_value = getattr(updated_model, attr_name)

            if not isinstance(attr_value, sa.Column):
                continue

            setattr(model, attr_name, attr_value)

        db.session.commit()
        return self.schema.dump(model) if dump else model

    def delete(self, id: int, dump: bool = True):
        model = self.get_by_id(id, dump=False)

        if not isinstance(model, self.model_class):
            return model

        db.session.delete(model)
        db.session.commit()
        return self.schema.dump(model) if dump else model

    def soft_delete(self, id: int, dump: bool = True):
        model = self.get_by_id(id, dump=False)

        if not isinstance(model, self.model_class):
            return model

        model.soft_deleted = True
        model.deleted_date = datetime.utcnow()

        db.session.commit()
        return self.schema.dump(model) if dump else model

    def map_model(self, model_dict: dict):
        try:
            model = self.schema.load(model_dict)
            model = self.model_class(**model_dict)
            return model
        except ValidationError as err:
            return err.messages
