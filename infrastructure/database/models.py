"""
SQLAlchemy models cho Union Management System
Chỉ hỗ trợ PostgreSQL database
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, Float
from sqlalchemy.sql import func
from infrastructure.database.connection import Base
from domain.entities.member import MemberType, MemberStatus
from domain.entities.report import ReportType, ReportStatus
from domain.entities.task import TaskPriority, TaskStatus


class MemberModel(Base):
    """SQLAlchemy model cho Member"""
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(DateTime)
    gender = Column(String(10))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    position = Column(String(100))
    department = Column(String(100))
    member_type = Column(SQLEnum(MemberType), nullable=False, default=MemberType.UNION_MEMBER)
    status = Column(SQLEnum(MemberStatus), nullable=False, default=MemberStatus.ACTIVE)
    join_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class ReportModel(Base):
    """SQLAlchemy model cho Report"""
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    report_type = Column(SQLEnum(ReportType), nullable=False, default=ReportType.MONTHLY)
    period = Column(String(20), nullable=False, index=True)
    content = Column(Text)
    attachments = Column(Text)  # JSON string
    status = Column(SQLEnum(ReportStatus), nullable=False, default=ReportStatus.DRAFT)
    created_by = Column(Integer)  # ID của người tạo báo cáo
    submitted_by = Column(Integer)  # Foreign key sẽ được thêm sau
    submitted_at = Column(DateTime)
    approved_by = Column(Integer)  # Foreign key sẽ được thêm sau
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class TaskModel(Base):
    """SQLAlchemy model cho Task"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    priority = Column(SQLEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED)
    assigned_to = Column(Integer)  # Foreign key sẽ được thêm sau
    assigned_by = Column(Integer)  # Foreign key sẽ được thêm sau
    start_date = Column(DateTime)
    due_date = Column(DateTime, index=True)
    completed_date = Column(DateTime)
    estimated_hours = Column(Float, default=0.0)
    actual_hours = Column(Float, default=0.0)
    progress_percentage = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)