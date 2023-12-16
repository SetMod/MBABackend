from sqlalchemy import (
    ForeignKeyConstraint,
    Index,
    ForeignKey,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    Boolean,
    Enum,
    UniqueConstraint,
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from model.MBAnalyze import Algorithm
from app.db import db
from typing import List
import enum


class Roles(enum.Enum):
    ADMIN = "Admin"
    USER = "User"


class OrganizationRoles(enum.Enum):
    OWNER = "Owner"
    ADMIN = "Admin"
    EDITOR = "EDITOR"
    VIEWER = "Viewer"


class DatasourceTypes(enum.Enum):
    FILE = "File"
    DB = "DB"

    # CSV = "CSV"
    # SQLITE = "SQLite"
    # MYSQL = "MySQL"
    # POSTGRESQL = "PostgreSQL"


class ReportTypes(enum.Enum):
    GENERIC = "generic"


class VisualizationTypes(enum.Enum):
    FILE = "file"
    DATA_POINTS = "data points"


class AnalyzeStatus(enum.Enum):
    NOT_STARTED = "Not started"
    STARTED = "Started"
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In progress"
    FINISHED = "Finished"
    FAILED = "Failed"


class GenericModel(db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, nullable=False)

    created_date: Mapped[datetime] = mapped_column(
        "created_date",
        DateTime,
        default=datetime.utcnow,
    )

    updated_date: Mapped[datetime] = mapped_column(
        "updated_date", DateTime, nullable=True
    )

    deleted_date: Mapped[datetime] = mapped_column(
        "deleted_date", DateTime, nullable=True
    )

    soft_deleted: Mapped[bool] = mapped_column("soft_deleted", Boolean, default=False)

    @classmethod
    def _name(cls, lower: bool = True, many: bool = False):
        model_name = cls.__name__
        if lower:
            model_name = model_name.lower()
        if not many:
            model_name = model_name[:-1]
        return model_name

    def _get_generic_repr(self):
        return f"created_date='{self.created_date}',updated_date='{self.updated_date}',deleted_date='{self.deleted_date}',soft_deleted='{self.soft_deleted}'"


class OrganizationMembers(GenericModel):
    __tablename__ = "organization_members"

    user_id: Mapped[int] = mapped_column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    organization_id: Mapped[int] = mapped_column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[OrganizationRoles] = mapped_column(
        "role",
        Enum(OrganizationRoles),
        default=OrganizationRoles.VIEWER,
        nullable=False,
    )
    active: Mapped[bool] = mapped_column(
        "active", Boolean, default=True, nullable=False
    )

    user: Mapped["Users"] = relationship("Users", back_populates="memberships")
    organization: Mapped["Organizations"] = relationship(
        "Organizations", back_populates="memberships"
    )
    reports: Mapped[List["Reports"]] = relationship("Reports", back_populates="creator")
    datasources: Mapped[List["Datasources"]] = relationship(
        "Datasources", back_populates="creator"
    )
    analyzes: Mapped[List["Analyzes"]] = relationship(
        "Analyzes", back_populates="creator"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_id",
            name="organization_member_unique_user_id_and_organization_id_combination_constraint",
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="organization_member_user_id_constraint"
        ),
        ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="organization_member_organization_id_constraint",
        ),
        # Index for the combination (optional but can improve performance for queries using this combination)
        Index(
            "unique_combination_index",
            "organization_id",
            "organization_id",
            "id",
        ),
    )

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',user_id='{self.user_id}',organization_id='{self.organization_id}',role='{self.role}',active='{self.active}',{self._get_generic_repr()})>"


