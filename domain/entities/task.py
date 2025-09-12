from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskPriority(Enum):
    """Mức độ ưu tiên công việc"""
    LOW = "low"  # Thấp
    MEDIUM = "medium"  # Trung bình
    HIGH = "high"  # Cao
    URGENT = "urgent"  # Khẩn cấp


class TaskStatus(Enum):
    """Trạng thái công việc"""
    NOT_STARTED = "not_started"  # Chưa bắt đầu
    IN_PROGRESS = "in_progress"  # Đang thực hiện
    COMPLETED = "completed"  # Hoàn thành
    CANCELLED = "cancelled"  # Hủy bỏ
    OVERDUE = "overdue"  # Quá hạn


@dataclass
class Task:
    """Entity cho Công việc"""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.NOT_STARTED
    assigned_to: Optional[int] = None  # ID của người được giao
    assigned_by: Optional[int] = None  # ID của người giao việc
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    progress_percentage: int = 0  # Phần trăm hoàn thành (0-100)
    notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def start_task(self):
        """Bắt đầu công việc"""
        if self.status == TaskStatus.NOT_STARTED:
            self.status = TaskStatus.IN_PROGRESS
            if self.start_date is None:
                self.start_date = datetime.now()
            self.updated_at = datetime.now()

    def complete_task(self, actual_hours: Optional[float] = None):
        """Hoàn thành công việc"""
        self.status = TaskStatus.COMPLETED
        self.completed_date = datetime.now()
        self.progress_percentage = 100
        if actual_hours is not None:
            self.actual_hours = actual_hours
        self.updated_at = datetime.now()

    def cancel_task(self, reason: str = ""):
        """Hủy bỏ công việc"""
        self.status = TaskStatus.CANCELLED
        if reason:
            self.notes += f"\nLý do hủy: {reason}"
        self.updated_at = datetime.now()

    def update_progress(self, percentage: int):
        """Cập nhật tiến độ công việc"""
        if 0 <= percentage <= 100:
            self.progress_percentage = percentage
            if percentage == 100 and self.status != TaskStatus.COMPLETED:
                self.complete_task()
            elif percentage > 0 and self.status == TaskStatus.NOT_STARTED:
                self.start_task()
            self.updated_at = datetime.now()

    def is_overdue(self) -> bool:
        """Kiểm tra công việc có quá hạn không"""
        if self.due_date is None or self.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return False
        return datetime.now() > self.due_date

    def get_days_remaining(self) -> Optional[int]:
        """Lấy số ngày còn lại"""
        if self.due_date is None:
            return None
        delta = self.due_date - datetime.now()
        return delta.days