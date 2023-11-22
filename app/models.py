from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    Boolean,
    Enum,
    inspect,
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.logger import logger
from app.db import db, Base
from typing import List
import enum


class DatasourceTypes(enum.Enum):
    FILE = "file"
    DB = "db"

    CSV = "CSV"
    SQLITE = "SQLite"
    MYSQL = "MySQL"
    POSTGRESQL = "PostgreSQL"


class ReportTypes(enum.Enum):
    GENERIC = "generic"


class VisualizationTypes(enum.Enum):
    FILE = "file"
    DATA_POINTS = "data points"


class AnalyzeStatus(enum.Enum):
    SCHEDULED = "scheduled"
    STARTED = "started"
    IN_PROGRESS = "in progress"
    FINISHED = "finished"
    FAILED = "failed"


class GenericModel(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)

    created_date: Mapped[datetime] = mapped_column(
        "created_date", DateTime, default=datetime.utcnow
    )

    updated_date: Mapped[datetime] = mapped_column(
        "updated_date", DateTime, nullable=True
    )

    deleted_date: Mapped[datetime] = mapped_column(
        "deleted_date", DateTime, nullable=True
    )

    soft_deleted: Mapped[bool] = mapped_column("soft_deleted", Boolean, default=False)

    @classmethod
    def _get_unique_fields(cls, model_dict: dict):
        unique_fields = {}
        for column in inspect(cls).columns:
            if column.unique:
                column_name = str(column).split(".")[1]  # Extracting column name
                if column_name in model_dict:
                    unique_fields[column_name] = model_dict[column_name]

        logger.info(f"{cls.__name__[:-1]} unique fields: {unique_fields}")
        return unique_fields

    updatable_fields: list = []

    @classmethod
    def _name(cls, lower: bool = True, many: bool = False):
        model_name = cls.__name__
        if lower:
            model_name = model_name.lower()
        if not many:
            model_name = model_name[:-1]
        return model_name

    def _get_generic_repr(self):
        return f"created_date={self.created_date},updated_date={self.updated_date},deleted_date={self.deleted_date},soft_deleted={self.soft_deleted}"


organization_members = Table(
    "organization_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("organization_id", ForeignKey("organizations.id")),
    Column("organization_role_id", ForeignKey("organization_roles.id")),
    Column("active", Boolean, default=True, nullable=False),
)


