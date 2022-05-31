from app import app
from routes.roles import roles_api
from routes.organization_roles import organization_roles_api
from routes.organizations import organizations_api
from routes.users import users_api
from routes.users_organizations import users_organizations_api
from routes.files import files_api
from routes.reports import reports_api
from routes.analyzes import analyzes_api
from routes.visualizations import visualizations_api


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
