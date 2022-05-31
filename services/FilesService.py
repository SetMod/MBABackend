from cgi import FieldStorage
import os
from marshmallow import ValidationError
from app import UPLOAD_FOLDER, db
from models.FilesModel import Files, FilesSchema
from werkzeug.utils import secure_filename


class FilesService():

    def __init__(self) -> None:
        self.files_schema = FilesSchema()

    def get_all_files(self, dump: bool = True):
        files = db.session.query(Files).all()

        if len(files) > 0:
            return self.files_schema.dump(files, many=True) if dump else files
        else:
            return None

    def get_file_by_id(self, file_id: int, dump: bool = True):
        file = db.session.query(Files).where(Files.file_id == file_id).first()

        if isinstance(file, Files):
            return self.files_schema.dump(file) if dump else file
        else:
            return None

    def create_file(self, file: Files, csv_file: FieldStorage, dump: bool = True):
        try:
            db.session.add(file)
            db.session.commit()

            file_path = os.path.join(
                UPLOAD_FOLDER, secure_filename(f'file_{file.file_id}.csv'))
            file.file_path = file_path
            csv_file.save(file.file_path)

            db.session.commit()
            return self.files_schema.dump(file) if dump else file
        except Exception:
            return None

    def update_file(self, file_id: int, updated_file: Files, dump: bool = True):
        file = self.get_file_by_id(file_id=file_id, dump=False)

        try:
            if isinstance(file, Files):
                file.file_name = updated_file.file_name
                # file.file_path = updated_file.file_path
                db.session.commit()
                return self.files_schema.dump(file) if dump else file
            else:
                return None
        except Exception:
            return None

    def delete_file(self, file_id: int, dump: bool = True):
        file = self.get_file_by_id(file_id=file_id, dump=False)

        try:
            if isinstance(file, Files):
                if os.path.exists(file.file_path):
                    os.remove(file.file_path)
                db.session.delete(file)
                db.session.commit()
                return self.files_schema.dump(file) if dump else file
            else:
                return None
        except Exception:
            return None

    def map_file(self, file_dict: dict):
        try:
            file = self.files_schema.load(file_dict)
            file_name = file_dict['file_name']
            file_path = file_dict['file_path']
            user_id = file_dict['user_id']
            organization_id = file_dict['organization_id']
            file = Files(file_name=file_name, file_path=file_path,
                         user_id=user_id, organization_id=organization_id)
            return file
        except ValidationError as err:
            return err.messages
