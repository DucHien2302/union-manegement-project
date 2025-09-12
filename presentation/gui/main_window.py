import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from datetime import datetime
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


class MainApplication:
    """Ứng dụng chính với giao diện Tkinter"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hệ thống Quản lý Đoàn - Hội")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Maximized trên Windows
        
        # Tạo status bar đầu tiên để tránh lỗi
        self._create_minimal_status_bar()
        
        # Khởi tạo database trước
        if not self._init_database_on_startup():
            self.root.destroy()
            return
        
        # Khởi tạo use cases
        self._init_use_cases()
        
        # Tạo giao diện đầy đủ
        self._create_widgets()
    
    def _create_minimal_status_bar(self):
        """Tạo status bar tối thiểu để tránh lỗi"""
        self.status_bar = ttk.Label(self.root, text="Đang khởi tạo...", relief=tk.SUNKEN)
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
        """Tạo các widget chính"""
        # Menu bar
        self._create_menu()
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Title
        title_label = ttk.Label(main_frame, text="HỆ THỐNG QUẢN LÝ ĐOÀN - HỘI", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tạo các tab
        self._create_dashboard_tab()
        self._create_member_tab()
        self._create_report_tab()
        self._create_task_tab()
        
        # Status bar với thêm thông tin
        self._create_status_bar()
    
    def _create_status_bar(self):
        """Tạo status bar với nhiều thông tin"""
        # Xóa status bar tối thiểu nếu có
        if hasattr(self, 'status_bar'):
            self.status_bar.destroy()
        
        # Status bar frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main status label
        self.status_bar = ttk.Label(status_frame, text="Sẵn sàng", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Database status
        self.db_status_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN, width=15)
        self.db_status_label.pack(side=tk.RIGHT, padx=(2, 0))
        
        # Time label
        self.time_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN, width=20)
        self.time_label.pack(side=tk.RIGHT, padx=(2, 0))
        
        # Update time every second
        self._update_status_time()
        self._update_database_status()
    
    def _update_status_time(self):
        """Cập nhật thời gian trên status bar"""
        from datetime import datetime
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.config(text=current_time)
        # Schedule next update
        self.root.after(1000, self._update_status_time)
    
    def _update_database_status(self):
        """Cập nhật trạng thái database"""
        try:
            from infrastructure.database.connection import db_manager
            if db_manager.config.use_sqlite_fallback:
                self.db_status_label.config(text="SQLite", foreground="orange")
            else:
                self.db_status_label.config(text="SQL Server", foreground="green")
        except:
            self.db_status_label.config(text="DB Error", foreground="red")
    
    def update_status(self, message: str, temp: bool = False):
        """Cập nhật thông báo status bar
        
        Args:
            message: Thông báo cần hiển thị
            temp: Nếu True, sẽ tự động reset về "Sẵn sàng" sau 3 giây
        """
        if hasattr(self, 'status_bar') and self.status_bar.winfo_exists():
            self.status_bar.config(text=message)
            if temp:
                self.root.after(3000, lambda: self.status_bar.config(text="Sẵn sàng") if hasattr(self, 'status_bar') and self.status_bar.winfo_exists() else None)
    
    def _create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tệp", menu=file_menu)
        file_menu.add_command(label="Khởi tạo Database", command=self._init_database)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Về chương trình", command=self._show_about)
    
    def _create_dashboard_tab(self):
        """Tạo tab tổng quan"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Tổng quan")
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Thống kê tổng quan")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Member statistics
        member_stats_frame = ttk.LabelFrame(stats_frame, text="Thành viên")
        member_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.member_stats_labels = {}
        stats = ['Tổng số', 'Đoàn viên', 'Hội viên', 'Ban chấp hành', 'Đang hoạt động']
        for stat in stats:
            label = ttk.Label(member_stats_frame, text=f"{stat}: 0")
            label.pack(anchor=tk.W, padx=5, pady=2)
            self.member_stats_labels[stat] = label
        
        # Report statistics  
        report_stats_frame = ttk.LabelFrame(stats_frame, text="Báo cáo")
        report_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.report_stats_labels = {}
        stats = ['Tổng số', 'Nháp', 'Chờ duyệt', 'Đã duyệt', 'Từ chối']
        for stat in stats:
            label = ttk.Label(report_stats_frame, text=f"{stat}: 0")
            label.pack(anchor=tk.W, padx=5, pady=2)
            self.report_stats_labels[stat] = label
        
        # Task statistics
        task_stats_frame = ttk.LabelFrame(stats_frame, text="Công việc")
        task_stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.task_stats_labels = {}
        stats = ['Tổng số', 'Hoàn thành', 'Đang thực hiện', 'Quá hạn']
        for stat in stats:
            label = ttk.Label(task_stats_frame, text=f"{stat}: 0")
            label.pack(anchor=tk.W, padx=5, pady=2)
            self.task_stats_labels[stat] = label
        
        # Refresh button
        refresh_btn = ttk.Button(dashboard_frame, text="Làm mới thống kê", 
                                command=self._refresh_dashboard)
        refresh_btn.pack(pady=10)
        
        # Load initial data
        self._refresh_dashboard()
    
    def _create_member_tab(self):
        """Tạo tab quản lý thành viên"""
        member_frame = ttk.Frame(self.notebook)
        self.notebook.add(member_frame, text="Quản lý thành viên")
        
        # Toolbar
        toolbar = ttk.Frame(member_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Thêm thành viên", 
                  command=self._add_member).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Sửa thành viên", 
                  command=self._edit_member).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Xóa thành viên", 
                  command=self._delete_member).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Làm mới", 
                  command=self._refresh_members).pack(side=tk.LEFT, padx=2)
        
        # Search frame
        search_frame = ttk.Frame(member_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.member_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.member_search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.bind('<KeyRelease>', self._search_members)
        
        # Member list
        columns = ('ID', 'Mã TV', 'Họ tên', 'Loại', 'Chức vụ', 'Phòng ban', 'Trạng thái')
        self.member_tree = ttk.Treeview(member_frame, columns=columns, show='tree headings')
        
        for col in columns:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(member_frame, orient=tk.VERTICAL, command=self.member_tree.yview)
        h_scrollbar = ttk.Scrollbar(member_frame, orient=tk.HORIZONTAL, command=self.member_tree.xview)
        self.member_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.member_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X, padx=5)
        
        # Load members
        self._refresh_members()
    
    def _create_report_tab(self):
        """Tạo tab quản lý báo cáo"""
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="Quản lý báo cáo")
        
        # Toolbar
        toolbar = ttk.Frame(report_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Tạo báo cáo", 
                  command=self._add_report).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Xem/Sửa", 
                  command=self._edit_report).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Duyệt báo cáo", 
                  command=self._approve_report).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Làm mới", 
                  command=self._refresh_reports).pack(side=tk.LEFT, padx=2)
        
        # Report list
        columns = ('ID', 'Tiêu đề', 'Loại', 'Kỳ', 'Trạng thái', 'Ngày tạo')
        self.report_tree = ttk.Treeview(report_frame, columns=columns, show='tree headings')
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=120)
        
        # Scrollbars for reports
        v_scrollbar2 = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=v_scrollbar2.set)
        
        self.report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
        v_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Load reports
        self._refresh_reports()
    
    def _create_task_tab(self):
        """Tạo tab quản lý công việc"""
        task_frame = ttk.Frame(self.notebook)
        self.notebook.add(task_frame, text="Quản lý công việc")
        
        # Toolbar
        toolbar = ttk.Frame(task_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Tạo công việc", 
                  command=self._add_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Cập nhật", 
                  command=self._edit_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Hoàn thành", 
                  command=self._complete_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Làm mới", 
                  command=self._refresh_tasks).pack(side=tk.LEFT, padx=2)
        
        # Task list
        columns = ('ID', 'Tiêu đề', 'Ưu tiên', 'Trạng thái', 'Người thực hiện', 'Hạn hoàn thành', 'Tiến độ')
        self.task_tree = ttk.Treeview(task_frame, columns=columns, show='tree headings')
        
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100)
        
        # Scrollbars for tasks
        v_scrollbar3 = ttk.Scrollbar(task_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=v_scrollbar3.set)
        
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
        v_scrollbar3.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Load tasks
        self._refresh_tasks()
    
    def _refresh_dashboard(self):
        """Làm mới thống kê tổng quan"""
        try:
            # Member statistics
            member_stats = self.member_use_case.get_member_statistics()
            self.member_stats_labels['Tổng số'].config(text=f"Tổng số: {member_stats['total']}")
            self.member_stats_labels['Đoàn viên'].config(text=f"Đoàn viên: {member_stats['union_members']}")
            self.member_stats_labels['Hội viên'].config(text=f"Hội viên: {member_stats['association_members']}")
            self.member_stats_labels['Ban chấp hành'].config(text=f"Ban chấp hành: {member_stats['executives']}")
            self.member_stats_labels['Đang hoạt động'].config(text=f"Đang hoạt động: {member_stats['active']}")
            
            # Report statistics
            report_stats = self.report_use_case.get_report_statistics()
            self.report_stats_labels['Tổng số'].config(text=f"Tổng số: {report_stats['total']}")
            self.report_stats_labels['Nháp'].config(text=f"Nháp: {report_stats['draft']}")
            self.report_stats_labels['Chờ duyệt'].config(text=f"Chờ duyệt: {report_stats['submitted']}")
            self.report_stats_labels['Đã duyệt'].config(text=f"Đã duyệt: {report_stats['approved']}")
            self.report_stats_labels['Từ chối'].config(text=f"Từ chối: {report_stats['rejected']}")
            
            # Task statistics
            task_stats = self.task_use_case.get_task_statistics()
            self.task_stats_labels['Tổng số'].config(text=f"Tổng số: {task_stats['total']}")
            self.task_stats_labels['Hoàn thành'].config(text=f"Hoàn thành: {task_stats['completed']}")
            self.task_stats_labels['Đang thực hiện'].config(text=f"Đang thực hiện: {task_stats['in_progress']}")
            self.task_stats_labels['Quá hạn'].config(text=f"Quá hạn: {task_stats['overdue']}")
            
            self.update_status("Đã cập nhật thống kê", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải thống kê: {e}")
    
    def _refresh_members(self):
        """Làm mới danh sách thành viên"""
        try:
            # Clear existing items
            for item in self.member_tree.get_children():
                self.member_tree.delete(item)
            
            # Load members
            members = self.member_use_case.get_all_members()
            for member in members:
                self.member_tree.insert('', 'end', values=(
                    member.id,
                    member.member_code,
                    member.full_name,
                    member.member_type.value,
                    member.position,
                    member.department,
                    member.status.value
                ))
            
            self.update_status(f"Đã tải {len(members)} thành viên", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách thành viên: {e}")
    
    def _refresh_reports(self):
        """Làm mới danh sách báo cáo"""
        try:
            # Clear existing items
            for item in self.report_tree.get_children():
                self.report_tree.delete(item)
            
            # Load reports
            reports = self.report_use_case.get_all_reports()
            for report in reports:
                created_date = report.created_at.strftime('%d/%m/%Y') if report.created_at else ''
                self.report_tree.insert('', 'end', values=(
                    report.id,
                    report.title,
                    report.report_type.value,
                    report.period,
                    report.status.value,
                    created_date
                ))
            
            self.update_status(f"Đã tải {len(reports)} báo cáo", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách báo cáo: {e}")
    
    def _refresh_tasks(self):
        """Làm mới danh sách công việc"""
        try:
            # Clear existing items
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
            
            # Load tasks
            tasks = self.task_use_case.get_all_tasks()
            for task in tasks:
                due_date = task.due_date.strftime('%d/%m/%Y') if task.due_date else ''
                self.task_tree.insert('', 'end', values=(
                    task.id,
                    task.title,
                    task.priority.value,
                    task.status.value,
                    task.assigned_to or '',
                    due_date,
                    f"{task.progress_percentage}%"
                ))
            
            self.update_status(f"Đã tải {len(tasks)} công việc", temp=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách công việc: {e}")
    
    # Placeholder methods cho các chức năng chưa implement
    def _search_members(self, event=None):
        """Tìm kiếm thành viên"""
        # TODO: Implement search functionality
        pass
    
    def _add_member(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _edit_member(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _delete_member(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _add_report(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _edit_report(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _approve_report(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _add_task(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _edit_task(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _complete_task(self):
        messagebox.showinfo("Thông báo", "Chức năng đang được phát triển")
    
    def _init_database(self):
        """Khởi tạo database"""
        from infrastructure.database.setup import init_database
        try:
            if init_database():
                messagebox.showinfo("Thành công", "Database đã được khởi tạo thành công!")
            else:
                messagebox.showerror("Lỗi", "Không thể khởi tạo database!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khởi tạo database: {e}")
    
    def _show_about(self):
        """Hiển thị thông tin về chương trình"""
        messagebox.showinfo("Về chương trình", 
                           "Hệ thống Quản lý Đoàn - Hội\n\n"
                           "Phiên bản: 1.0\n"
                           "Sử dụng Clean Architecture\n"
                           "Database: SQL Server\n"
                           "Framework: Python + Tkinter")
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()