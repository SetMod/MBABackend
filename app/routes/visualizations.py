import os
import pandas as pd
from flask import Blueprint, jsonify, request, send_from_directory
from app import VISUALIZATIONS_UPLOAD_FOLDER
from app.models import Visualizations
from app.services import VisualizationsService

visualizations_api = Blueprint("visualizations", __name__)
visualizations_service = VisualizationsService()


@visualizations_api.get("/")
def get_all_visualizations():
    visualizations = visualizations_service.get_all_visualizations()

    if isinstance(visualizations, str):
        return visualizations, 404
    else:
        return jsonify(visualizations), 200


@visualizations_api.get("/<int:id>")
def get_visualization_by_id(id: int):
    visualization = visualizations_service.get_visualization_by_id(id)

    if isinstance(visualization, str):
        return visualization, 404
    else:
        return jsonify(visualization), 200


@visualizations_api.get("/data/<int:id>")
def get_visualization_data(id: int):
    visualization = visualizations_service.get_visualization_by_id(id)

    if isinstance(visualization, str):
        return visualization, 404

    if not os.path.exists(visualization["image_file_path"]):
        return "File path doesn't exists", 400

    df = pd.read_csv(visualization["image_file_path"])
    # return jsonify(df.to_json(orient='split')), 200
    return jsonify(df.to_dict()), 200


@visualizations_api.get("/download/<int:id>")
def download_analyze_by_id(id: int):
    visualization = visualizations_service.get_visualization_by_id(id)

    if isinstance(visualization, str):
        return visualization, 404

    if not os.path.exists(visualization["image_file_path"]):
        return "File path doesn't exists", 400

    name = os.path.basename(visualization["image_file_path"])
    return send_from_directory(
        VISUALIZATIONS_UPLOAD_FOLDER, name, name, as_attachment=True
    )


@visualizations_api.post("/")
def create_visualization():
    image_file_path = "None"
    name = request.json["name"]
    report_id = request.json["report_id"]
    visualization = Visualizations(
        name=name, image_file_path=image_file_path, report_id=report_id
    )
    created_visualization = visualizations_service.create_visualization(visualization)

    if isinstance(created_visualization, str):
        return created_visualization, 400
    else:
        return jsonify(created_visualization), 201


@visualizations_api.put("/<int:id>")
def update_visualization(id: int):
    image_file_path = "None"
    name = request.json["name"]
    report_id = request.json["report_id"]
    visualization = Visualizations(
        name=name, image_file_path=image_file_path, report_id=report_id
    )
    updated_visualization = visualizations_service.update_visualization(
        id, visualization
    )

    if isinstance(updated_visualization, str):
        return updated_visualization, 400
    else:
        return jsonify(updated_visualization), 201


@visualizations_api.delete("/<int:id>")
def delete_role(id: int):
    deleted_visualization = visualizations_service.delete_visualization(id)

    if isinstance(deleted_visualization, str):
        return deleted_visualization, 400
    else:
        return jsonify(deleted_visualization), 200