class Users(GenericModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column("first_name", String(100), nullable=False)
    second_name: Mapped[str] = mapped_column("second_name", String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        "email", String(250), unique=True, nullable=False
    )
    phone: Mapped[str] = mapped_column("phone", String(18), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        "username", String(50), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        "password_hash", String(200), nullable=False
    )
    active: Mapped[bool] = mapped_column(
        "active", Boolean, default=True, nullable=False
    )
    last_login_date: Mapped[datetime] = mapped_column(
        "last_login_date", DateTime, nullable=True
    )
    role: Mapped[Roles] = mapped_column(
        "role", Enum(Roles), default=Roles.USER, nullable=False
    )

    memberships: Mapped[List["OrganizationMembers"]] = relationship(
        "OrganizationMembers",
        back_populates="user",
        cascade="all, delete",
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',first_name='{self.first_name}',second_name='{self.second_name}',email='{self.email}',phone='{self.phone}',username='{self.username}',role='{self.role}',{self._get_generic_repr()})>"


class Organizations(GenericModel):
    __tablename__ = "organizations"

    name = mapped_column("name", String(200), unique=True, nullable=False)
    description = mapped_column("description", Text, nullable=False)
    email = mapped_column("email", String(255), unique=True, nullable=False)
    phone = mapped_column("phone", String(18), unique=True)
    memberships: Mapped[List["OrganizationMembers"]] = relationship(
        "OrganizationMembers",
        back_populates="organization",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',description='{self.description}',email='{self.email}',phone='{self.phone}',{self._get_generic_repr()})>"


class FileDatasourcesMixin:
    file_path: Mapped[str] = mapped_column(
        "file_path", String(255), unique=True, nullable=True
    )
    file_name: Mapped[str] = mapped_column(
        "file_name", String(250), unique=False, nullable=True
    )
    file_size: Mapped[int] = mapped_column(
        "file_size", Integer, unique=False, nullable=True
    )


class Datasources(GenericModel, FileDatasourcesMixin):
    __tablename__ = "datasources"

    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    type: Mapped[DatasourceTypes] = mapped_column(
        "type", Enum(DatasourceTypes), default=DatasourceTypes.FILE, nullable=False
    )
    creator_id: Mapped[int] = mapped_column(
        "creator_id",
        Integer,
        ForeignKey("organization_members.id"),
        nullable=True,
    )
    analyzes: Mapped[List["Analyzes"]] = relationship(
        "Analyzes",
        back_populates="datasource",
        cascade="all, delete",
    )
    creator: Mapped[OrganizationMembers] = relationship(
        OrganizationMembers, back_populates=__tablename__
    )

    # __mapper_args__ = {
    #     "polymorphic_on": type,
    #     "polymorphic_identity": __tablename__,
    # }

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',type='{self.type}',creator_id='{self.creator_id}',{self._get_generic_repr()})>"


# class FileDatasources(Datasources):
#     __mapper_args__ = {"polymorphic_identity": DatasourceTypes.FILE}

#     file_path: Mapped[str] = mapped_column(
#         "file_path", String(255), unique=True, nullable=True
#     )
#     file_name: Mapped[str] = mapped_column(
#         "file_name", String(250), unique=False, nullable=True
#     )
#     file_size: Mapped[int] = mapped_column(
#         "file_size", Integer, unique=False, nullable=True
#     )

#     def __repr__(self):
#         return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',creator_id='{self.creator_id}',file_path='{self.file_path}',file_name='{self.file_name}',file_size='{self.file_size}',{self._get_generic_repr()})>"


class Reports(GenericModel):
    __tablename__ = "reports"

    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    type: Mapped[ReportTypes] = mapped_column(
        "type", Enum(ReportTypes), default=ReportTypes.GENERIC, nullable=False
    )
    creator_id: Mapped[int] = mapped_column(
        "creator_id",
        Integer,
        ForeignKey("organization_members.id"),
        nullable=True,
    )
    creator: Mapped[OrganizationMembers] = relationship(
        OrganizationMembers, back_populates=__tablename__
    )

    visualizations: Mapped[List["Visualizations"]] = relationship(
        "Visualizations", back_populates="report"
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',type='{self.type}',creator_id='{self.creator_id}',{self._get_generic_repr()})>"


class GenericReports(Reports):
    __mapper_args__ = {"polymorphic_identity": ReportTypes.GENERIC}

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',type='{self.type}',creator_id='{self.creator_id}',{self._get_generic_repr()})>"


class Visualizations(GenericModel):
    __tablename__ = "visualizations"

    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    type: Mapped[VisualizationTypes] = mapped_column(
        "type",
        Enum(VisualizationTypes),
        default=VisualizationTypes.FILE,
        nullable=False,
    )
    report_id: Mapped[int] = mapped_column(
        "report_id", Integer, ForeignKey("reports.id"), nullable=False
    )
    report: Mapped["Reports"] = relationship("Reports", back_populates=__tablename__)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": __tablename__,
    }

    def __repr__(self) -> str:
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',report_id='{self.report_id}',{self._get_generic_repr()})>"


class FileVisualizations(Visualizations):
    __mapper_args__ = {"polymorphic_identity": VisualizationTypes.FILE}

    file_path: Mapped[str] = mapped_column("file_path", String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',file_path='{self.file_path}',{self._get_generic_repr()})>"


class DataVisualizations(FileVisualizations):
    __mapper_args__ = {"polymorphic_identity": VisualizationTypes.DATA_POINTS}

    data_points: Mapped[str] = mapped_column("data_points", Text, nullable=True)

    def __repr__(self) -> str:
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',file_path='{self.file_path}',{self._get_generic_repr()})>"


class Analyzes(GenericModel):
    __tablename__ = "analyzes"

    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    description: Mapped[str] = mapped_column("description", Text, nullable=False)
    support: Mapped[float] = mapped_column("support", Float, nullable=False)
    lift: Mapped[float] = mapped_column("lift", Float, nullable=False)
    confidence: Mapped[float] = mapped_column("confidence", Float, nullable=False)
    rules_length: Mapped[int] = mapped_column("rules_length", Integer, nullable=False)
    file_path: Mapped[str] = mapped_column("file_path", String(255), nullable=False)
    algorithm: Mapped[Algorithm] = mapped_column(
        "algorithm", Enum(Algorithm), nullable=False
    )
    status: Mapped[AnalyzeStatus] = mapped_column(
        "status", Enum(AnalyzeStatus), nullable=False
    )
    started_date: Mapped[datetime] = mapped_column(
        "started_date", DateTime, default=datetime.utcnow, nullable=True
    )
    finished_date: Mapped[datetime] = mapped_column(
        "finished_date", DateTime, default=datetime.utcnow, nullable=True
    )
    datasource_id: Mapped[int] = mapped_column(
        "datasource_id",
        Integer,
        ForeignKey("datasources.id"),
        nullable=False,
    )
    creator_id: Mapped[int] = mapped_column(
        "creator_id", ForeignKey("organization_members.id"), nullable=True
    )
    creator: Mapped[OrganizationMembers] = relationship(
        OrganizationMembers, back_populates=__tablename__
    )
    datasource: Mapped[Datasources] = relationship(
        Datasources, back_populates=__tablename__
    )
    # report: Mapped["Reports"] = relationship("Reports", back_populates="analyzes")

    def __repr__(self):
        return f"<{self._name(lower=False)}(id='{self.id}',name='{self.name}',support='{self.support}',lift='{self.lift}',confidence='{self.confidence}',rules_length='{self.rules_length}',datasource_id='{self.datasource_id}',{self._get_generic_repr()})>"
