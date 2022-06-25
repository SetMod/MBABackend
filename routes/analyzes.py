import os
from flask import Blueprint, jsonify, request, send_from_directory
from app import ANALYZES_UPLOAD_FOLDER
from models.AnalyzesModel import Analyzes
from services.AnalyzesService import AnalyzesService

analyzes_api = Blueprint('analyzes', __name__)
analyzes_service = AnalyzesService()


@analyzes_api.get('/')
def get_all_analyzes():
    analyzes = analyzes_service.get_all_analyzes()

    if isinstance(analyzes, str):
        return analyzes, 404
    else:
        return jsonify(analyzes), 200


@analyzes_api.get('/<int:analyze_id>')
def get_analyze_by_id(analyze_id: int):
    analyze = analyzes_service.get_analyze_by_id(analyze_id)

    if isinstance(analyze, str):
        return analyze, 404
    else:
        return jsonify(analyze), 200


@analyzes_api.get('/download/<int:analyze_id>')
def download_analyze_by_id(analyze_id: int):
    analyze = analyzes_service.get_analyze_by_id(analyze_id)

    if isinstance(analyze, str):
        return analyze, 404

    if not os.path.exists(analyze['analyze_file_path']):
        return 'File path doesn\'t exists', 400

    file_name = os.path.basename(analyze['analyze_file_path'])
    return send_from_directory(ANALYZES_UPLOAD_FOLDER, file_name, file_name, as_attachment=True)


@analyzes_api.post('/')
def create_analyze():
    request.json['analyze_file_path'] = 'None'
    file_id = request.args.get('file_id')

    if file_id is None:
        return 'The file id is not specified'

    analyze = analyzes_service.map_analyze(request.json)

    if not isinstance(analyze, Analyzes):
        return jsonify(analyze), 400

    created_analyze = analyzes_service.create_analyze(
        analyze, file_id)

    if isinstance(created_analyze, str):
        return created_analyze, 400
    else:
        return created_analyze.to_json(orient='records'), 201


@analyzes_api.put('/<int:analyze_id>')
def update_analyze(analyze_id: int):
    analyze = analyzes_service.map_analyze(request.json)

    if not isinstance(analyze, Analyzes):
        return jsonify(analyze), 400

    updated_analyze = analyzes_service.update_analyze(analyze_id, analyze)

    if isinstance(updated_analyze, str):
        return updated_analyze, 400
    else:
        return jsonify(updated_analyze), 201


@analyzes_api.delete('/<int:analyze_id>')
def delete_role(analyze_id: int):
    deleted_analyze = analyzes_service.delete_analyze(analyze_id)

    if isinstance(deleted_analyze, str):
        return deleted_analyze, 400
    else:
        return jsonify(deleted_analyze), 200
