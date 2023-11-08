from flask import Blueprint, jsonify, request
from app.models import Reports
from app.services import ReportsService

reports_api = Blueprint("reports", __name__)
reports_service = ReportsService()


@reports_api.get("/")
def get_all_reports():
    reports = reports_service.get_all()

    if reports is None:
        return "Reports not found", 404
    else:
        return jsonify(reports), 200


@reports_api.get("/<int:id>")
def get_report_by_id(id: int):
    report = reports_service.get_by_id(id)

    if report is None:
        return "Report not found", 404
    else:
        return jsonify(report), 200


@reports_api.get("/<int:id>/analyzes")
def get_report_analyzes(id: int):
    analyzes = reports_service.get_report_analyzes(id)

    if analyzes is None:
        return "Analyzes not found", 404
    else:
        return jsonify(analyzes), 200


@reports_api.get("/<int:id>/visualizations")
def get_report_visualizations(id: int):
    visualizations = reports_service.get_report_visualizations(id)

    if visualizations is None:
        return "Visualizations not found", 404
    else:
        return jsonify(visualizations), 200


@reports_api.post("/")
def create_report():
    report = reports_service.map_model(request.json)

    if not isinstance(report, Reports):
        return jsonify(report), 400

    created_report = reports_service.create(report)

    if created_report is None:
        return "Failed to create a report", 400
    else:
        return jsonify(created_report), 201


@reports_api.put("/<int:id>")
def update_report(id: int):
    report = reports_service.map_model(request.json)

    if not isinstance(report, Reports):
        return jsonify(report), 400

    updated_report = reports_service.update(id, report)

    if updated_report is None:
        return "Failed to update a report", 400
    else:
        return jsonify(updated_report), 201


@reports_api.delete("/<int:id>")
def delete_report(id: int):
    deleted_report = reports_service.delete(id)

    if deleted_report is None:
        return "Failed to delete a report", 400
    else:
        return jsonify(deleted_report)
