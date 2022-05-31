from flask import Blueprint, jsonify, request
from models.VisualizationsModel import Visualizations
from services.VisualizationsService import VisualizationsService

visualizations_api = Blueprint('visualizations', __name__)
visualizations_service = VisualizationsService()


@visualizations_api.get('/')
def get_all_visualizations():
    visualizations = visualizations_service.get_all_visualizations()
    return jsonify(visualizations), 200


@visualizations_api.get('/<int:visualization_id>')
def get_visualization_by_id(visualization_id: int):
    visualization = visualizations_service.get_visualization_by_id(
        visualization_id)
    return jsonify(visualization), 200


@visualizations_api.post('/')
def create_visualization():
    visualization_name = request.json['visualization_name']
    visualization_image_path = request.json['visualization_image_path']
    report_id = request.json['report_id']
    visualization = Visualizations(visualization_name=visualization_name,
                                   visualization_image_path=visualization_image_path, report_id=report_id)
    new_visualization = visualizations_service.create_visualization(
        visualization)
    return jsonify(new_visualization)


@visualizations_api.put('/<int:visualization_id>')
def update_visualization(visualization_id: int):
    visualization_name = request.json['visualization_name']
    visualization_image_path = request.json['visualization_image_path']
    report_id = request.json['report_id']
    visualization = Visualizations(visualization_name=visualization_name,
                                   visualization_image_path=visualization_image_path, report_id=report_id)
    updated_visualization = visualizations_service.update_visualization(
        visualization_id, visualization)
    return jsonify(updated_visualization)


@visualizations_api.delete('/<int:visualization_id>')
def delete_role(visualization_id: int):
    return visualizations_service.delete_visualization(visualization_id)
