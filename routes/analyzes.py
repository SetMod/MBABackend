from re import L
from flask import Blueprint, jsonify, request
from models.AnalyzesModel import Analyzes
from services.AnalyzesService import AnalyzesService

analyzes_api = Blueprint('analyzes', __name__)
analyzes_service = AnalyzesService()


@analyzes_api.get('/')
def get_all_analyzes():
    analyzes = analyzes_service.get_all_analyzes()

    if analyzes is None:
        return 'Analyzes not found', 404
    else:
        return jsonify(analyzes), 200


@analyzes_api.get('/<int:analyze_id>')
def get_analyze_by_id(analyze_id: int):
    analyze = analyzes_service.get_analyze_by_id(analyze_id)

    if analyze is None:
        return 'Analyze not found', 404
    else:
        return jsonify(analyze), 200


@analyzes_api.post('/')
def create_analyze():
    analyze = analyzes_service.map_analyze(request.json)

    if not isinstance(analyze, Analyzes):
        return jsonify(analyze), 400

    created_analyze = analyzes_service.create_analyze(analyze)

    if created_analyze is None:
        return 'Failed to create an analyze', 400
    else:
        return jsonify(created_analyze), 201


@analyzes_api.put('/<int:analyze_id>')
def update_analyze(analyze_id: int):
    analyze = analyzes_service.map_analyze(request.json)

    if not isinstance(analyze, Analyzes):
        return jsonify(analyze), 400

    updated_analyze = analyzes_service.update_analyze(analyze_id, analyze)

    if updated_analyze is None:
        return 'Failed to update an analyze', 400
    else:
        return jsonify(updated_analyze), 201


@analyzes_api.delete('/<int:analyze_id>')
def delete_role(analyze_id: int):
    deleted_analyze = analyzes_service.delete_analyze(analyze_id)

    if deleted_analyze is None:
        return 'Failed to delete an analyze', 400
    else:
        return jsonify(deleted_analyze), 200
