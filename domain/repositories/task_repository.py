from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.task import Task, TaskPriority, TaskStatus


class ITaskRepository(ABC):
    """Interface cho Task Repository"""
    
    @abstractmethod
    def create(self, task: Task) -> Task:
        """Tạo công việc mới"""
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Lấy công việc theo ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        """Lấy tất cả công việc"""
        pass
    
    @abstractmethod
    def get_by_assignee(self, assignee_id: int) -> List[Task]:
        """Lấy công việc theo người được giao"""
        pass
    
    @abstractmethod
    def get_by_assigner(self, assigner_id: int) -> List[Task]:
        """Lấy công việc theo người giao việc"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: TaskStatus) -> List[Task]:
        """Lấy công việc theo trạng thái"""
        pass
    
    @abstractmethod
    def get_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Lấy công việc theo mức độ ưu tiên"""
        pass
    
    @abstractmethod
    def get_by_due_date_range(self, start_date: datetime, end_date: datetime) -> List[Task]:
        """Lấy công việc trong khoảng hạn hoàn thành"""
        pass
    
    @abstractmethod
    def get_overdue_tasks(self) -> List[Task]:
        """Lấy công việc quá hạn"""
        pass
    
    @abstractmethod
    def search_by_title(self, title: str) -> List[Task]:
        """Tìm kiếm công việc theo tiêu đề"""
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        """Cập nhật công việc"""
        pass
    
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Xóa công việc"""
        pass
    
    @abstractmethod
    def count_by_status(self, status: TaskStatus) -> int:
        """Đếm số công việc theo trạng thái"""
        pass
    
    @abstractmethod
    def get_task_statistics(self) -> dict:
        """Lấy thống kê công việc"""
        pass