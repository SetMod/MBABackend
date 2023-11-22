import os
from cgi import FieldStorage
from werkzeug.utils import secure_filename
from app.config import APP_UPLOAD_FOLDER
from app.logger import logger
from app.db import db
from app.models import FileDatasources
from app.schemas import FileDatasourcesSchema
from app.services.GenericService import GenericService


class FileDatasourcesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=FileDatasourcesSchema(), model_class=FileDatasources)

    def create_file(
        self, file: FileDatasources, csv_file: FieldStorage, dump: bool = True
    ):
        db.session.add(file)
        db.session.commit()

        file_path = os.path.join(
            APP_UPLOAD_FOLDER, secure_filename(f"file_{file.id}.csv")
        )

        if os.path.exists(file_path):
            logger.warn(f"File {file_path} already exists")

        file.file_path = file_path
        csv_file.save(file.file_path)
        db.session.commit()

        return self.schema.dump(file) if dump else file

    def delete_file(self, id: int, dump: bool = True):
        file = self.get_by_id(id=id, dump=False)

        if not isinstance(file, FileDatasources):
            return file

        if os.path.exists(file.file_path):
            os.remove(file.file_path)

        db.session.delete(file)
        db.session.commit()

        return self.schema.dump(file) if dump else file