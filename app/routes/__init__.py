from app.routes.roles import roles_api
from app.routes.organization_roles import organization_roles_api
from app.routes.users_organizations import users_organizations_api
from app.routes.users import users_api
from app.routes.organizations import organizations_api
from app.routes.analyzes import analyzes_api
from app.routes.files import files_api
from app.routes.reports import reports_api
from app.routes.visualizations import visualizations_api
from app.init import app

app.register_blueprint(roles_api, url_prefix="/api/v1/roles")
app.register_blueprint(organization_roles_api, url_prefix="/api/v1/organization_roles")
app.register_blueprint(organizations_api, url_prefix="/api/v1/organizations")
app.register_blueprint(users_api, url_prefix="/api/v1/users")
app.register_blueprint(
    users_organizations_api, url_prefix="/api/v1/users_organizations"
)
app.register_blueprint(files_api, url_prefix="/api/v1/files")
app.register_blueprint(reports_api, url_prefix="/api/v1/reports")
app.register_blueprint(analyzes_api, url_prefix="/api/v1/analyzes")
app.register_blueprint(visualizations_api, url_prefix="/api/v1/visualizations")
