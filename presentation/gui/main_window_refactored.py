import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import sys
import os

# Thêm project root vào Python path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))

# Import tuyệt đối
from application.use_cases.member_management import MemberManagementUseCase
from application.use_cases.report_management import ReportManagementUseCase  
from application.use_cases.task_management import TaskManagementUseCase
from infrastructure.repositories.member_repository_impl import MemberRepository
from infrastructure.repositories.report_repository_impl import ReportRepository
from infrastructure.repositories.task_repository_impl import TaskRepository

# Import UI components
from .theme import ModernTheme, StyleManager
from .dashboard_components import DashboardTab
from .member_components import MemberTab, MemberActions, MemberForm
from .report_components import ReportTab, ReportActions, ReportForm
from .task_components import TaskTab, TaskActions, TaskForm


class MainApplication:
    """Ứng dụng chính với giao diện hiện đại và kiến trúc modular"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏛️ Union Management System")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximized trên Windows
        
        # Apply modern theme
        StyleManager.apply_theme_to_root(self.root)
        
        # Tạo status bar đầu tiên để tránh lỗi
        self._create_minimal_status_bar()
        
        # Khởi tạo database trước
        if not self._init_database_on_startup():
            self.root.destroy()
            return
        
        # Khởi tạo use cases
        self._init_use_cases()
        
        # Storage for components
        self.dashboard_cards = {}
        self.all_members = []
        self.all_reports = []
        self.all_tasks = []
        
        # Tạo giao diện đầy đủ
        self._create_widgets()
    
    def _create_minimal_status_bar(self):
        """Tạo status bar tối thiểu để tránh lỗi"""
        self.status_bar = tk.Label(self.root, text="Đang khởi tạo...", 
                                  relief=tk.SUNKEN, anchor=tk.W,
                                  bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _init_database_on_startup(self) -> bool:
        """Khởi tạo database khi chạy ứng dụng"""
        try:
            from infrastructure.database.setup import init_database
            print("🔧 Checking and initializing database...")
            
            if init_database():
                print("✅ Database ready!")
                return True
            else:
                messagebox.showerror("Lỗi Database", 
                    "Không thể khởi tạo database!\n"
                    "Vui lòng kiểm tra:\n"
                    "1. SQL Server đang chạy\n"
                    "2. Thông tin kết nối trong file .env\n"
                    "3. Quyền tạo database")
                return False
        except Exception as e:
            messagebox.showerror("Lỗi Database", f"Lỗi khởi tạo database: {e}")
            return False
        
    def _init_use_cases(self):
        """Khởi tạo các use cases"""
        try:
            # Repositories
            member_repo = MemberRepository()
            report_repo = ReportRepository()
            task_repo = TaskRepository()
            
            # Use cases
            self.member_use_case = MemberManagementUseCase(member_repo)
            self.report_use_case = ReportManagementUseCase(report_repo)
            self.task_use_case = TaskManagementUseCase(task_repo)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối database: {e}")
            self.root.destroy()
    
    def _create_widgets(self):
        """Tạo giao diện hiện đại"""
        # Create main container
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_header(self):
        """Tạo header hiện đại với branding và navigation"""
        # Header container
        header_frame = tk.Frame(self.root, bg=ModernTheme.WHITE, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 1))
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=ModernTheme.WHITE)
        header_content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, pady=ModernTheme.PADDING_MEDIUM)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Logo (emoji as placeholder)
        logo_label = tk.Label(left_frame, text="🏛️", font=("Segoe UI", 24), 
                             bg=ModernTheme.WHITE, fg=ModernTheme.PRIMARY)
        logo_label.pack(side=tk.LEFT, padx=(0, 12))
        
        # Title and subtitle
        title_frame = tk.Frame(left_frame, bg=ModernTheme.WHITE)
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(title_frame, text="Union Management", 
                              font=("Segoe UI", 18, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame, text="Hệ thống quản lý đoàn - hội", 
                                 font=ModernTheme.FONT_PRIMARY,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
        subtitle_label.pack(anchor=tk.W)
        
        # Right side - Quick actions
        right_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Quick action buttons
        quick_actions = [
            ("🔄", "Làm mới", self._refresh_all_data),
            ("📊", "Thống kê", self._show_statistics),
            ("⚙️", "Cài đặt", self._show_settings),
        ]
        
        for icon, tooltip, command in quick_actions:
            btn = tk.Button(right_frame, text=icon, font=("Segoe UI", 16),
                           bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                           border=0, cursor="hand2", padx=12, pady=8,
                           command=command)
            btn.pack(side=tk.RIGHT, padx=2)
            
            # Add tooltip (simplified)
            btn.bind("<Enter>", lambda e, t=tooltip: self.update_status(t, temp=True))
            btn.bind("<Leave>", lambda e: self.update_status(""))
    
    def _create_main_content(self):
        """Tạo nội dung chính"""
        # Main container
        main_container = tk.Frame(self.root, bg=ModernTheme.GRAY_50)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook with modern style
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs using component modules
        self._create_tabs()
    
    def _create_tabs(self):
        """Tạo các tabs sử dụng component modules"""
        # Dashboard tab
        dashboard_frame, self.dashboard_cards = DashboardTab.create_dashboard_tab(
            self.notebook, 
            notebook_ref=self.notebook,
            quick_action_callbacks={
                'add_member': self._add_member_quick,
                'create_report': self._create_report_quick,
                'create_task': self._create_task_quick,
                'view_statistics': self._view_statistics
            }
        )
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Member tab
        member_frame, self.member_tree, self.member_search_var = MemberTab.create_member_tab(
            self.notebook,
            callbacks={
                'add_member': self._add_member,
                'edit_member': self._edit_member,
                'delete_member': self._delete_member,
                'search_members': self._search_members
            }
        )
        self.notebook.add(member_frame, text="👥 Thành viên")
        
        # Report tab
        report_frame, self.report_tree, self.report_search_var, self.report_filter_vars = ReportTab.create_report_tab(
            self.notebook,
            callbacks={
                'add_report': self._add_report,
                'edit_report': self._edit_report,
                'view_report': self._view_report,
                'delete_report': self._delete_report,
                'approve_report': self._approve_report,
                'search_reports': self._search_reports,
                'filter_reports': self._filter_reports,
                'export_reports': self._export_reports,
                'bulk_action': self._bulk_action_reports,
                'refresh_data': self._refresh_reports
            }
        )
        self.notebook.add(report_frame, text="📋 Báo cáo")
        
        # Task tab
        task_frame, self.task_tree, self.task_search_var, self.task_filter_vars = TaskTab.create_task_tab(
            self.notebook,
            callbacks={
                'add_task': self._add_task,
                'edit_task': self._edit_task,
                'view_task': self._view_task,
                'complete_task': self._complete_task,
                'delete_task': self._delete_task,
                'search_tasks': self._search_tasks,
                'filter_tasks': self._filter_tasks,
                'export_tasks': self._export_tasks,
                'bulk_action': self._bulk_action_tasks,
                'refresh_data': self._refresh_tasks
            }
        )
        self.notebook.add(task_frame, text="✅ Công việc")
        
        # Load initial data
        self._load_initial_data()
    
    def _create_status_bar(self):
        """Tạo status bar hiện đại"""
        # Remove old status bar if exists
        if hasattr(self, 'status_bar'):
            self.status_bar.destroy()
        
        self.status_bar = tk.Frame(self.root, bg=ModernTheme.GRAY_100, height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        # Status content
        status_content = tk.Frame(self.status_bar, bg=ModernTheme.GRAY_100)
        status_content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_MEDIUM, 
                           pady=4)
        
        # Status text
        self.status_label = tk.Label(status_content, text="Sẵn sàng", 
                                    font=ModernTheme.FONT_SMALL,
                                    bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                                    anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Connection status
        self.connection_label = tk.Label(status_content, text="🟢 Đã kết nối", 
                                        font=ModernTheme.FONT_SMALL,
                                        bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_600)
        self.connection_label.pack(side=tk.RIGHT)
        
        # Update status
        self.update_status("Hệ thống sẵn sàng")
        
        # Refresh dashboard after startup
        self.root.after(500, self._refresh_dashboard)
    
    def update_status(self, message: str, temp: bool = False):
        """Cập nhật status bar"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            if temp:
                self.root.after(3000, lambda: self.update_status("Sẵn sàng"))
    
    # Data loading methods
    def _load_initial_data(self):
        """Load initial data for all tabs"""
        self._refresh_members()
        self._refresh_reports()
        self._refresh_tasks()
    
    def _refresh_members(self):
        """Làm mới danh sách thành viên"""
        try:
            self.all_members = self.member_use_case.get_all_members()
            MemberActions.populate_member_tree(self.member_tree, self.all_members)
            self.update_status(f"Đã tải {len(self.all_members)} thành viên", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách thành viên: {e}")
    
    def _refresh_reports(self):
        """Làm mới danh sách báo cáo"""
        try:
            self.all_reports = self.report_use_case.get_all_reports()
            ReportActions.populate_report_tree(self.report_tree, self.all_reports)
            self.update_status(f"Đã tải {len(self.all_reports)} báo cáo", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách báo cáo: {e}")
    
    def _refresh_tasks(self):
        """Làm mới danh sách công việc"""
        try:
            self.all_tasks = self.task_use_case.get_all_tasks()
            TaskActions.populate_task_tree(self.task_tree, self.all_tasks)
            self.update_status(f"Đã tải {len(self.all_tasks)} công việc", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách công việc: {e}")
    
    def _refresh_dashboard(self):
        """Làm mới thống kê dashboard"""
        try:
            # Member statistics
            member_stats = self.member_use_case.get_member_statistics()
            if 'thành viên_card' in self.dashboard_cards:
                card = self.dashboard_cards['thành viên_card']
                card.number_label.config(text=str(member_stats['total']))
                card.subtitle_label.config(text=f"Đang hoạt động: {member_stats['active']}")
            
            # Report statistics  
            report_stats = self.report_use_case.get_report_statistics()
            if 'báo cáo_card' in self.dashboard_cards:
                card = self.dashboard_cards['báo cáo_card']
                card.number_label.config(text=str(report_stats['total']))
                card.subtitle_label.config(text=f"Chờ duyệt: {report_stats['submitted']}")
            
            # Task statistics
            task_stats = self.task_use_case.get_task_statistics()
            if 'công việc_card' in self.dashboard_cards:
                card = self.dashboard_cards['công việc_card']
                card.number_label.config(text=str(task_stats['total']))
                card.subtitle_label.config(text=f"Hoàn thành: {task_stats['completed']}")
            
            self.update_status("Đã cập nhật thống kê", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thống kê: {e}")
    
    # Quick action methods for dashboard
    def _add_member_quick(self):
        """Quick action: Thêm thành viên"""
        self.notebook.select(1)
        self.update_status("Chuyển đến tab Thành viên", temp=True)
    
    def _create_report_quick(self):
        """Quick action: Tạo báo cáo"""
        self.notebook.select(2)
        self.update_status("Chuyển đến tab Báo cáo", temp=True)
    
    def _create_task_quick(self):
        """Quick action: Tạo công việc"""
        self.notebook.select(3)
        self.update_status("Chuyển đến tab Công việc", temp=True)
    
    def _view_statistics(self):
        """Quick action: Xem thống kê"""
        self._refresh_dashboard()
        self.update_status("Đã làm mới thống kê", temp=True)
    
    # Member management methods
    def _add_member(self):
        """Thêm thành viên mới"""
        result = MemberForm.create_member_form_dialog(self.root, "Thêm thành viên mới")
        if result:
            try:
                # TODO: Implement actual member creation
                messagebox.showinfo("Thành công", "Thêm thành viên thành công!")
                self._refresh_members()
                self._refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm thành viên: {e}")
    
    def _edit_member(self):
        """Sửa thông tin thành viên"""
        member_id = MemberActions.get_selected_member_id(self.member_tree)
        if not member_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thành viên cần sửa!")
            return
        
        # TODO: Get member data and show edit form
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _delete_member(self):
        """Xóa thành viên"""
        member_id = MemberActions.get_selected_member_id(self.member_tree)
        if not member_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thành viên cần xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa thành viên này?"):
            # TODO: Implement actual member deletion
            messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _search_members(self, event=None):
        """Tìm kiếm thành viên"""
        search_term = self.member_search_var.get()
        MemberActions.search_members(self.member_tree, search_term, self.all_members)
    
    # Report management methods
    def _add_report(self):
        """Tạo báo cáo mới"""
        result = ReportForm.create_report_form_dialog(self.root, "Tạo báo cáo mới")
        if result:
            try:
                # TODO: Implement actual report creation
                messagebox.showinfo("Thành công", "Tạo báo cáo thành công!")
                self._refresh_reports()
                self._refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {e}")
    
    def _edit_report(self):
        """Sửa báo cáo"""
        report_id = ReportActions.get_selected_report_id(self.report_tree)
        if not report_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn báo cáo cần sửa!")
            return
        
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _approve_report(self):
        """Duyệt báo cáo"""
        report_id = ReportActions.get_selected_report_id(self.report_tree)
        if not report_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn báo cáo cần duyệt!")
            return
        
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")

    def _view_report(self):
        """Xem báo cáo"""
        self._edit_report()  # Reuse edit for now

    def _delete_report(self):
        """Xóa báo cáo"""
        report_id = ReportActions.get_selected_report_id(self.report_tree)
        if not report_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn báo cáo cần xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa báo cáo này?"):
            messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")

    def _search_reports(self, event=None):
        """Tìm kiếm báo cáo"""
        try:
            search_term = getattr(self, 'report_search_var', tk.StringVar()).get()
            if search_term and search_term != "Tìm kiếm báo cáo...":
                # Implement search logic here
                pass
        except Exception as e:
            print(f"Search error: {e}")

    def _export_reports(self):
        """Xuất danh sách báo cáo"""
        messagebox.showinfo("Thông báo", "Tính năng xuất Excel sẽ được cập nhật trong phiên bản sau!")

    def _bulk_action_reports(self, action):
        """Thao tác hàng loạt cho báo cáo"""
        messagebox.showinfo("Thông báo", f"Đã thực hiện {action} cho các báo cáo được chọn!")

    def _refresh_reports(self):
        """Làm mới danh sách báo cáo"""
        try:
            self.all_reports = self.report_use_case.get_all_reports()
            ReportActions.populate_report_tree(self.report_tree, self.all_reports)
            self.update_status(f"Đã tải {len(self.all_reports)} báo cáo", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách báo cáo: {e}")
    
    def _filter_reports(self, event=None):
        """Lọc báo cáo theo nhiều tiêu chí"""
        try:
            # Lấy tất cả filter values
            report_type_filter = self.report_filter_vars.get('report_type', tk.StringVar()).get()
            period_filter = self.report_filter_vars.get('period', tk.StringVar()).get()
            status_filter = self.report_filter_vars.get('status', tk.StringVar()).get()
            
            print(f"🔍 Debug - Report filters: Type={report_type_filter}, Period={period_filter}, Status={status_filter}")
            
            # Lọc dữ liệu
            filtered_reports = []
            for report in self.all_reports:
                # Kiểm tra từng filter
                if report_type_filter and report_type_filter != "Tất cả":
                    if hasattr(report, 'report_type') and str(report.report_type) != report_type_filter:
                        continue
                
                if period_filter and period_filter != "Tất cả":
                    if hasattr(report, 'period') and str(report.period) != period_filter:
                        continue
                
                if status_filter and status_filter != "Tất cả":
                    if hasattr(report, 'status') and str(report.status) != status_filter:
                        continue
                
                filtered_reports.append(report)
            
            # Cập nhật table với dữ liệu đã lọc
            ReportActions.populate_report_tree(self.report_tree, filtered_reports)
            self.update_status(f"Đã lọc {len(filtered_reports)}/{len(self.all_reports)} báo cáo", temp=True)
            
        except Exception as e:
            print(f"❌ Filter reports error: {e}")
            # Fallback to show all reports
            ReportActions.populate_report_tree(self.report_tree, self.all_reports)
    
    # Task management methods
    def _add_task(self):
        """Tạo công việc mới"""
        result = TaskForm.create_task_form_dialog(self.root, "Tạo công việc mới")
        if result:
            try:
                # TODO: Implement actual task creation
                messagebox.showinfo("Thành công", "Tạo công việc thành công!")
                self._refresh_tasks()
                self._refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo công việc: {e}")
    
    def _edit_task(self):
        """Sửa công việc"""
        task_id = TaskActions.get_selected_task_id(self.task_tree)
        if not task_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc cần sửa!")
            return
        
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _complete_task(self):
        """Hoàn thành công việc"""
        task_id = TaskActions.get_selected_task_id(self.task_tree)
        if not task_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc cần hoàn thành!")
            return
        
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")

    def _view_task(self):
        """Xem công việc"""
        self._edit_task()  # Reuse edit for now

    def _delete_task(self):
        """Xóa công việc"""
        task_id = TaskActions.get_selected_task_id(self.task_tree)
        if not task_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc cần xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa công việc này?"):
            messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")

    def _search_tasks(self, event=None):
        """Tìm kiếm công việc"""
        try:
            search_term = getattr(self, 'task_search_var', tk.StringVar()).get()
            if search_term and search_term != "Tìm kiếm công việc...":
                # Implement search logic here
                pass
        except Exception as e:
            print(f"Search error: {e}")

    def _export_tasks(self):
        """Xuất danh sách công việc"""
        messagebox.showinfo("Thông báo", "Tính năng xuất Excel sẽ được cập nhật trong phiên bản sau!")

    def _bulk_action_tasks(self, action):
        """Thao tác hàng loạt cho công việc"""
        messagebox.showinfo("Thông báo", f"Đã thực hiện {action} cho các công việc được chọn!")

    def _refresh_tasks(self):
        """Làm mới danh sách công việc"""
        try:
            self.all_tasks = self.task_use_case.get_all_tasks()
            TaskActions.populate_task_tree(self.task_tree, self.all_tasks)
            self.update_status(f"Đã tải {len(self.all_tasks)} công việc", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách công việc: {e}")
    
    def _filter_tasks(self, event=None):
        """Lọc công việc theo nhiều tiêu chí"""
        try:
            # Lấy tất cả filter values
            priority_filter = self.task_filter_vars.get('priority', tk.StringVar()).get()
            status_filter = self.task_filter_vars.get('status', tk.StringVar()).get()
            assignee_filter = self.task_filter_vars.get('assignee', tk.StringVar()).get()
            
            print(f"🔍 Debug - Task filters: Priority={priority_filter}, Status={status_filter}, Assignee={assignee_filter}")
            
            # Lọc dữ liệu
            filtered_tasks = []
            for task in self.all_tasks:
                # Kiểm tra từng filter
                if priority_filter and priority_filter != "Tất cả":
                    priority_mapping = {
                        'Thấp': 'low',
                        'Trung bình': 'medium', 
                        'Cao': 'high',
                        'Khẩn cấp': 'urgent'
                    }
                    db_priority = priority_mapping.get(priority_filter, priority_filter.lower())
                    task_priority = task.priority.value if hasattr(task.priority, 'value') else str(task.priority)
                    if task_priority != db_priority:
                        continue
                
                if status_filter and status_filter != "Tất cả":
                    status_mapping = {
                        'Chờ thực hiện': 'not_started',
                        'Đang thực hiện': 'in_progress',
                        'Hoàn thành': 'completed',
                        'Tạm dừng': 'on_hold'
                    }
                    db_status = status_mapping.get(status_filter, status_filter.lower())
                    task_status = task.status.value if hasattr(task.status, 'value') else str(task.status)
                    if task_status != db_status:
                        continue
                
                if assignee_filter and assignee_filter != "Tất cả":
                    # TODO: Implement assignee filtering logic based on current user
                    pass
                
                filtered_tasks.append(task)
            
            # Cập nhật table với dữ liệu đã lọc
            TaskActions.populate_task_tree(self.task_tree, filtered_tasks)
            self.update_status(f"Đã lọc {len(filtered_tasks)}/{len(self.all_tasks)} công việc", temp=True)
            
        except Exception as e:
            print(f"❌ Filter tasks error: {e}")
            # Fallback to show all tasks
            TaskActions.populate_task_tree(self.task_tree, self.all_tasks)
    
    # Header action methods
    def _refresh_all_data(self):
        """Làm mới tất cả dữ liệu"""
        self._load_initial_data()
        self._refresh_dashboard()
        self.update_status("Đã làm mới tất cả dữ liệu", temp=True)
    
    def _show_statistics(self):
        """Hiển thị thống kê chi tiết"""
        self.notebook.select(0)  # Switch to dashboard
        self._refresh_dashboard()
    
    def _show_settings(self):
        """Hiển thị cài đặt"""
        messagebox.showinfo("Cài đặt", "Chức năng cài đặt đang được phát triển")
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()