import os
from flask import Blueprint, jsonify, request, send_from_directory
from app import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import app
from app.models import Files
from app.services import FilesService

files_api = Blueprint("files", __name__)
files_service = FilesService()


@files_api.get("/")
def get_all_files():
    files = files_service.get_all_files()

    if isinstance(files, str):
        return files, 404
    else:
        return jsonify(files), 200


@files_api.get("/<int:id>")
def get_file_by_id(id: int):
    file = files_service.get_file_by_id(id)

    if isinstance(file, str):
        return file, 404
    else:
        return jsonify(file), 200


@files_api.get("/download/<int:id>")
def download_file_by_id(id: int):
    file = files_service.get_file_by_id(id)

    if isinstance(file, str):
        return file, 404

    if not os.path.exists(file["file_path"]):
        return "File path doesn't exists", 400

    name = os.path.basename(file["file_path"])
    return send_from_directory(UPLOAD_FOLDER, name, name, as_attachment=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@files_api.post("/upload")
def create_file():
    if "file" not in request.files:
        return "No file part", 400

    name = request.args.get("name")
    user_id = request.args.get("user_id")
    organization_id = request.args.get("organization_id")
    csv_file = request.files["file"]

    if user_id is None or organization_id is None:
        return "User or organization not specified", 400
    if csv_file.filename == "":
        return "No selected file", 400
    if not allowed_file(csv_file.filename):
        return "Not allowed file format", 400

    file = Files(
        name=name,
        file_path="",
        user_id=user_id,
        organization_id=organization_id,
    )
    created_file = files_service.create_file(file, csv_file)

    if isinstance(created_file, str):
        return created_file, 400
    else:
        return jsonify(created_file)


@files_api.put("/<int:id>")
def update_file(id: int):
    file = files_service.map_file(request.json)

    if not isinstance(file, Files):
        return jsonify(file), 400

    updated_file = files_service.update_file(id, file)

    if isinstance(updated_file, str):
        return updated_file, 400
    else:
        return jsonify(updated_file), 200


@files_api.delete("/<int:id>")
def delete_role(id: int):
    deleted_file = files_service.delete_file(id)

    if isinstance(deleted_file, str):
        return deleted_file, 400
    else:
        return jsonify(deleted_file), 200
