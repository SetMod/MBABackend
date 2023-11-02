from app import db
from models.RolesModel import Roles
from models.OrganizationRolesModel import OrganizationRoles
# from models.UsersOrganizationsModel import users_organizations_table
from models.UsersOrganizationsModel import UsersOrganizations
from models.UsersModel import Users
from models.OrganizationsModel import Organizations
from models.FilesModel import Files
from models.ReportsModel import Reports
from models.AnalyzesModel import Analyzes
from models.VisualizationsModel import Visualizations

# Organizations.__table__.drop(db.engine)
# UsersOrganizations.__table__.drop(db.engine)
# db.drop_all()

db.create_all()
