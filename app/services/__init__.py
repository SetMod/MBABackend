from app import db
from app.models.RolesModel import Roles
from app.models.OrganizationRolesModel import OrganizationRoles
# from app.models.UsersOrganizationsModel import users_organizations_table
from app.models.UsersOrganizationsModel import UsersOrganizations
from app.models.UsersModel import Users
from app.models.OrganizationsModel import Organizations
from app.models.FilesModel import Files
from app.models.ReportsModel import Reports
from app.models.AnalyzesModel import Analyzes
from app.models.VisualizationsModel import Visualizations

# Organizations.__table__.drop(db.engine)
# UsersOrganizations.__table__.drop(db.engine)
# db.drop_all()

db.create_all()
