"""
Task Controller
Handles task-related UI logic and data transformation
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from tkinter import messagebox

from domain.entities.task import Task, TaskPriority, TaskStatus
from application.use_cases.task_management import TaskManagementUseCase
from presentation.controllers.base_controller import BaseController


class TaskController(BaseController):
    """Controller for task management operations"""
    
    def __init__(self, task_use_case: TaskManagementUseCase):
        super().__init__()
        self.task_use_case = task_use_case
    
    def get_all_tasks(self) -> List[Task]:
        """Lấy tất cả tasks"""
        try:
            tasks = self.task_use_case.get_all_tasks()
            self.logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
        except Exception as e:
            self.logger.error(f"Error getting all tasks: {e}")
            return []
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Lấy task theo ID"""
        try:
            task = self.task_use_case.get_task_by_id(task_id)
            self.logger.info(f"Retrieved task: {task_id}")
            return task
        except Exception as e:
            self.logger.error(f"Error getting task {task_id}: {e}")
            return None
    
    def create_task(self, task_data: Dict[str, Any]) -> bool:
        """Tạo task mới"""
        try:
            # Process and validate data
            processed_data = self._process_task_data(task_data)
            
            # Save through use case (pass dict, not Task object)
            created_task = self.task_use_case.create_task(processed_data)
            
            if created_task:
                self.logger.info(f"Created task: {created_task.id}")
                messagebox.showinfo("Thành công", "Tạo công việc thành công!")
                return True
            else:
                messagebox.showerror("Lỗi", "Không thể tạo công việc!")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating task: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi tạo công việc: {e}")
            return False
    
    def update_task(self, task_id: int, task_data: Dict[str, Any]) -> bool:
        """Cập nhật task"""
        try:
            # Get existing task
            existing_task = self.task_use_case.get_task_by_id(task_id)
            if not existing_task:
                messagebox.showerror("Lỗi", "Không tìm thấy công việc!")
                return False
            
            # Process and validate data
            processed_data = self._process_task_data(task_data)
            
            # Save through use case with processed data
            success = self.task_use_case.update_task(task_id, processed_data)
            
            if success:
                self.logger.info(f"Updated task: {task_id}")
                messagebox.showinfo("Thành công", "Cập nhật công việc thành công!")
                return True
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật công việc!")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating task {task_id}: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật công việc: {e}")
            return False
    
    def complete_task(self, task_id: int) -> bool:
        """Hoàn thành task"""
        try:
            # Get existing task
            existing_task = self.task_use_case.get_task_by_id(task_id)
            if not existing_task:
                messagebox.showerror("Lỗi", "Không tìm thấy công việc!")
                return False
            
            # Prepare update data
            update_data = {
                'status': TaskStatus.COMPLETED,
                'progress_percentage': 100,
                'completed_at': datetime.now()
            }
            
            # Save through use case
            success = self.task_use_case.update_task(task_id, update_data)
            
            if success:
                self.logger.info(f"Completed task: {task_id}")
                messagebox.showinfo("Thành công", "Đánh dấu hoàn thành công việc!")
                return True
            else:
                messagebox.showerror("Lỗi", "Không thể hoàn thành công việc!")
                return False
                
        except Exception as e:
            self.logger.error(f"Error completing task {task_id}: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi hoàn thành công việc: {e}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Xóa task"""
        try:
            success = self.task_use_case.delete_task(task_id)
            
            if success:
                self.logger.info(f"Deleted task: {task_id}")
                messagebox.showinfo("Thành công", "Xóa công việc thành công!")
                return True
            else:
                messagebox.showerror("Lỗi", "Không thể xóa công việc!")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting task {task_id}: {e}")
            messagebox.showerror("Lỗi", f"Lỗi khi xóa công việc: {e}")
            return False
    
    def format_task_data_for_display(self, task: Task) -> Dict[str, str]:
        """Chuyển đổi dữ liệu task để hiển thị trong form"""
        # Mapping cho hiển thị
        priority_display_mapping = {
            TaskPriority.LOW: "Thấp",
            TaskPriority.MEDIUM: "Trung bình", 
            TaskPriority.HIGH: "Cao",
            TaskPriority.URGENT: "Khẩn cấp"
        }
        
        status_display_mapping = {
            TaskStatus.NOT_STARTED: "Chờ thực hiện",
            TaskStatus.IN_PROGRESS: "Đang thực hiện",
            TaskStatus.COMPLETED: "Hoàn thành",
            TaskStatus.ON_HOLD: "Tạm dừng",
            TaskStatus.CANCELLED: "Hủy bỏ",
            TaskStatus.OVERDUE: "Quá hạn"
        }
        
        return {
            'title': task.title or '',
            'description': task.description or '',
            'priority': priority_display_mapping.get(task.priority, "Trung bình"),
            'status': status_display_mapping.get(task.status, "Chờ thực hiện"),
            'assigned_to': str(task.assigned_to) if task.assigned_to else '',
            'due_date': task.due_date.strftime('%d/%m/%Y') if task.due_date else '',
            'progress_percentage': str(task.progress_percentage or 0),
            'notes': task.notes or ''
        }
    
    def _process_task_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Xử lý và validate dữ liệu task từ form"""
        processed_data = {}
        
        # Title (required)
        processed_data['title'] = data.get('title', '').strip()
        if not processed_data['title']:
            raise ValueError("Tiêu đề công việc không được để trống")
        
        # Description
        processed_data['description'] = data.get('description', '').strip()
        
        # Priority (required)
        priority_str = data.get('priority', '').strip()
        priority_mapping = {
            'Thấp': TaskPriority.LOW,
            'Trung bình': TaskPriority.MEDIUM,
            'Cao': TaskPriority.HIGH,
            'Khẩn cấp': TaskPriority.URGENT
        }
        processed_data['priority'] = priority_mapping.get(priority_str, TaskPriority.MEDIUM)
        
        # Status (required)
        status_str = data.get('status', '').strip()
        status_mapping = {
            'Chờ thực hiện': TaskStatus.NOT_STARTED,
            'Đang thực hiện': TaskStatus.IN_PROGRESS,
            'Hoàn thành': TaskStatus.COMPLETED,
            'Tạm dừng': TaskStatus.ON_HOLD,
            'Hủy bỏ': TaskStatus.CANCELLED,
            'Quá hạn': TaskStatus.OVERDUE
        }
        processed_data['status'] = status_mapping.get(status_str, TaskStatus.NOT_STARTED)
        
        # Assigned to  
        assigned_to_str = data.get('assigned_to', '').strip()
        if assigned_to_str:
            # For now, use a default member ID (1) or lookup by name later
            # TODO: Implement proper member lookup by name
            processed_data['assigned_to'] = 1  # Default member ID for testing
        else:
            processed_data['assigned_to'] = None
        
        # Due date
        due_date_str = data.get('due_date', '').strip()
        if due_date_str:
            try:
                # Try parsing DD/MM/YYYY format
                processed_data['due_date'] = datetime.strptime(due_date_str, '%d/%m/%Y')
            except ValueError:
                try:
                    # Try parsing YYYY-MM-DD format
                    processed_data['due_date'] = datetime.strptime(due_date_str, '%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Định dạng ngày không hợp lệ: {due_date_str}. Sử dụng DD/MM/YYYY")
        else:
            processed_data['due_date'] = None
        
        # Progress percentage
        progress_str = data.get('progress_percentage', '').strip()
        if progress_str:
            try:
                progress = int(progress_str)
                if not (0 <= progress <= 100):
                    raise ValueError("Tiến độ phải từ 0 đến 100%")
                processed_data['progress_percentage'] = progress
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError("Tiến độ phải là số nguyên")
                raise e
        else:
            processed_data['progress_percentage'] = 0
        
        # Notes
        processed_data['notes'] = data.get('notes', '').strip()
        
        return processed_data