class Roles(GenericModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column("name", String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column("description", Text, nullable=False)
    users: Mapped[List["Users"]] = relationship(back_populates="role")

    updatable_fields = [
        "name",
        "description",
    ]

    def __repr__(self):
        return f"<Role(id={self.id},name={self.name},description={self.description},{self._get_generic_repr()})>"


class Users(GenericModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column("first_name", String(100), nullable=False)
    second_name: Mapped[str] = mapped_column("second_name", String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        "email", String(255), unique=True, nullable=False
    )
    phone: Mapped[str] = mapped_column("phone", String(18), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        "username", String(50), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        "password_hash", String(50), nullable=False
    )
    active: Mapped[bool] = mapped_column(
        "active", Boolean, default=True, nullable=False
    )
    last_login_date: Mapped[datetime] = mapped_column(
        "last_login_date", DateTime, nullable=True
    )
    role_id: Mapped[int] = mapped_column(
        "role_id", Integer, ForeignKey("roles.id"), nullable=False
    )
    role: Mapped["Roles"] = relationship("Roles", back_populates="users")

    organizations: Mapped[List["Organizations"]] = relationship(
        secondary=organization_members,
        back_populates="members",
        cascade="save-update, merge, delete",
    )

    reports: Mapped[List["Reports"]] = relationship("Reports", back_populates="user")
    datasources: Mapped[List["Datasources"]] = relationship(
        "Datasources", back_populates="user"
    )

    updatable_fields = [
        "first_name",
        "second_name",
        "email",
        "phone",
        "username",
        "password_hash",
        "active",
        "role_id",
    ]

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(id={self.id},first_name={self.first_name},second_name={self.second_name},email={self.email},phone={self.phone},username={self.username},role_id={self.role_id},{self._get_generic_repr()})>"


class OrganizationRoles(GenericModel):
    __tablename__ = "organization_roles"

    name: Mapped[str] = mapped_column("name", String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column("description", Text, nullable=False)

    def __repr__(self):
        return f"<OrganizationRole(id={self.id},name={self.name},description={self.description},{self._get_generic_repr()})>"


class Organizations(GenericModel):
    __tablename__ = "organizations"

    name = mapped_column("name", String(200), unique=True, nullable=False)
    description = mapped_column("description", Text, nullable=False)
    email = mapped_column("email", String(255), unique=True, nullable=False)
    phone = mapped_column("phone", String(18), unique=True)
    members: Mapped[List[Users]] = relationship(
        secondary=organization_members,
        back_populates="organizations",
        cascade="save-update, merge, delete",
    )
    reports: Mapped[List["Reports"]] = relationship(
        "Reports", back_populates="organization"
    )
    datasources: Mapped[List["Datasources"]] = relationship(
        "Datasources", back_populates="organization"
    )

    updatable_fields = [
        "name",
        "description",
        "email",
        "phone",
    ]

    def __repr__(self):
        return f"<Organization(id={self.id},name={self.name},description={self.description},email={self.email},phone={self.phone},{self._get_generic_repr()})>"


class Datasources(GenericModel):
    __tablename__ = "datasources"

    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    type: Mapped[DatasourceTypes] = mapped_column(
        "type", Enum(DatasourceTypes), nullable=False
    )
    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("users.id"))
    user: Mapped["Users"] = relationship("Users", back_populates="datasources")
    organization_id: Mapped[int] = mapped_column(
        "organization_id", Integer, ForeignKey("organizations.id"), nullable=False
    )
    organization: Mapped["Organizations"] = relationship(
        "Organizations", back_populates="datasources"
    )

    updatable_fields = [
        "name",
        "type",
    ]

    def __repr__(self):
        return f"<Report(id={self.id},name={self.name},user_id={self.user_id},organization_id={self.organization_id},{self._get_generic_repr()})>"


class FileDatasources(GenericModel):
    __tablename__ = "file_datasources"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(
        "file_path", String(255), unique=True, nullable=False
    )
    datasource_id: Mapped[int] = mapped_column(
        "datasource_id", Integer, ForeignKey("datasources.id")
    )
    # datasource: Mapped["Users"] = relationship("Users", back_populates="file_datasources")

    updatable_fields = [
        "name",
        "file_path",
    ]

    def __repr__(self):
        return f"<File(id={self.id},name={self.name},user_id={self.user_id},organization_id={self.organization_id},file_path={self.file_path},{self._get_generic_repr()})>"


class Reports(GenericModel):
    __tablename__ = "reports"

    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    type: Mapped[ReportTypes] = mapped_column(
        "type", Enum(ReportTypes), default=ReportTypes.GENERIC, nullable=False
    )
    user_id: Mapped[int] = mapped_column("user_id", Integer, ForeignKey("users.id"))
    user: Mapped["Users"] = relationship("Users", back_populates="reports")
    organization_id: Mapped[int] = mapped_column(
        "organization_id", Integer, ForeignKey("organizations.id"), nullable=False
    )
    organization: Mapped["Organizations"] = relationship(
        "Organizations", back_populates="reports"
    )
    visualizations: Mapped[List["Visualizations"]] = relationship(
        "Visualizations", back_populates="report"
    )

    updatable_fields = [
        "name",
        "type",
    ]

    def __repr__(self):
        return f"<Report(id={self.id},name={self.name},user_id={self.user_id},organization_id={self.organization_id},{self._get_generic_repr()})>"


class Visualizations(GenericModel):
    __tablename__ = "visualizations"

    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    type: Mapped[VisualizationTypes] = mapped_column(
        "type", Enum(VisualizationTypes), nullable=False
    )
    report_id: Mapped[int] = mapped_column(
        "report_id", Integer, ForeignKey("reports.id"), nullable=False
    )
    report: Mapped["Reports"] = relationship("Reports", back_populates="visualizations")

    updatable_fields = [
        "name",
        "type",
    ]

    def __repr__(self) -> str:
        return f"Visualization(id={self.id},name={self.name},report_id={self.report_id},{self._get_generic_repr()})"


class FileVisualizations(GenericModel):
    __tablename__ = "file_visualizations"

    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    file_path: Mapped[str] = mapped_column("file_path", String(255), nullable=False)
    visualization_id: Mapped[int] = mapped_column(
        "visualization_id", Integer, ForeignKey("visualizations.id"), nullable=False
    )
    # visualization: Mapped["visualizations"] = relationship("visualizations", back_populates="visualizations")

    updatable_fields = [
        "name",
        "file_path",
    ]

    def __repr__(self) -> str:
        return f"Visualization(id={self.id},name={self.name},file_path={self.file_path},visualization_id={self.visualization_id},{self._get_generic_repr()})"


class DataVisualizations(GenericModel):
    __tablename__ = "data_visualizations"

    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    type: Mapped[str] = mapped_column("type", Text, nullable=False)
    file_path: Mapped[str] = mapped_column("file_path", String(255), nullable=False)
    data_points: Mapped[str] = mapped_column("data_points", Text, nullable=False)
    visualization_id: Mapped[int] = mapped_column(
        "visualization_id", Integer, ForeignKey("visualizations.id"), nullable=False
    )
    # visualization: Mapped["visualizations"] = relationship("visualizations", back_populates="visualizations")

    updatable_fields = [
        "name",
        "type",
        "file_path",
        "data_points",
    ]

    def __repr__(self) -> str:
        return f"Visualization(id={self.id},name={self.name},file_path={self.file_path},visualization_id={self.visualization_id},{self._get_generic_repr()})"


class Analyzes(GenericModel):
    __tablename__ = "analyzes"

    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    description: Mapped[str] = mapped_column("description", Text, nullable=False)
    support: Mapped[float] = mapped_column("support", Float, nullable=False)
    lift: Mapped[float] = mapped_column("lift", Float, nullable=False)
    confidence: Mapped[float] = mapped_column("confidence", Float, nullable=False)
    rules_length: Mapped[int] = mapped_column("rules_length", Integer, nullable=False)
    file_path: Mapped[str] = mapped_column("file_path", String(255), nullable=False)
    status: Mapped[str] = mapped_column("status", Enum(AnalyzeStatus), nullable=False)
    started_date: Mapped[datetime] = mapped_column(
        "started_date", DateTime, default=datetime.utcnow
    )
    finished_date: Mapped[datetime] = mapped_column(
        "finished_date", DateTime, default=datetime.utcnow
    )
    report_id: Mapped[int] = mapped_column(
        "report_id",
        Integer,
        ForeignKey("reports.id"),
        nullable=False,
    )
    # report: Mapped["Reports"] = relationship("Reports", back_populates="analyzes")

    updatable_fields = [
        "name",
        "description",
        "support",
        "lift",
        "confidence",
        "rules_length",
        "file_path",
    ]

    def __repr__(self):
        return f"<Analyze(id={self.id},name={self.name},support={self.support},lift={self.lift},confidence={self.confidence},rules_length={self.rules_length},report_id={self.report_id},{self._get_generic_repr()})>"
