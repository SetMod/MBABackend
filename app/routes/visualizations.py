import os
import pandas as pd
from flask import Blueprint, jsonify, request, send_from_directory
from app import VISUALIZATIONS_UPLOAD_FOLDER
from app.models.VisualizationsModel import Visualizations
from app.services.VisualizationsService import VisualizationsService

visualizations_api = Blueprint('visualizations', __name__)
visualizations_service = VisualizationsService()


@visualizations_api.get('/')
def get_all_visualizations():
    visualizations = visualizations_service.get_all_visualizations()

    if isinstance(visualizations, str):
        return visualizations, 404
    else:
        return jsonify(visualizations), 200


@visualizations_api.get('/<int:visualization_id>')
def get_visualization_by_id(visualization_id: int):
    visualization = visualizations_service.get_visualization_by_id(
        visualization_id)

    if isinstance(visualization, str):
        return visualization, 404
    else:
        return jsonify(visualization), 200


@visualizations_api.get('/data/<int:visualization_id>')
def get_visualization_data(visualization_id: int):
    visualization = visualizations_service.get_visualization_by_id(
        visualization_id)

    if isinstance(visualization, str):
        return visualization, 404

    if not os.path.exists(visualization['visualization_image_path']):
        return 'File path doesn\'t exists', 400

    df = pd.read_csv(visualization['visualization_image_path'])
    # return jsonify(df.to_json(orient='split')), 200
    return jsonify(df.to_dict()), 200


@visualizations_api.get('/download/<int:visualization_id>')
def download_analyze_by_id(visualization_id: int):
    visualization = visualizations_service.get_visualization_by_id(
        visualization_id)

    if isinstance(visualization, str):
        return visualization, 404

    if not os.path.exists(visualization['visualization_image_path']):
        return 'File path doesn\'t exists', 400

    file_name = os.path.basename(visualization['visualization_image_path'])
    return send_from_directory(VISUALIZATIONS_UPLOAD_FOLDER, file_name, file_name, as_attachment=True)


@visualizations_api.post('/')
def create_visualization():
    visualization_image_path = 'None'
    visualization_name = request.json['visualization_name']
    report_id = request.json['report_id']
    visualization = Visualizations(visualization_name=visualization_name,
                                   visualization_image_path=visualization_image_path, report_id=report_id)
    created_visualization = visualizations_service.create_visualization(
        visualization)

    if isinstance(created_visualization, str):
        return created_visualization, 400
    else:
        return jsonify(created_visualization), 201


@visualizations_api.put('/<int:visualization_id>')
def update_visualization(visualization_id: int):
    visualization_image_path = 'None'
    visualization_name = request.json['visualization_name']
    report_id = request.json['report_id']
    visualization = Visualizations(visualization_name=visualization_name,
                                   visualization_image_path=visualization_image_path, report_id=report_id)
    updated_visualization = visualizations_service.update_visualization(
        visualization_id, visualization)

    if isinstance(updated_visualization, str):
        return updated_visualization, 400
    else:
        return jsonify(updated_visualization), 201


@visualizations_api.delete('/<int:visualization_id>')
def delete_role(visualization_id: int):
    deleted_visualization = visualizations_service.delete_visualization(
        visualization_id)

    if isinstance(deleted_visualization, str):
        return deleted_visualization, 400
    else:
        return jsonify(deleted_visualization), 200
