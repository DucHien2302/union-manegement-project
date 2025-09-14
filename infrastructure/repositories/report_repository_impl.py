from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from domain.entities.report import Report, ReportType, ReportStatus
from domain.repositories.report_repository import IReportRepository
from infrastructure.database.models import ReportModel
from infrastructure.database.connection import db_manager


class ReportRepository(IReportRepository):
    """Implementation của Report Repository"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def _model_to_entity(self, model: ReportModel) -> Report:
        """Chuyển đổi từ SQLAlchemy model sang Domain entity"""
        return Report(
            id=model.id,
            title=model.title,
            report_type=model.report_type,
            period=model.period,
            content=model.content,
            attachments=model.attachments,
            status=model.status,
            created_by=model.created_by,
            submitted_by=model.submitted_by,
            submitted_at=model.submitted_at,
            approved_by=model.approved_by,
            approved_at=model.approved_at,
            rejection_reason=model.rejection_reason,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Report) -> ReportModel:
        """Chuyển đổi từ Domain entity sang SQLAlchemy model"""
        return ReportModel(
            id=entity.id,
            title=entity.title,
            report_type=entity.report_type,
            period=entity.period,
            content=entity.content,
            attachments=entity.attachments,
            status=entity.status,
            created_by=entity.created_by,
            submitted_by=entity.submitted_by,
            submitted_at=entity.submitted_at,
            approved_by=entity.approved_by,
            approved_at=entity.approved_at,
            rejection_reason=entity.rejection_reason,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, report: Report) -> Report:
        """Tạo báo cáo mới"""
        session: Session = self.db_manager.get_session()
        try:
            model = self._entity_to_model(report)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_by_id(self, report_id: int) -> Optional[Report]:
        """Lấy báo cáo theo ID"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(ReportModel).filter(ReportModel.id == report_id).first()
            return self._model_to_entity(model) if model else None
        finally:
            session.close()
    
    def get_all(self) -> List[Report]:
        """Lấy tất cả báo cáo"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_type(self, report_type: ReportType) -> List[Report]:
        """Lấy báo cáo theo loại"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).filter(
                ReportModel.report_type == report_type
            ).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_status(self, status: ReportStatus) -> List[Report]:
        """Lấy báo cáo theo trạng thái"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).filter(
                ReportModel.status == status
            ).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_period(self, period: str) -> List[Report]:
        """Lấy báo cáo theo kỳ"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).filter(
                ReportModel.period == period
            ).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_submitter(self, submitter_id: int) -> List[Report]:
        """Lấy báo cáo theo người nộp"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).filter(
                ReportModel.submitted_by == submitter_id
            ).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Report]:
        """Lấy báo cáo trong khoảng thời gian"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).filter(
                ReportModel.created_at >= start_date,
                ReportModel.created_at <= end_date
            ).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def search_by_title(self, title: str) -> List[Report]:
        """Tìm kiếm báo cáo theo tiêu đề"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(ReportModel).filter(
                ReportModel.title.contains(title)
            ).order_by(ReportModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def update(self, report: Report) -> Report:
        """Cập nhật báo cáo"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(ReportModel).filter(ReportModel.id == report.id).first()
            if not model:
                raise ValueError(f"Report with ID {report.id} not found")
            
            # Cập nhật các thuộc tính
            model.title = report.title
            model.report_type = report.report_type
            model.period = report.period
            model.content = report.content
            model.attachments = report.attachments
            model.status = report.status
            model.submitted_by = report.submitted_by
            model.submitted_at = report.submitted_at
            model.approved_by = report.approved_by
            model.approved_at = report.approved_at
            model.rejection_reason = report.rejection_reason
            model.updated_at = report.updated_at
            
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, report_id: int) -> bool:
        """Xóa báo cáo"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(ReportModel).filter(ReportModel.id == report_id).first()
            if not model:
                return False
            
            session.delete(model)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def count_by_status(self, status: ReportStatus) -> int:
        """Đếm số báo cáo theo trạng thái"""
        session: Session = self.db_manager.get_session()
        try:
            count = session.query(func.count(ReportModel.id)).filter(
                ReportModel.status == status
            ).scalar()
            return count or 0
        finally:
            session.close()