from cgi import FieldStorage
from app.config import APP_UPLOAD_FOLDER
from app.exceptions import CustomBadRequest
from app.logger import logger
from app.models import Datasources, FileDatasources
from app.schemas import DatasourcesTypeFullSchema
from app.config import APP_UPLOAD_FOLDER
from app.services.GenericService import GenericService
from app.utils import allowed_file, generate_unique_filename
from app.db import db
import os


class DatasourcesService(GenericService):
    def __init__(self) -> None:
        super().__init__(
            schema=DatasourcesTypeFullSchema(), model_class=Datasources
        )

    def create_file(self, new_file_datasource_dict: dict, file: FieldStorage):
        logger.info(f"Creating new {self.model_class._name()}")

        if file.filename == "":
            err_msg = "No selected file"
            logger.warning(err_msg)
            raise CustomBadRequest(err_msg)

        if not allowed_file(file.filename):
            err_msg = "Not allowed file extension"
            logger.warning(err_msg)
            raise CustomBadRequest(err_msg)

        _, file_extension = os.path.splitext(file.filename)
        unique_filename = generate_unique_filename(
            file_prefix="fd", file_extension=file_extension
        )

        unique_file_path = APP_UPLOAD_FOLDER.joinpath(unique_filename)

        if unique_file_path.exists():
            err_msg = "File path already exists"
            logger.warning(err_msg)
            raise CustomBadRequest(err_msg)

        if not APP_UPLOAD_FOLDER.exists():
            logger.info(f"Creating upload dir at '{APP_UPLOAD_FOLDER.as_posix()}'")
            os.makedirs(APP_UPLOAD_FOLDER)

        new_file_datasource: FileDatasources = self.map_model(new_file_datasource_dict)
        new_file_datasource.file_path = unique_file_path.as_posix()
        db.session.add(new_file_datasource)
        self.commit()

        logger.info(f"Saving new file to '{new_file_datasource.file_path}'")
        file.save(new_file_datasource.file_path)

        logger.info(
            f"Successfully created new {new_file_datasource._name()} with id='{new_file_datasource.id}'"
        )
        return new_file_datasource

    def delete(self, id: int):
        logger.info(f"Deleting {self.model_class._name()} with id='{id}'")

        existing_model: FileDatasources = self.get_by_id(id)

        if os.path.exists(existing_model.file_path):
            logger.info(f"Deleting file at '{existing_model.file_path}'")
            os.remove(existing_model.file_path)

        db.session.delete(existing_model)
        self.commit()

        logger.info(
            f"Successfully deleted {self.model_class._name()} with id='{existing_model.id}'"
        )
        return existing_model
