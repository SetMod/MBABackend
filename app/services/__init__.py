from app import db
from app.models import *

from app.services.RolesService import RolesService
from app.services.OrganizationRolesService import OrganizationRolesService
from app.services.UsersOrganizationsService import UsersOrganizationsService
from app.services.VisualizationsService import VisualizationsService
from app.services.FilesService import FilesService
from app.services.UsersService import UsersService
from app.services.OrganizationsService import OrganizationsService
from app.services.AnalyzesService import AnalyzesService
from app.services.ReportsService import ReportsService


# Organizations.__table__.drop(db.engine)
# UsersOrganizations.__table__.drop(db.engine)
# db.drop_all()

db.create_all()
