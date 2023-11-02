from flask import Blueprint, jsonify, request
from models.ReportsModel import Reports

from services.ReportsService import ReportsService

reports_api = Blueprint('reports', __name__)
reports_service = ReportsService()


@reports_api.get('/')
def get_all_reports():
    reports = reports_service.get_all_reports()

    if reports is None:
        return 'Reports not found', 404
    else:
        return jsonify(reports), 200


@reports_api.get('/<int:report_id>')
def get_report_by_id(report_id: int):
    report = reports_service.get_report_by_id(report_id)

    if report is None:
        return 'Report not found', 404
    else:
        return jsonify(report), 200


@reports_api.get('/<int:report_id>/analyzes')
def get_report_analyzes(report_id: int):
    analyzes = reports_service.get_report_analyzes(report_id)

    if analyzes is None:
        return 'Analyzes not found', 404
    else:
        return jsonify(analyzes), 200


@reports_api.get('/<int:report_id>/visualizations')
def get_report_visualizations(report_id: int):
    visualizations = reports_service.get_report_visualizations(report_id)

    if visualizations is None:
        return 'Visualizations not found', 404
    else:
        return jsonify(visualizations), 200


@reports_api.post('/')
def create_report():
    report = reports_service.map_report(request.json)

    if not isinstance(report, Reports):
        return jsonify(report), 400

    created_report = reports_service.create_report(report)

    if created_report is None:
        return "Failed to create a report", 400
    else:
        return jsonify(created_report), 201


@reports_api.put('/<int:report_id>')
def update_report(report_id: int):
    report = reports_service.map_report(request.json)

    if not isinstance(report, Reports):
        return jsonify(report), 400

    updated_report = reports_service.update_report(report_id, report)

    if updated_report is None:
        return "Failed to update a report", 400
    else:
        return jsonify(updated_report), 201


@reports_api.delete('/<int:report_id>')
def delete_report(report_id: int):
    deleted_report = reports_service.delete_report(report_id)

    if deleted_report is None:
        return 'Failed to delete a report', 400
    else:
        return jsonify(deleted_report)
