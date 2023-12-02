from flask import Flask
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.routes.organizations import organizations_bp
from app.routes.organization_members import organization_members_bp
from app.routes.members import members_bp
from app.routes.reports import reports_bp
from app.routes.datasources import datasources_bp
from app.routes.visualizations import visualizations_bp
from app.routes.analyzes import analyzes_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix="/api/v1/users/auth")
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    app.register_blueprint(organizations_bp, url_prefix="/api/v1/organizations")
    app.register_blueprint(
        organization_members_bp,
        url_prefix="/api/v1/organizations/<int:org_id>/members",
    )
    app.register_blueprint(members_bp, url_prefix="/api/v1/members")
    app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")
    app.register_blueprint(datasources_bp, url_prefix="/api/v1/datasources")
    # # app.register_blueprint(files_api, url_prefix="/api/v1/files")
    app.register_blueprint(visualizations_bp, url_prefix="/api/v1/visualizations")
    app.register_blueprint(analyzes_bp, url_prefix="/api/v1/analyzes")
