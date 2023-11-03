# from db.database import engine, Base
# from .RolesSchema import Base as RoleBase
# from .UsersSchema import Base as UserBase
# from .UsersOrganizationsSchema import Base as UsersOrganizationsBase
# from .OrganizationsSchema import Base as OrganizationsBase
# from .OrganizationRolesSchema import Base as OrganizationRolesBase
# from .AnalyzesSchema import Base as AnalyzesBase
# from .FilesSchema import Base as FilesBase
# from .ReportsSchema import Base as ReportsBase
# from .VisualizationsSchema import Base as VisualizationsBase

# Base.metadata.create_all(engine)

from app.models.Roles import Roles, RolesSchema
from app.models.OrganizationRoles import OrganizationRoles, OrganizationRolesSchema
from app.models.UsersOrganizations import UsersOrganizations, UsersOrganizationsSchema
from app.models.Organizations import Organizations, OrganizationsSchema
from app.models.Users import Users, UsersSchema
from app.models.Reports import Reports, ReportsSchema
from app.models.Analyzes import Analyzes, AnalyzesSchema
from app.models.Files import Files, FilesSchema
from app.models.Visualizations import Visualizations, VisualizationsSchema
