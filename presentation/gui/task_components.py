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
            'delete_task': lambda: None,
            'filter_tasks': lambda e=None: None
        }
        if callbacks:
            default_callbacks.update(callbacks)
        
        # Header with actions
        actions = [
            ("✏️ Cập nhật", default_callbacks['edit_task']),
            ("✅ Hoàn thành", default_callbacks['complete_task']),
            ("🗑️ Xóa", default_callbacks.get('delete_task', lambda: None)),
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
        dialog.geometry("650x700")
        dialog.resizable(True, True)
        dialog.grab_set()  # Make it modal
        
        # Center the dialog
        dialog.transient(parent)
        dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        result = {}
        is_saved = False  # Flag để theo dõi việc save
        
        # Handle dialog close
        def on_dialog_close():
            nonlocal is_saved
            is_saved = False
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        
        # Create main layout với button frame cố định ở bottom
        main_frame = tk.Frame(dialog, bg=ModernTheme.WHITE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, pady=ModernTheme.PADDING_LARGE)
        
        # Content frame với scrollbar (sẽ chiếm phần còn lại)
        content_frame = tk.Frame(main_frame, bg=ModernTheme.WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas và scrollbar cho nội dung form
        canvas = tk.Canvas(content_frame, bg=ModernTheme.WHITE)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ModernTheme.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields container
        form_container = tk.Frame(scrollable_frame, bg=ModernTheme.WHITE)
        form_container.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_MEDIUM, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        fields = [
            ("Tiêu đề công việc:", "title", "entry"),
            ("Mô tả:", "description", "text"),
            ("Ưu tiên:", "priority", "combo"),
            ("Trạng thái:", "status", "combo"),
            ("Người thực hiện:", "assigned_to", "entry"),
            ("Hạn hoàn thành:", "due_date", "date"),
            ("Tiến độ (%):", "progress_percentage", "number"),
            ("Ghi chú:", "notes", "text")
        ]
        
        variables = {}
        
        # Debug: In dữ liệu nhận được
        if task_data:
            print(f"🔍 Debug - Task data received: {task_data}")
        
        for label_text, field_name, field_type in fields:
            # Field container
            field_frame = tk.Frame(form_container, bg=ModernTheme.WHITE)
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
                
                # Set initial value if task_data exists
                if task_data and field_name in task_data:
                    initial_value = task_data[field_name]
                    print(f"🔍 Debug - Setting {field_name} to: {initial_value}")
                    if initial_value in values:
                        combo.set(initial_value)
                        var.set(initial_value)
                    else:
                        print(f"⚠️ Warning - Value '{initial_value}' not found in {values}")
                        # Try to find partial match
                        for value in values:
                            if initial_value.lower() in value.lower() or value.lower() in initial_value.lower():
                                combo.set(value)
                                var.set(value)
                                print(f"✅ Found partial match: {value}")
                                break
                
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
                
            elif field_type == "date":
                # Date picker field
                var = tk.StringVar()
                date_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                date_frame.pack(fill=tk.X, pady=(4, 0))
                
                # Date entry
                entry = tk.Entry(date_frame, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=5, width=15)
                entry.pack(side=tk.LEFT)
                
                # Date picker button  
                def create_date_picker_command(date_var):
                    def open_date_picker():
                        try:
                            from tkinter import simpledialog
                            import datetime
                            
                            # Simple date input dialog
                            date_str = simpledialog.askstring("Chọn ngày", 
                                                             "Nhập ngày (DD/MM/YYYY):",
                                                             initialvalue=date_var.get())
                            if date_str:
                                # Validate date format
                                try:
                                    datetime.datetime.strptime(date_str, '%d/%m/%Y')
                                    date_var.set(date_str)
                                except ValueError:
                                    from tkinter import messagebox
                                    messagebox.showerror("Lỗi", "Định dạng ngày không đúng. Sử dụng DD/MM/YYYY")
                        except Exception as e:
                            print(f"Date picker error: {e}")
                    return open_date_picker
                
                date_btn = tk.Button(date_frame, text="📅", 
                                   font=ModernTheme.FONT_PRIMARY,
                                   bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                                   border=0, cursor="hand2", padx=8, pady=4,
                                   command=create_date_picker_command(var))
                date_btn.pack(side=tk.LEFT, padx=(5, 0))
                
                # Help text
                help_label = tk.Label(date_frame, text="(DD/MM/YYYY)", 
                                    font=('Segoe UI', 8), 
                                    bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                help_label.pack(side=tk.LEFT, padx=(5, 0))
                
                if task_data and field_name in task_data:
                    entry.insert(0, str(task_data[field_name]))
                
                variables[field_name] = var
                
            elif field_type == "number":
                # Number input with validation
                var = tk.StringVar()
                number_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                number_frame.pack(fill=tk.X, pady=(4, 0))
                
                # Number validation
                def validate_number(value):
                    if value == "":
                        return True
                    try:
                        num = int(value)
                        if field_name == "progress_percentage":
                            return 0 <= num <= 100
                        return num >= 0
                    except ValueError:
                        return False
                
                vcmd = (dialog.register(validate_number), '%P')
                
                entry = tk.Entry(number_frame, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=5, width=10,
                               validate='key', validatecommand=vcmd)
                entry.pack(side=tk.LEFT)
                
                # Min/Max labels
                if field_name == "progress_percentage":
                    range_label = tk.Label(number_frame, text="(0-100)", 
                                         font=('Segoe UI', 8), 
                                         bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                    range_label.pack(side=tk.LEFT, padx=(5, 0))
                
                if task_data and field_name in task_data:
                    entry.insert(0, str(task_data[field_name]))
                
                variables[field_name] = var
                
            else:  # entry
                var = tk.StringVar()
                entry = tk.Entry(field_frame, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=5)
                entry.pack(fill=tk.X, pady=(4, 0))
                
                if task_data and field_name in task_data:
                    entry.insert(0, str(task_data[field_name]))
                
                variables[field_name] = var
        
        # Separator line
        separator = tk.Frame(main_frame, height=2, bg=ModernTheme.GRAY_200)
        separator.pack(fill=tk.X, pady=(ModernTheme.PADDING_MEDIUM, 0))
        
        # Fixed button frame at bottom - pack sau khi content đã được pack
        button_frame = tk.Frame(main_frame, bg=ModernTheme.WHITE, height=70)
        button_frame.pack(fill=tk.X, pady=(ModernTheme.PADDING_MEDIUM, 0))
        button_frame.pack_propagate(False)  # Maintain fixed height
        
        # Buttons functions
        def validate_form():
            """Validate form data before saving"""
            errors = []
            
            # Check required fields
            if not variables['title'].get().strip():
                errors.append("Tiêu đề công việc không được để trống")
            if not variables['priority'].get():
                errors.append("Vui lòng chọn mức độ ưu tiên")
            if not variables['status'].get():
                errors.append("Vui lòng chọn trạng thái")
            
            # Validate progress percentage
            try:
                progress = variables['progress_percentage'].get().strip()
                if progress:
                    progress_num = int(progress)
                    if not (0 <= progress_num <= 100):
                        errors.append("Tiến độ phải từ 0 đến 100%")
            except ValueError:
                errors.append("Tiến độ phải là số nguyên")
            
            return errors
        
        def on_save():
            nonlocal is_saved
            
            # Validate form
            errors = validate_form()
            if errors:
                from tkinter import messagebox
                messagebox.showerror("Lỗi", "\n".join(errors))
                return
            
            # Collect form data
            for field_name, var in variables.items():
                if isinstance(var, tk.Text):
                    result[field_name] = var.get("1.0", tk.END).strip()
                else:
                    result[field_name] = var.get()
            is_saved = True
            dialog.destroy()
        
        def on_cancel():
            nonlocal is_saved
            result.clear()
            is_saved = False
            dialog.destroy()
        
        # Create buttons with better styling and spacing
        button_container = tk.Frame(button_frame, bg=ModernTheme.WHITE)
        button_container.pack(expand=True, fill=tk.BOTH)
        
        cancel_btn = tk.Button(button_container, text="Hủy", 
                              font=ModernTheme.FONT_PRIMARY,
                              bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                              border=0, cursor="hand2", padx=30, pady=10,
                              command=on_cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(ModernTheme.PADDING_SMALL, ModernTheme.PADDING_MEDIUM), 
                       pady=ModernTheme.PADDING_SMALL)
        
        save_btn = tk.Button(button_container, text="Lưu", 
                            font=ModernTheme.FONT_PRIMARY,
                            bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                            border=0, cursor="hand2", padx=30, pady=10,
                            command=on_save)
        save_btn.pack(side=tk.RIGHT, padx=(0, ModernTheme.PADDING_SMALL), 
                     pady=ModernTheme.PADDING_SMALL)
        
        # Keyboard shortcuts
        dialog.bind('<Control-s>', lambda e: on_save())  # Ctrl+S to save
        dialog.bind('<Escape>', lambda e: on_cancel())   # Esc to cancel
        dialog.bind('<Return>', lambda e: on_save())     # Enter to save (when not in text widget)
        
        # Focus on first field
        if variables and 'title' in variables:
            dialog.after(100, lambda: dialog.focus_set())
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result if is_saved else None


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
    def filter_tasks(tree: ttk.Treeview, filter_type: str, filter_value: str, all_tasks: List[Any]):
        """
        Filter tasks in tree based on priority or status
        
        Args:
            tree: Treeview widget
            filter_type: Type of filter ('priority' or 'status')
            filter_value: Filter value string
            all_tasks: Complete list of tasks
        """
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        
        # If showing all, populate with all tasks
        if filter_value == "Tất cả":
            TaskActions.populate_task_tree(tree, all_tasks)
            return
        
        # Filter mapping
        if filter_type == "priority":
            filter_mapping = {
                'Thấp': 'low',
                'Trung bình': 'medium',
                'Cao': 'high',
                'Khẩn cấp': 'urgent'
            }
        else:  # status
            filter_mapping = {
                'Chờ thực hiện': 'not_started',
                'Đang thực hiện': 'in_progress',
                'Hoàn thành': 'completed',
                'Tạm dừng': 'on_hold'
            }
        
        # Get database value
        db_value = filter_mapping.get(filter_value, filter_value.lower())
        
        # Filter tasks
        filtered_tasks = []
        for task in all_tasks:
            if filter_type == "priority":
                task_value = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
            else:  # status
                task_value = task.status.value if hasattr(task.status, 'value') else str(task.status)
            
            # Compare with database value or display value
            if task_value == db_value or task_value == filter_value:
                filtered_tasks.append(task)
        
        # Populate with filtered results
        TaskActions.populate_task_tree(tree, filtered_tasks)
    
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