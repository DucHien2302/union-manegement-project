from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from domain.entities.task import Task, TaskPriority, TaskStatus
from domain.repositories.task_repository import ITaskRepository
from infrastructure.database.models import TaskModel
from infrastructure.database.connection import db_manager


class TaskRepository(ITaskRepository):
    """Implementation của Task Repository"""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def _model_to_entity(self, model: TaskModel) -> Task:
        """Chuyển đổi từ SQLAlchemy model sang Domain entity"""
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            priority=model.priority,
            status=model.status,
            assigned_to=model.assigned_to,
            assigned_by=model.assigned_by,
            start_date=model.start_date,
            due_date=model.due_date,
            completed_date=model.completed_date,
            estimated_hours=model.estimated_hours,
            actual_hours=model.actual_hours,
            progress_percentage=model.progress_percentage,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Task) -> TaskModel:
        """Chuyển đổi từ Domain entity sang SQLAlchemy model"""
        return TaskModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            priority=entity.priority,
            status=entity.status,
            assigned_to=entity.assigned_to,
            assigned_by=entity.assigned_by,
            start_date=entity.start_date,
            due_date=entity.due_date,
            completed_date=entity.completed_date,
            estimated_hours=entity.estimated_hours,
            actual_hours=entity.actual_hours,
            progress_percentage=entity.progress_percentage,
            notes=entity.notes,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, task: Task) -> Task:
        """Tạo công việc mới"""
        session: Session = self.db_manager.get_session()
        try:
            model = self._entity_to_model(task)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Lấy công việc theo ID"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            return self._model_to_entity(model) if model else None
        finally:
            session.close()
    
    def get_all(self) -> List[Task]:
        """Lấy tất cả công việc"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).order_by(TaskModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_assignee(self, assignee_id: int) -> List[Task]:
        """Lấy công việc theo người được giao"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).filter(
                TaskModel.assigned_to == assignee_id
            ).order_by(TaskModel.due_date.asc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_assigner(self, assigner_id: int) -> List[Task]:
        """Lấy công việc theo người giao việc"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).filter(
                TaskModel.assigned_by == assigner_id
            ).order_by(TaskModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_status(self, status: TaskStatus) -> List[Task]:
        """Lấy công việc theo trạng thái"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).filter(
                TaskModel.status == status
            ).order_by(TaskModel.due_date.asc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Lấy công việc theo mức độ ưu tiên"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).filter(
                TaskModel.priority == priority
            ).order_by(TaskModel.due_date.asc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_by_due_date_range(self, start_date: datetime, end_date: datetime) -> List[Task]:
        """Lấy công việc trong khoảng hạn hoàn thành"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).filter(
                and_(
                    TaskModel.due_date >= start_date,
                    TaskModel.due_date <= end_date
                )
            ).order_by(TaskModel.due_date.asc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def get_overdue_tasks(self) -> List[Task]:
        """Lấy công việc quá hạn"""
        session: Session = self.db_manager.get_session()
        try:
            now = datetime.now()
            models = session.query(TaskModel).filter(
                and_(
                    TaskModel.due_date < now,
                    TaskModel.status.notin_([TaskStatus.COMPLETED, TaskStatus.CANCELLED])
                )
            ).order_by(TaskModel.due_date.asc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def search_by_title(self, title: str) -> List[Task]:
        """Tìm kiếm công việc theo tiêu đề"""
        session: Session = self.db_manager.get_session()
        try:
            models = session.query(TaskModel).filter(
                TaskModel.title.contains(title)
            ).order_by(TaskModel.created_at.desc()).all()
            return [self._model_to_entity(model) for model in models]
        finally:
            session.close()
    
    def update(self, task: Task) -> Task:
        """Cập nhật công việc"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task.id).first()
            if not model:
                raise ValueError(f"Task with ID {task.id} not found")
            
            # Cập nhật các thuộc tính
            model.title = task.title
            model.description = task.description
            model.priority = task.priority
            model.status = task.status
            model.assigned_to = task.assigned_to
            model.assigned_by = task.assigned_by
            model.start_date = task.start_date
            model.due_date = task.due_date
            model.completed_date = task.completed_date
            model.estimated_hours = task.estimated_hours
            model.actual_hours = task.actual_hours
            model.progress_percentage = task.progress_percentage
            model.notes = task.notes
            model.updated_at = task.updated_at
            
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, task_id: int) -> bool:
        """Xóa công việc"""
        session: Session = self.db_manager.get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task_id).first()
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
    
    def count_by_status(self, status: TaskStatus) -> int:
        """Đếm số công việc theo trạng thái"""
        session: Session = self.db_manager.get_session()
        try:
            count = session.query(func.count(TaskModel.id)).filter(
                TaskModel.status == status
            ).scalar()
            return count or 0
        finally:
            session.close()
    
    def get_task_statistics(self) -> dict:
        """Lấy thống kê công việc"""
        session: Session = self.db_manager.get_session()
        try:
            total_tasks = session.query(func.count(TaskModel.id)).scalar() or 0
            completed_tasks = session.query(func.count(TaskModel.id)).filter(
                TaskModel.status == TaskStatus.COMPLETED
            ).scalar() or 0
            in_progress_tasks = session.query(func.count(TaskModel.id)).filter(
                TaskModel.status == TaskStatus.IN_PROGRESS
            ).scalar() or 0
            not_started_tasks = session.query(func.count(TaskModel.id)).filter(
                TaskModel.status == TaskStatus.NOT_STARTED
            ).scalar() or 0
            overdue_tasks = session.query(func.count(TaskModel.id)).filter(
                and_(
                    TaskModel.due_date < datetime.now(),
                    TaskModel.status.notin_([TaskStatus.COMPLETED, TaskStatus.CANCELLED])
                )
            ).scalar() or 0
            
            return {
                'total': total_tasks,
                'not_started': not_started_tasks,
                'in_progress': in_progress_tasks,
                'completed': completed_tasks,
                'overdue': overdue_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
        finally:
            session.close()