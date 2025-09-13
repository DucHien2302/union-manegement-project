"""
Task Management Components
Specialized components for task management including task table,
filters, priority indicators, and task forms
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple, Optional, Dict, Any
from presentation.gui.theme import ModernTheme
from presentation.gui.base_components import BaseHeader, BaseTable, BaseFilter


class TaskTable:
    """Task table component with modern styling and priority indicators"""
    
    @staticmethod
    def create_task_table(parent) -> Tuple[ttk.Treeview, tk.Frame]:
        """
        Create modern task table with priority and status indicators
        
        Args:
            parent: Parent widget
            
        Returns:
            Tuple of (treeview, container_frame)
        """
        columns = ('ID', 'Tiêu đề', 'Ưu tiên', 'Trạng thái', 'Người thực hiện', 'Hạn hoàn thành', 'Tiến độ')
        column_widths = {
            'ID': 60, 'Tiêu đề': 250, 'Ưu tiên': 140, 'Trạng thái': 160, 
            'Người thực hiện': 150, 'Hạn hoàn thành': 130, 'Tiến độ': 90
        }
        
        tree, container = BaseTable.create_modern_table(parent, columns, column_widths)
        tree.configure(height=15)
        
        # Additional tags for task priorities and status
        tree.tag_configure('high_priority', background='#fef2f2', foreground='#dc2626')
        tree.tag_configure('medium_priority', background='#fffbeb', foreground='#d97706')
        tree.tag_configure('low_priority', background='#f0f9ff', foreground='#0369a1')
        tree.tag_configure('normal', background='#ffffff', foreground='#374151')
        tree.tag_configure('overdue', background='#fef2f2', foreground='#991b1b')
        tree.tag_configure('completed', background='#f0fdf4', foreground='#166534')
        tree.tag_configure('cancelled', background='#f9fafb', foreground='#6b7280')
        
        return tree, container


class TaskFilter:
    """Task filter component with priority and status filters"""
    
    @staticmethod
    def create_task_filter(parent, filter_callback: Callable = None) -> Dict[str, tk.StringVar]:
        """
        Create task filter section with priority and status filters
        
        Args:
            parent: Parent widget
            filter_callback: Filter callback function
            
        Returns:
            Dict of filter variables
        """
        filters = [
            ("Ưu tiên", ["Tất cả", "Thấp", "Trung bình", "Cao", "Khẩn cấp"], filter_callback),
            ("Trạng thái", ["Tất cả", "Chờ thực hiện", "Đang thực hiện", "Hoàn thành", "Tạm dừng"], filter_callback)
        ]
        
        return BaseFilter.create_filter_section(parent, filters)


class TaskTab:
    """Complete task management tab component"""
    
    @staticmethod
    def create_task_tab(parent, callbacks: Dict[str, Callable] = None) -> Tuple[tk.Frame, ttk.Treeview, Dict[str, tk.StringVar]]:
        """
        Create complete task management tab
        
        Args:
            parent: Parent widget (usually notebook)
            callbacks: Dict of callback functions for actions
            
        Returns:
            Tuple of (task_frame, task_tree, filter_vars)
        """
        task_frame = ttk.Frame(parent)
        
        # Default callbacks
        default_callbacks = {
            'add_task': lambda: None,
            'edit_task': lambda: None,
            'complete_task': lambda: None,
            'filter_tasks': lambda e=None: None
        }
        if callbacks:
            default_callbacks.update(callbacks)
        
        # Header with actions
        actions = [
            ("✏️ Cập nhật", default_callbacks['edit_task']),
            ("✅ Hoàn thành", default_callbacks['complete_task']),
            ("➕ Tạo công việc", default_callbacks['add_task'])
        ]
        BaseHeader.create_header(task_frame, "Quản lý Công việc", actions)
        
        # Content area
        content_frame = tk.Frame(task_frame, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter section
        filter_vars = TaskFilter.create_task_filter(
            content_frame, default_callbacks['filter_tasks'])
        
        # Table container
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=ModernTheme.PADDING_MEDIUM, 
                            pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Create task table
        task_tree, tree_container = TaskTable.create_task_table(table_container)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        return task_frame, task_tree, filter_vars


class TaskForm:
    """Task form component for add/edit operations"""
    
    @staticmethod
    def create_task_form_dialog(parent, title: str = "Thông tin công việc", 
                               task_data: Dict = None) -> Optional[Dict]:
        """
        Create task form dialog
        
        Args:
            parent: Parent widget
            title: Dialog title
            task_data: Existing task data for editing
            
        Returns:
            Dict with form data or None if cancelled
        """
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("600x650")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make it modal
        
        # Center the dialog
        dialog.transient(parent)
        dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        result = {}
        
        # Main container with scrollbar
        canvas = tk.Canvas(dialog, bg=ModernTheme.WHITE)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ModernTheme.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=ModernTheme.PADDING_LARGE)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        main_frame = tk.Frame(scrollable_frame, bg=ModernTheme.WHITE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                       pady=ModernTheme.PADDING_LARGE)
        
        fields = [
            ("Tiêu đề công việc:", "title", "entry"),
            ("Mô tả:", "description", "text"),
            ("Ưu tiên:", "priority", "combo"),
            ("Trạng thái:", "status", "combo"),
            ("Người thực hiện:", "assigned_to", "entry"),
            ("Hạn hoàn thành:", "due_date", "entry"),
            ("Tiến độ (%):", "progress_percentage", "entry"),
            ("Ghi chú:", "notes", "text")
        ]
        
        variables = {}
        
        for label_text, field_name, field_type in fields:
            # Field container
            field_frame = tk.Frame(main_frame, bg=ModernTheme.WHITE)
            field_frame.pack(fill=tk.X, pady=ModernTheme.PADDING_SMALL)
            
            # Label
            label = tk.Label(field_frame, text=label_text, 
                            font=ModernTheme.FONT_PRIMARY,
                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700,
                            anchor=tk.W)
            label.pack(fill=tk.X)
            
            # Input field
            if field_type == "combo":
                var = tk.StringVar()
                
                if field_name == "priority":
                    values = ["Thấp", "Trung bình", "Cao", "Khẩn cấp"]
                else:  # status
                    values = ["Chờ thực hiện", "Đang thực hiện", "Hoàn thành", "Tạm dừng"]
                
                combo = ttk.Combobox(field_frame, textvariable=var, values=values, 
                                   state="readonly", font=ModernTheme.FONT_PRIMARY)
                combo.pack(fill=tk.X, pady=(4, 0))
                
                if task_data and field_name in task_data:
                    combo.set(task_data[field_name])
                
                variables[field_name] = var
                
            elif field_type == "text":
                # Text area
                text_frame = tk.Frame(field_frame, bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                text_frame.pack(fill=tk.X, pady=(4, 0))
                
                text_widget = tk.Text(text_frame, height=4, 
                                    font=ModernTheme.FONT_PRIMARY,
                                    bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                    relief=tk.FLAT, bd=5, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                if task_data and field_name in task_data:
                    text_widget.insert(tk.END, str(task_data[field_name]))
                
                variables[field_name] = text_widget  # Store widget instead of StringVar
                
            else:  # entry
                var = tk.StringVar()
                entry = tk.Entry(field_frame, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=5)
                entry.pack(fill=tk.X, pady=(4, 0))
                
                if task_data and field_name in task_data:
                    entry.insert(0, str(task_data[field_name]))
                
                # Special handling for progress percentage
                if field_name == "progress_percentage":
                    # Add validation
                    def validate_percentage(value):
                        if value == "":
                            return True
                        try:
                            num = int(value)
                            return 0 <= num <= 100
                        except ValueError:
                            return False
                    
                    vcmd = (dialog.register(validate_percentage), '%P')
                    entry.config(validate='key', validatecommand=vcmd)
                
                variables[field_name] = var
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=ModernTheme.WHITE)
        button_frame.pack(fill=tk.X, pady=(ModernTheme.PADDING_LARGE, 0))
        
        # Buttons
        def on_save():
            # Collect form data
            for field_name, var in variables.items():
                if isinstance(var, tk.Text):
                    result[field_name] = var.get("1.0", tk.END).strip()
                else:
                    result[field_name] = var.get()
            dialog.destroy()
        
        def on_cancel():
            result.clear()
            dialog.destroy()
        
        cancel_btn = tk.Button(button_frame, text="Hủy", 
                              font=ModernTheme.FONT_PRIMARY,
                              bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                              border=0, cursor="hand2", padx=20, pady=8,
                              command=on_cancel)
        cancel_btn.pack(side=tk.RIGHT)
        
        save_btn = tk.Button(button_frame, text="Lưu", 
                            font=ModernTheme.FONT_PRIMARY,
                            bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                            border=0, cursor="hand2", padx=20, pady=8,
                            command=on_save)
        save_btn.pack(side=tk.RIGHT, padx=(0, ModernTheme.PADDING_SMALL))
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result if result else None


class TaskActions:
    """Task action handlers and utilities"""
    
    @staticmethod
    def populate_task_tree(tree: ttk.Treeview, tasks: List[Any]):
        """
        Populate task tree with data and apply styling based on priority and status
        
        Args:
            tree: Treeview widget
            tasks: List of task objects
        """
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Mapping for user-friendly display
        priority_display = {
            'low': '🟢 Thấp',
            'medium': '🟡 Trung bình',
            'high': '🟠 Cao',
            'urgent': '🔴 Khẩn cấp'
        }
        
        status_display = {
            'not_started': '⏸️ Chưa bắt đầu',
            'in_progress': '⚡ Đang thực hiện',
            'completed': '✅ Hoàn thành',
            'cancelled': '❌ Hủy bỏ',
            'on_hold': '⏸️ Tạm dừng'
        }
        
        # Add tasks with styling
        if not tasks:
            # Show empty state
            tree.insert('', 'end', values=('', '📝 Không có công việc nào', '', '', '', '', ''))
            return
            
        for task in tasks:
            # Format priority and status for better display
            priority_str = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
            status_str = task.status.value if hasattr(task.status, 'value') else str(task.status)
            
            # Convert to user-friendly display
            priority_display_str = priority_display.get(priority_str, priority_str)
            status_display_str = status_display.get(status_str, status_str)
            
            # Format date and progress
            due_date = task.due_date.strftime('%d/%m/%Y') if hasattr(task, 'due_date') and task.due_date else ''
            progress = f"{task.progress_percentage}%" if hasattr(task, 'progress_percentage') else "0%"
            
            item_id = tree.insert('', 'end', values=(
                task.id,
                task.title or "",
                priority_display_str,
                status_display_str,
                task.assigned_to or '',
                due_date,
                progress
            ))
            
            # Apply styling based on priority and status
            TaskActions._apply_task_styling(tree, item_id, task)
    
    @staticmethod
    def _apply_task_styling(tree: ttk.Treeview, item_id: str, task: Any):
        """Apply color coding based on task priority and status"""
        priority = task.priority.value if hasattr(task.priority, 'value') else task.priority
        status = task.status.value if hasattr(task.status, 'value') else task.status
        
        # Status-based styling (primary)
        if status in ["completed", "Hoàn thành"]:
            tree.item(item_id, tags=('completed',))
            return
        elif status in ["cancelled", "Hủy bỏ"]:
            tree.item(item_id, tags=('cancelled',))
            return
        
        # Check if overdue
        if hasattr(task, 'due_date') and task.due_date:
            from datetime import datetime
            if task.due_date < datetime.now() and status not in ["completed", "Hoàn thành"]:
                tree.item(item_id, tags=('overdue',))
                return
        
        # Priority-based styling (secondary)
        if priority in ["urgent", "Khẩn cấp", "🔴 Khẩn cấp"]:
            tree.item(item_id, tags=('high_priority',))
        elif priority in ["high", "Cao", "🟠 Cao"]:
            tree.item(item_id, tags=('medium_priority',))
        elif priority in ["medium", "Trung bình", "🟡 Trung bình"]:
            tree.item(item_id, tags=('low_priority',))
        else:  # low priority
            tree.item(item_id, tags=('normal',))
    
    @staticmethod
    def get_selected_task_id(tree: ttk.Treeview) -> Optional[int]:
        """
        Get selected task ID from tree
        
        Args:
            tree: Treeview widget
            
        Returns:
            Task ID or None if no selection
        """
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            return int(item['values'][0])  # ID is first column
        return None
    
    @staticmethod
    def filter_tasks(tree: ttk.Treeview, priority_filter: str, status_filter: str, all_tasks: List[Any]):
        """
        Filter tasks in tree based on priority and status
        
        Args:
            tree: Treeview widget
            priority_filter: Priority filter string
            status_filter: Status filter string
            all_tasks: Complete list of tasks
        """
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        
        # Filter tasks
        filtered_tasks = []
        for task in all_tasks:
            task_priority = task.priority.value if hasattr(task.priority, 'value') else task.priority
            task_status = task.status.value if hasattr(task.status, 'value') else task.status
            
            # Check priority filter
            priority_match = (priority_filter == "Tất cả" or task_priority == priority_filter)
            
            # Check status filter
            status_match = (status_filter == "Tất cả" or task_status == status_filter)
            
            if priority_match and status_match:
                filtered_tasks.append(task)
        
        # Populate with filtered results
        TaskActions.populate_task_tree(tree, filtered_tasks)
    
    @staticmethod
    def get_task_statistics(tasks: List[Any]) -> Dict[str, int]:
        """
        Calculate task statistics
        
        Args:
            tasks: List of task objects
            
        Returns:
            Dict with statistics
        """
        stats = {
            'total': len(tasks),
            'completed': 0,
            'in_progress': 0,
            'pending': 0,
            'overdue': 0,
            'high_priority': 0
        }
        
        from datetime import datetime
        now = datetime.now()
        
        for task in tasks:
            status = task.status.value if hasattr(task.status, 'value') else task.status
            priority = task.priority.value if hasattr(task.priority, 'value') else task.priority
            
            # Status counts
            if status == "Hoàn thành":
                stats['completed'] += 1
            elif status == "Đang thực hiện":
                stats['in_progress'] += 1
            elif status == "Chờ thực hiện":
                stats['pending'] += 1
            
            # Priority counts
            if priority in ["Cao", "Khẩn cấp"]:
                stats['high_priority'] += 1
            
            # Overdue check
            if (hasattr(task, 'due_date') and task.due_date and 
                task.due_date < now and status != "Hoàn thành"):
                stats['overdue'] += 1
        
        return stats