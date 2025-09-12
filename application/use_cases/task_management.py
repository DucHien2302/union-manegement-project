from typing import List, Optional
from datetime import datetime, timedelta
from domain.entities.task import Task, TaskPriority, TaskStatus
from domain.repositories.task_repository import ITaskRepository


class TaskManagementUseCase:
    """Use case cho quản lý công việc"""
    
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository
    
    def create_task(self, task_data: dict) -> Task:
        """Tạo công việc mới"""
        task = Task(
            title=task_data.get('title', ''),
            description=task_data.get('description', ''),
            priority=task_data.get('priority', TaskPriority.MEDIUM),
            status=TaskStatus.NOT_STARTED,
            assigned_to=task_data.get('assigned_to'),
            assigned_by=task_data.get('assigned_by'),
            start_date=task_data.get('start_date'),
            due_date=task_data.get('due_date'),
            estimated_hours=task_data.get('estimated_hours', 0.0),
            notes=task_data.get('notes', '')
        )
        
        return self.task_repository.create(task)
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Lấy công việc theo ID"""
        return self.task_repository.get_by_id(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Lấy tất cả công việc"""
        return self.task_repository.get_all()
    
    def get_tasks_by_assignee(self, assignee_id: int) -> List[Task]:
        """Lấy công việc được giao cho người dùng"""
        return self.task_repository.get_by_assignee(assignee_id)
    
    def get_tasks_by_assigner(self, assigner_id: int) -> List[Task]:
        """Lấy công việc do người dùng giao"""
        return self.task_repository.get_by_assigner(assigner_id)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Lấy công việc theo trạng thái"""
        return self.task_repository.get_by_status(status)
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Lấy công việc theo mức độ ưu tiên"""
        return self.task_repository.get_by_priority(priority)
    
    def get_overdue_tasks(self) -> List[Task]:
        """Lấy công việc quá hạn"""
        return self.task_repository.get_overdue_tasks()
    
    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Lấy công việc sắp hết hạn trong số ngày tới"""
        end_date = datetime.now() + timedelta(days=days)
        return self.task_repository.get_by_due_date_range(datetime.now(), end_date)
    
    def search_tasks_by_title(self, title: str) -> List[Task]:
        """Tìm kiếm công việc theo tiêu đề"""
        return self.task_repository.search_by_title(title)
    
    def update_task(self, task_id: int, update_data: dict) -> Task:
        """Cập nhật công việc"""
        existing_task = self.task_repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        # Cập nhật các thuộc tính
        for key, value in update_data.items():
            if hasattr(existing_task, key) and key not in ['id', 'created_at']:
                setattr(existing_task, key, value)
        
        existing_task.updated_at = datetime.now()
        return self.task_repository.update(existing_task)
    
    def start_task(self, task_id: int) -> Task:
        """Bắt đầu công việc"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        if task.status != TaskStatus.NOT_STARTED:
            raise ValueError("Chỉ có thể bắt đầu công việc ở trạng thái chưa bắt đầu")
        
        task.start_task()
        return self.task_repository.update(task)
    
    def complete_task(self, task_id: int, actual_hours: Optional[float] = None) -> Task:
        """Hoàn thành công việc"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        if task.status == TaskStatus.COMPLETED:
            raise ValueError("Công việc đã được hoàn thành")
        
        if task.status == TaskStatus.CANCELLED:
            raise ValueError("Không thể hoàn thành công việc đã bị hủy")
        
        task.complete_task(actual_hours)
        return self.task_repository.update(task)
    
    def cancel_task(self, task_id: int, reason: str = "") -> Task:
        """Hủy bỏ công việc"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        if task.status == TaskStatus.COMPLETED:
            raise ValueError("Không thể hủy công việc đã hoàn thành")
        
        if task.status == TaskStatus.CANCELLED:
            raise ValueError("Công việc đã bị hủy")
        
        task.cancel_task(reason)
        return self.task_repository.update(task)
    
    def update_task_progress(self, task_id: int, percentage: int) -> Task:
        """Cập nhật tiến độ công việc"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        if task.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            raise ValueError("Không thể cập nhật tiến độ công việc đã hoàn thành hoặc bị hủy")
        
        if not (0 <= percentage <= 100):
            raise ValueError("Tiến độ phải trong khoảng 0-100%")
        
        task.update_progress(percentage)
        return self.task_repository.update(task)
    
    def assign_task(self, task_id: int, assignee_id: int, assigner_id: int) -> Task:
        """Giao việc cho người khác"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        if task.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            raise ValueError("Không thể giao công việc đã hoàn thành hoặc bị hủy")
        
        task.assigned_to = assignee_id
        task.assigned_by = assigner_id
        task.updated_at = datetime.now()
        
        return self.task_repository.update(task)
    
    def delete_task(self, task_id: int) -> bool:
        """Xóa công việc"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Không tìm thấy công việc với ID {task_id}")
        
        return self.task_repository.delete(task_id)
    
    def get_task_statistics(self) -> dict:
        """Lấy thống kê công việc"""
        return self.task_repository.get_task_statistics()
    
    def get_my_tasks(self, user_id: int) -> dict:
        """Lấy tổng quan công việc của người dùng"""
        assigned_tasks = self.get_tasks_by_assignee(user_id)
        created_tasks = self.get_tasks_by_assigner(user_id)
        
        my_overdue = [task for task in assigned_tasks if task.is_overdue()]
        my_upcoming = [task for task in assigned_tasks 
                      if task.due_date and task.get_days_remaining() is not None 
                      and 0 <= task.get_days_remaining() <= 7]
        my_in_progress = [task for task in assigned_tasks 
                         if task.status == TaskStatus.IN_PROGRESS]
        
        return {
            'assigned_to_me': len(assigned_tasks),
            'created_by_me': len(created_tasks),
            'overdue': len(my_overdue),
            'upcoming': len(my_upcoming),
            'in_progress': len(my_in_progress),
            'overdue_tasks': my_overdue,
            'upcoming_tasks': my_upcoming,
            'in_progress_tasks': my_in_progress
        }