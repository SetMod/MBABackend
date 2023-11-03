from app import app
from app.routes import (
    roles_api,
    organization_roles_api,
    organizations_api,
    users_api,
    users_organizations_api,
    files_api,
    reports_api,
    analyzes_api,
    visualizations_api,
)


app.register_blueprint(roles_api, url_prefix="/api/roles")
app.register_blueprint(organization_roles_api, url_prefix="/api/organization_roles")
app.register_blueprint(organizations_api, url_prefix="/api/organizations")
app.register_blueprint(users_api, url_prefix="/api/users")
app.register_blueprint(users_organizations_api, url_prefix="/api/users_organizations")
app.register_blueprint(files_api, url_prefix="/api/files")
app.register_blueprint(reports_api, url_prefix="/api/reports")
app.register_blueprint(analyzes_api, url_prefix="/api/analyzes")
app.register_blueprint(visualizations_api, url_prefix="/api/visualizations")

if __name__ == "__main__":
    host = "localhost"
    port = 8000
    debug = True
    app.run(host, port, debug)
