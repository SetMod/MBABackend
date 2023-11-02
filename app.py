from app import app
from app.routes.roles import roles_api
from app.routes.organization_roles import organization_roles_api
from app.routes.organizations import organizations_api
from app.routes.users import users_api
from app.routes.users_organizations import users_organizations_api
from app.routes.files import files_api
from app.routes.reports import reports_api
from app.routes.analyzes import analyzes_api
from app.routes.visualizations import visualizations_api


app.register_blueprint(roles_api, url_prefix='/api/roles')
app.register_blueprint(organization_roles_api,
                       url_prefix='/api/organization_roles')
app.register_blueprint(organizations_api, url_prefix='/api/organizations')
app.register_blueprint(users_api, url_prefix='/api/users')
app.register_blueprint(users_organizations_api,
                       url_prefix='/api/users_organizations')
app.register_blueprint(files_api, url_prefix='/api/files')
app.register_blueprint(reports_api, url_prefix='/api/reports')
app.register_blueprint(analyzes_api, url_prefix='/api/analyzes')
app.register_blueprint(visualizations_api, url_prefix='/api/visualizations')

if __name__ == "__main__":
    host = 'localhost'
    port = 8000
    debug = True
    app.run(host, port, debug)
