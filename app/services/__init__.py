from app.services.GenericService import GenericService
from app.services.OrganizationMembersService import OrganizationMembersService
from app.services.UsersService import UsersService
from app.services.OrganizationsService import OrganizationsService
from app.services.AnalyzesService import AnalyzesService
from app.services.DatasourcesService import DatasourcesService
from app.services.VisualizationsService import VisualizationsService
from app.services.FileVisualizationsService import FileVisualizationsService
from app.services.ReportsService import ReportsService

organization_members_service = OrganizationMembersService()
users_service = UsersService()
organizations_service = OrganizationsService()
analyzes_service = AnalyzesService()
datasources_service = DatasourcesService()
visualizations_service = VisualizationsService()
file_visualizations_service = FileVisualizationsService()
reports_service = ReportsService()
