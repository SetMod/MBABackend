from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError
from flask_sqlalchemy.model import Model
import sqlalchemy as sa
from typing import Union
from app import db


class GenericService:
    def __init__(self, schema: SQLAlchemyAutoSchema, model_class: type[Model]) -> None:
        self.schema = schema
        self.model_class = model_class

    def get_all(self, dump: bool = True) -> Union[list[Model], list[dict]]:
        result = db.session.query(self.model_class).all()
        return self.schema.dump(result, many=True) if dump else result

    def get_by_id(self, id: int, dump: bool = True) -> Union[Model, dict]:
        result = (
            db.session.query(self.model_class).where(self.model_class.id == id).first()
        )
        return self.schema.dump(result) if dump else result

    def get_by_name(self, name: str, dump: bool = True) -> Union[Model, dict]:
        result = db.session.query(self.model_class).filter_by(name=name).first()
        return self.schema.dump(result) if dump else result

    def create(self, model: Model, dump: bool = True) -> Union[Model, dict]:
        db.session.add(model)
        db.session.commit()
        return self.schema.dump(model) if dump else model

    def update(
        self, id: int, updated_model: Model, dump: bool = True
    ) -> Union[Model, dict]:
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
        result = self.get_by_id(id, dump=False)

        if not isinstance(result, self.model_class):
            return result

        db.session.delete(result)
        db.session.commit()
        return self.schema.dump(result) if dump else result

    def map_model(self, data: dict):
        try:
            model = self.schema.load(data)
            model = self.model_class(**data)
            return model
        except ValidationError as err:
            return err.messages
