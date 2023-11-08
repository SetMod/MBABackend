from app.config import UPLOAD_FOLDER, logger
from werkzeug.utils import secure_filename
from app.models import Files, FilesSchema
from app.services import GenericService
from cgi import FieldStorage
from app.init import db
import os


class FilesService(GenericService):
    def __init__(self) -> None:
        super().__init__(schema=FilesSchema(), model_class=Files)

    def create_file(self, file: Files, csv_file: FieldStorage, dump: bool = True):
        db.session.add(file)
        db.session.commit()

        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(f"file_{file.id}.csv"))

        if os.path.exists(file_path):
            logger.warn(f"File {file_path} already exists")

        file.file_path = file_path
        csv_file.save(file.file_path)
        db.session.commit()

        return self.schema.dump(file) if dump else file

    def delete_file(self, id: int, dump: bool = True):
        file = self.get_by_id(id=id, dump=False)

        if not isinstance(file, Files):
            return file

        if os.path.exists(file.file_path):
            os.remove(file.file_path)

        db.session.delete(file)
        db.session.commit()

        return self.schema.dump(file) if dump else file
