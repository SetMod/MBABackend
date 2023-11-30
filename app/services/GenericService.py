from enum import Enum
from typing import List, Union
from datetime import datetime
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy import Row, or_
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError
from app.exceptions import CustomBadRequest, CustomNotFound
from app.logger import logger
from app.models import GenericModel
from app.db import db


class GenericService:
    def __init__(
        self, schema: SQLAlchemyAutoSchema, model_class: type[GenericModel]
    ) -> None:
        self.schema = schema
        self.model_class = model_class

    def to_json(
        self, model: Union[GenericModel, List[GenericModel]]
    ) -> Union[dict, List[dict]]:
        if isinstance(model, list):
            model_json = self.schema.dump(model, many=True)
        else:
            model_json = self.schema.dump(model)

        logger.debug(f"{self.model_class._name(lower=False)} json: {model_json}")
        return model_json

    def map_model(self, model_dict: dict) -> GenericModel:
        logger.info(f"Mapping {self.model_class._name()} model")
        try:
            model_dict = self.schema.load(model_dict)
            model = self.model_class(**model_dict)
            logger.info(f"Mapped {self.model_class._name()}: {model}")
            return model
        except ValidationError as err:
            err_msg = err.messages
            # err_msg = f"Failed to map {self.model_name()} model due to {err}"
            logger.error(err_msg)
            raise CustomBadRequest(err_msg)

    def get_all(self) -> list[GenericModel]:
        logger.info(f"Getting all {self.model_class._name(many=True)}")
        models = (
            db.session.execute(
                db.select(self.model_class).where(
                    self.model_class.soft_deleted == False
                )
            )
            .scalars()
            .all()
        )

        logger.info(f"Found {self.model_class._name(many=True)}: {models}")
        return models

    def get_by_id(self, id: int, must_exist: bool = True) -> GenericModel:
        logger.info(f"Getting {self.model_class._name()} with id='{id}'")

        if not isinstance(id, int):
            msg = f"Bad id type '{type(id)}', expected type 'int'"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        model = db.session.execute(
            db.select(self.model_class).where(self.model_class.id == id)
        ).scalar_one_or_none()

        if must_exist and not model:
            msg = f"{self.model_class._name(lower=False)} with id='{id}' not found"
            logger.warning(msg)
            raise CustomNotFound(msg)
        elif not must_exist and model:
            msg = f"{self.model_class._name(lower=False)} with id='{id}' already exists"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        logger.info(f"Found {self.model_class._name()}: {model}")
        return model

    def get_by_field(
        self, field_name: str, field_value, must_exist: bool = True
    ) -> GenericModel:
        logger.info(
            f"Getting {self.model_class._name()} with {field_name}='{field_value}'"
        )
        if not hasattr(self.model_class, field_name):
            msg = f"{self.model_class._name(lower=False)} doesn't have '{field_name}' field"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        field = getattr(self.model_class, field_name)
        model = db.session.execute(
            db.select(self.model_class).where(field == field_value)
        ).scalar_one_or_none()

        if must_exist and not model:
            msg = f"{self.model_class._name(lower=False)} with field {field_name}='{field_value}' not found"
            logger.warning(msg)
            raise CustomNotFound(msg)
        elif not must_exist and model:
            msg = f"{self.model_class._name(lower=False)} with field {field_name}='{field_value}' already exists"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        logger.info(f"Found {self.model_class._name()}: {model}")
        return model

    def get_by_fields(
        self, model_dict: dict, many: bool = False, must_exist: bool = True
    ) -> Union[GenericModel, List[GenericModel]]:
        logger.info(
            f"Getting {self.model_class._name(many=many)} with fields {model_dict}"
        )
        for key in model_dict:
            if key not in [
                column.name for column in self.model_class.__table__.columns
            ]:
                msg = (
                    f"{self.model_class._name(lower=False)} doesn't have '{key}' field"
                )
                logger.warning(msg)
                raise CustomBadRequest(msg)

        if many:
            models: List[GenericModel] = (
                db.session.execute(db.select(self.model_class).filter_by(**model_dict))
                .scalars()
                .all()
            )

            logger.info(f"Found {self.model_class._name(many=True)}: {models}")
            return models
        else:
            model: Row[GenericModel] = db.session.execute(
                db.select(self.model_class).filter_by(**model_dict)
            ).scalar()
            # ).scalar_one_or_none()

            if must_exist and not model:
                msg = f"{self.model_class._name(lower=False)} with fields '{model_dict}' not found"
                logger.warning(msg)
                raise CustomNotFound(msg)
            elif not must_exist and model:
                msg = f"{self.model_class._name(lower=False)} with fields '{model_dict}' already exists"
                logger.warning(msg)
                raise CustomBadRequest(msg)

            logger.info(f"Found {self.model_class._name()}: {model}")
            return model

    def get_by_unique_fields(
        self, model_dict: dict, must_exist: bool = False
    ) -> Union[GenericModel, None]:
        logger.info(f"Getting {self.model_class._name()} by unique fields")

        unique_fields = {}
        for column in self.model_class.__table__.columns:
            if column.unique:
                column_name = column.name
                if column_name in model_dict:
                    unique_fields[column_name] = model_dict[column_name]

        logger.info(
            f"{self.model_class._name(lower=False)} unique fields: {unique_fields}"
        )

        if not unique_fields:
            return None

        conditions = [
            getattr(self.model_class, field) == value
            for field, value in unique_fields.items()
        ]
        existing_model = db.session.execute(
            db.select(self.model_class).where(or_(*conditions))
        ).scalar_one_or_none()

        # existing_model = db.session.execute(
        #     db.select(self.model_class).filter_by(**unique_fields)
        # ).scalar_one_or_none()

        logger.info(f"Found {self.model_class._name()}: {existing_model}")
        if must_exist and not existing_model:
            msg = f"{self.model_class._name(lower=False)} with unique fields {unique_fields} not found"
            logger.warning(msg)
            raise CustomNotFound(msg)
        elif not must_exist and existing_model:
            msg = f"{self.model_class._name(lower=False)} with unique fields {unique_fields} already exists"
            logger.warning(msg)
            raise CustomBadRequest(msg)

        return existing_model

    def commit(self) -> None:
        logger.info(f"Committing {self.model_class._name()} changes")
        try:
            db.session.commit()
            logger.info(f"Successfully committed changes to {self.model_class._name()}")
        except PendingRollbackError as err:
            err_msg = f"Failed to commit {self.model_class._name()} model. Rolling back changes. Message: {err}"
            logger.error(err_msg)
            db.session.rollback()
            raise CustomBadRequest(err_msg)
        except IntegrityError as err:
            err_msg = f"Failed to commit {self.model_class._name()} model. Rolling back changes. Message: {err.orig}"
            logger.error(err_msg)
            db.session.rollback()
            raise CustomBadRequest(err_msg)

    def create(self, new_model_dict: dict) -> GenericModel:
        logger.info(f"Creating new {self.model_class._name()}")

        self.get_by_unique_fields(new_model_dict, must_exist=False)
        new_model = self.map_model(new_model_dict)

        db.session.add(new_model)
        self.commit()

        logger.info(
            f"Successfully created new {new_model._name()} with id='{new_model.id}'"
        )

        return new_model

    def update(self, id: int, updated_model_dict: dict) -> GenericModel:
        logger.info(f"Updating {self.model_class._name()} with id='{id}'")

        self.get_by_unique_fields(updated_model_dict, must_exist=False)
        existing_model: GenericModel = self.get_by_id(id)

        existing_model_dict = self.to_json(existing_model)
        for field in existing_model.updatable_fields:
            if field in updated_model_dict:
                existing_model_dict[field] = updated_model_dict[field]

        updated_model = self.map_model(existing_model_dict)
        for field in existing_model.updatable_fields:
            value = getattr(updated_model, field)
            setattr(existing_model, field, value)

        existing_model.updated_date = datetime.utcnow()
        self.commit()

        logger.info(
            f"Successfully updated {existing_model._name()} with id='{existing_model.id}'"
        )

        return existing_model

    def delete(self, id: int):
        logger.info(f"Deleting {self.model_class._name()} with id='{id}'")

        existing_model = self.get_by_id(id)

        db.session.delete(existing_model)
        self.commit()

        logger.info(
            f"Successfully deleted {self.model_class._name()} with id='{existing_model.id}'"
        )

        return existing_model

    def soft_delete(self, id: int) -> GenericModel:
        logger.info(f"Soft deleting {self.model_class._name()} with id='{id}'")

        existing_model = self.get_by_id(id)

        existing_model.soft_deleted = True
        existing_model.deleted_date = datetime.utcnow()
        self.commit()

        logger.info(
            f"Successfully soft deleted {self.model_class._name()} with id='{existing_model.id}'"
        )

        return existing_model
