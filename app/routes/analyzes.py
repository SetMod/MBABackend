from flask import Blueprint, jsonify, request, send_from_directory
from app import ANALYZES_UPLOAD_FOLDER
from app.models import Analyzes
from app.services import AnalyzesService
import os

analyzes_api = Blueprint("analyzes", __name__)
analyzes_service = AnalyzesService()


@analyzes_api.get("/")
def get_all_analyzes():
    analyzes = analyzes_service.get_all_analyzes()

    if isinstance(analyzes, str):
        return analyzes, 404
    else:
        return jsonify(analyzes), 200


@analyzes_api.get("/<int:id>")
def get_analyze_by_id(id: int):
    analyze = analyzes_service.get_analyze_by_id(id)

    if isinstance(analyze, str):
        return analyze, 404
    else:
        return jsonify(analyze), 200


@analyzes_api.get("/download/<int:id>")
def download_analyze_by_id(id: int):
    analyze = analyzes_service.get_analyze_by_id(id)

    if isinstance(analyze, str):
        return analyze, 404

    if not os.path.exists(analyze["file_path"]):
        return "Analyze file doesn't exists", 400

    name = os.path.basename(analyze["file_path"])
    return send_from_directory(ANALYZES_UPLOAD_FOLDER, name, name, as_attachment=True)


@analyzes_api.post("/")
def create_analyze():
    request.json["file_path"] = "None"
    id = request.args.get("id")

    if id is None:
        return "The file id is not specified"

    analyze = analyzes_service.map_analyze(request.json)

    if not isinstance(analyze, Analyzes):
        return jsonify(analyze), 400

    created_analyze = analyzes_service.create_analyze(analyze, id)

    if isinstance(created_analyze, str):
        return created_analyze, 400
    else:
        return created_analyze.to_json(orient="records"), 201


@analyzes_api.put("/<int:id>")
def update_analyze(id: int):
    analyze = analyzes_service.map_analyze(request.json)

    if not isinstance(analyze, Analyzes):
        return jsonify(analyze), 400

    updated_analyze = analyzes_service.update_analyze(id, analyze)

    if isinstance(updated_analyze, str):
        return updated_analyze, 400
    else:
        return jsonify(updated_analyze), 201


@analyzes_api.delete("/<int:id>")
def delete_role(id: int):
    deleted_analyze = analyzes_service.delete_analyze(id)

    if isinstance(deleted_analyze, str):
        return deleted_analyze, 400
    else:
        return jsonify(deleted_analyze), 200
