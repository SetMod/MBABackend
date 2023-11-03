from cgi import FieldStorage
import os
from marshmallow import ValidationError
from app import UPLOAD_FOLDER, db
from app.models import Files, FilesSchema
from werkzeug.utils import secure_filename


class FilesService:
    def __init__(self) -> None:
        self.files_schema = FilesSchema()

    def get_all_files(self, dump: bool = True):
        try:
            files = db.session.query(Files).all()

            if len(files) > 0:
                return self.files_schema.dump(files, many=True) if dump else files
            else:
                return None
        except Exception as err:
            print(err)
            return "Failed to get files"

    def get_file_by_id(self, id: int, dump: bool = True):
        try:
            file = db.session.query(Files).where(Files.id == id).first()

            if isinstance(file, Files):
                return self.files_schema.dump(file) if dump else file
            else:
                return "File not found"
        except Exception as err:
            print(err)
            return "Failed to get file"

    def create_file(self, file: Files, csv_file: FieldStorage, dump: bool = True):
        try:
            db.session.add(file)
            db.session.commit()

            file_path = os.path.join(
                UPLOAD_FOLDER, secure_filename(f"file_{file.id}.csv")
            )
            file.file_path = file_path
            csv_file.save(file.file_path)

            db.session.commit()
            return self.files_schema.dump(file) if dump else file
        except Exception as err:
            print(err)
            return "Failed to create file"

    def update_file(self, id: int, updated_file: Files, dump: bool = True):
        file = self.get_file_by_id(id=id, dump=False)

        if not isinstance(file, Files):
            return file

        try:
            file.name = updated_file.name
            # file.file_path = updated_file.file_path
            db.session.commit()
            return self.files_schema.dump(file) if dump else file
        except Exception as err:
            print(err)
            return "Failed to update file"

    def delete_file(self, id: int, dump: bool = True):
        file = self.get_file_by_id(id=id, dump=False)

        if not isinstance(file, Files):
            return file

        try:
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            db.session.delete(file)
            db.session.commit()
            return self.files_schema.dump(file) if dump else file
        except Exception as err:
            print(err)
            return "Failed to delete file"

    def map_file(self, file_dict: dict):
        try:
            file = self.files_schema.load(file_dict)
            name = file_dict["name"]
            file_path = file_dict["file_path"]
            user_id = file_dict["user_id"]
            organization_id = file_dict["organization_id"]
            file = Files(
                name=name,
                file_path=file_path,
                user_id=user_id,
                organization_id=organization_id,
            )
            return file
        except ValidationError as err:
            return err.messages
