from flask import Flask
from app.routes.RolesRoute import RolesRoute
from app.routes.OrganizationRolesRoute import OrganizationRolesRoute
from app.routes.UsersRoute import UsersRoute
from app.routes.OrganizationsRoute import OrganizationsRoute
from app.routes.ReportsRoute import ReportsRoute
from app.routes.DatasourcesRoute import DatasourcesRoute
from app.routes.VisualizationsRoute import VisualizationsRoute


def register_blueprints(app: Flask):
    roles_route = RolesRoute()
    organization_roles_route = OrganizationRolesRoute()
    users_route = UsersRoute()
    organizations_route = OrganizationsRoute()
    reports_route = ReportsRoute()
    datasources_route = DatasourcesRoute()
    visualizations_route = VisualizationsRoute()

    app.register_blueprint(roles_route.bp, url_prefix="/api/v1/roles")
    app.register_blueprint(organizations_route.bp, url_prefix="/api/v1/organizations")
    # # app.register_blueprint(organizations_members_api, url_prefix="/api/v1/organizations/<int:id>/members",)
    app.register_blueprint(
        organization_roles_route.bp,
        url_prefix="/api/v1/organizations/<int:org_id>/roles",
    )
    app.register_blueprint(users_route.bp, url_prefix="/api/v1/users")
    app.register_blueprint(reports_route.bp, url_prefix="/api/v1/reports")
    app.register_blueprint(datasources_route.bp, url_prefix="/api/v1/datasource")
    # # app.register_blueprint(files_api, url_prefix="/api/v1/files")
    app.register_blueprint(visualizations_route.bp, url_prefix="/api/v1/visualizations")
    # app.register_blueprint(analyzes_api, url_prefix="/api/v1/analyzes")
