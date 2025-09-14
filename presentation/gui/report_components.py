"""
Report Management Components
Specialized components for report management including report table,
filters, and report forms
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple, Optional, Dict, Any
from presentation.gui.theme import ModernTheme
from presentation.gui.base_components import BaseHeader, BaseTable, BaseFilter


class ReportTable:
    """Report table component with modern styling"""
    
    @staticmethod
    def create_report_table(parent) -> Tuple[ttk.Treeview, tk.Frame]:
        """
        Create modern report table
        
        Args:
            parent: Parent widget
            
        Returns:
            Tuple of (treeview, container_frame)
        """
        columns = ('ID', 'Tiêu đề', 'Loại', 'Kỳ', 'Trạng thái', 'Ngày tạo')
        column_widths = {
            'ID': 60, 'Tiêu đề': 300, 'Loại': 140, 'Kỳ': 120, 
            'Trạng thái': 150, 'Ngày tạo': 120
        }
        
        tree, container = BaseTable.create_modern_table(parent, columns, column_widths)
        tree.configure(height=15)
        
        return tree, container


class ReportFilter:
    """Report filter component"""
    
    @staticmethod
    def create_report_filter(parent, filter_callback: Callable = None) -> Dict[str, tk.StringVar]:
        """
        Create report filter section
        
        Args:
            parent: Parent widget
            filter_callback: Filter callback function
            
        Returns:
            Dict of filter variables
        """
        filters = [
            ("Trạng thái", ["Tất cả", "Nháp", "Đã nộp", "Đã duyệt", "Từ chối"], filter_callback)
        ]
        
        return BaseFilter.create_filter_section(parent, filters)


class ReportTab:
    """Complete report management tab component"""
    
    @staticmethod
    def create_report_tab(parent, callbacks: Dict[str, Callable] = None) -> Tuple[tk.Frame, ttk.Treeview, Dict[str, tk.StringVar]]:
        """
        Create complete report management tab
        
        Args:
            parent: Parent widget (usually notebook)
            callbacks: Dict of callback functions for actions
            
        Returns:
            Tuple of (report_frame, report_tree, filter_vars)
        """
        report_frame = ttk.Frame(parent)
        
        # Default callbacks
        default_callbacks = {
            'add_report': lambda: None,
            'edit_report': lambda: None,
            'approve_report': lambda: None,
            'filter_reports': lambda e=None: None
        }
        if callbacks:
            default_callbacks.update(callbacks)
        
        # Header with actions
        actions = [
            ("👁️ Xem/Sửa", default_callbacks['edit_report']),
            ("✅ Duyệt", default_callbacks['approve_report']),
            ("📝 Tạo báo cáo", default_callbacks['add_report'])
        ]
        BaseHeader.create_header(report_frame, "Quản lý Báo cáo", actions)
        
        # Content area
        content_frame = tk.Frame(report_frame, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter section
        filter_vars = ReportFilter.create_report_filter(
            content_frame, default_callbacks['filter_reports'])
        
        # Table container
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=ModernTheme.PADDING_MEDIUM, 
                            pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Create report table
        report_tree, tree_container = ReportTable.create_report_table(table_container)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        return report_frame, report_tree, filter_vars


class ReportForm:
    """Report form component for add/edit operations"""
    
    @staticmethod
    def create_report_form_dialog(parent, title: str = "Thông tin báo cáo", 
                                 report_data: Dict = None) -> Optional[Dict]:
        """
        Create report form dialog
        
        Args:
            parent: Parent widget
            title: Dialog title
            report_data: Existing report data for editing
            
        Returns:
            Dict with form data or None if cancelled
        """
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("650x750")
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
            ("Tiêu đề báo cáo:", "title", "entry"),
            ("Loại báo cáo:", "report_type", "combo"),
            ("Kỳ báo cáo:", "period", "entry"),
            ("Trạng thái:", "status", "combo"),
            ("Nội dung báo cáo:", "content", "text")
        ]
        
        variables = {}
        
        # Debug: In dữ liệu nhận được
        if report_data:
            print(f"🔍 Debug - Report data received: {report_data}")
        
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
                
                if field_name == "report_type":
                    values = ["Báo cáo tháng", "Báo cáo quý", "Báo cáo năm", "Báo cáo đặc biệt"]
                else:  # status
                    values = ["Nháp", "Đã nộp", "Đã duyệt", "Từ chối"]
                
                combo = ttk.Combobox(field_frame, textvariable=var, values=values, 
                                   state="readonly", font=ModernTheme.FONT_PRIMARY)
                combo.pack(fill=tk.X, pady=(4, 0))
                
                # Set initial value if report_data exists
                if report_data and field_name in report_data:
                    initial_value = report_data[field_name]
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
                
                text_widget = tk.Text(text_frame, height=6, 
                                    font=ModernTheme.FONT_PRIMARY,
                                    bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                    relief=tk.FLAT, bd=5, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                if report_data and field_name in report_data:
                    text_widget.insert(tk.END, str(report_data[field_name]))
                
                variables[field_name] = text_widget  # Store widget instead of StringVar
                
            else:  # entry
                var = tk.StringVar()
                entry = tk.Entry(field_frame, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=5)
                entry.pack(fill=tk.X, pady=(4, 0))
                
                if report_data and field_name in report_data:
                    entry.insert(0, str(report_data[field_name]))
                
                variables[field_name] = var
        
        # Separator line
        separator = tk.Frame(main_frame, height=2, bg=ModernTheme.GRAY_200)
        separator.pack(fill=tk.X, pady=(ModernTheme.PADDING_MEDIUM, 0))
        
        # Fixed button frame at bottom - pack sau khi content đã được pack
        button_frame = tk.Frame(main_frame, bg=ModernTheme.WHITE, height=70)
        button_frame.pack(fill=tk.X, pady=(ModernTheme.PADDING_MEDIUM, 0))
        button_frame.pack_propagate(False)  # Maintain fixed height
        
        # Buttons định nghĩa functions
        def validate_form():
            """Validate form data before saving"""
            errors = []
            
            # Check required fields
            if not variables['title'].get().strip():
                errors.append("Tiêu đề báo cáo không được để trống")
            if not variables['report_type'].get():
                errors.append("Vui lòng chọn loại báo cáo")
            if not variables['period'].get().strip():
                errors.append("Kỳ báo cáo không được để trống")
            if not variables['status'].get():
                errors.append("Vui lòng chọn trạng thái")
            
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


class ReportActions:
    """Report action handlers and utilities"""
    
    @staticmethod
    def populate_report_tree(tree: ttk.Treeview, reports: List[Any]):
        """
        Populate report tree with data
        
        Args:
            tree: Treeview widget
            reports: List of report objects
        """
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Mapping for user-friendly display
        report_type_display = {
            'weekly': '📊 Tuần',
            'monthly': '📅 Tháng',
            'quarterly': '📈 Quý',
            'annual': '📋 Năm',
            'special': '⭐ Đặc biệt'
        }
        
        status_display = {
            'draft': '📝 Nháp',
            'submitted': '📤 Đã nộp',
            'approved': '✅ Đã duyệt',
            'rejected': '❌ Từ chối',
            'in_review': '👀 Đang xem xét'
        }
        
        # Add reports
        if not reports:
            # Show empty state
            tree.insert('', 'end', values=('', '📭 Không có báo cáo nào', '', '', '', ''))
            return
            
        for report in reports:
            # Format report type and status for better display
            report_type_str = report.report_type.value if hasattr(report.report_type, 'value') else str(report.report_type)
            status_str = report.status.value if hasattr(report.status, 'value') else str(report.status)
            
            # Convert to user-friendly display
            report_type_display_str = report_type_display.get(report_type_str, report_type_str)
            status_display_str = status_display.get(status_str, status_str)
            
            # Format date
            created_date = report.created_at.strftime('%d/%m/%Y') if hasattr(report, 'created_at') and report.created_at else ''
            
            tree.insert('', 'end', values=(
                report.id,
                report.title or "",
                report_type_display_str,
                report.period or "",
                status_display_str,
                created_date
            ))
    
    @staticmethod
    def get_selected_report_id(tree: ttk.Treeview) -> Optional[int]:
        """
        Get selected report ID from tree
        
        Args:
            tree: Treeview widget
            
        Returns:
            Report ID or None if no selection
        """
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            return int(item['values'][0])  # ID is first column
        return None
    
    @staticmethod
    def filter_reports(tree: ttk.Treeview, status_filter: str, all_reports: List[Any]):
        """
        Filter reports in tree based on status
        
        Args:
            tree: Treeview widget
            status_filter: Status filter string
            all_reports: Complete list of reports
        """
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        
        # If showing all, populate with all reports
        if status_filter == "Tất cả":
            ReportActions.populate_report_tree(tree, all_reports)
            return
        
        # Status mapping từ display name sang database value
        status_mapping = {
            'Nháp': 'draft',
            'Đã nộp': 'submitted',
            'Đã duyệt': 'approved', 
            'Từ chối': 'rejected',
            'Đang xem xét': 'in_review'
        }
        
        # Get database status value
        db_status = status_mapping.get(status_filter, status_filter.lower())
        
        # Filter reports by status
        filtered_reports = []
        for report in all_reports:
            # Get report status value
            report_status = report.status.value if hasattr(report.status, 'value') else str(report.status)
            
            # Compare with database status or display status
            if report_status == db_status or report_status == status_filter:
                filtered_reports.append(report)
        
        # Populate with filtered results
        ReportActions.populate_report_tree(tree, filtered_reports)
        ReportActions.populate_report_tree(tree, filtered_reports)