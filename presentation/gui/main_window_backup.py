import tkinter as tk
from tkinter import ttk, messagebox, font
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


class ModernTheme:
    """Modern UI Theme Configuration"""
    
    # Color Palette
    PRIMARY = "#2563eb"      # Modern blue
    PRIMARY_LIGHT = "#3b82f6"
    PRIMARY_DARK = "#1d4ed8"
    
    SECONDARY = "#10b981"    # Green
    SECONDARY_LIGHT = "#34d399"
    
    ACCENT = "#8b5cf6"       # Purple
    WARNING = "#f59e0b"      # Amber
    DANGER = "#ef4444"       # Red
    
    # Neutrals
    WHITE = "#ffffff"
    GRAY_50 = "#f9fafb"
    GRAY_100 = "#f3f4f6"
    GRAY_200 = "#e5e7eb"
    GRAY_300 = "#d1d5db"
    GRAY_400 = "#9ca3af"
    GRAY_500 = "#6b7280"
    GRAY_600 = "#4b5563"
    GRAY_700 = "#374151"
    GRAY_800 = "#1f2937"
    GRAY_900 = "#111827"
    
    # Typography
    FONT_PRIMARY = ("Segoe UI", 10)
    FONT_HEADING = ("Segoe UI", 14, "bold")
    FONT_SUBHEADING = ("Segoe UI", 12, "bold")
    FONT_SMALL = ("Segoe UI", 8)
    
    # Spacing
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24
    
    # Border Radius (simulated)
    BORDER_RADIUS = 8


class MainApplication:
    """Ứng dụng chính với giao diện hiện đại"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏛️ Union Management System")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximized trên Windows
        
        # Apply modern theme
        self._configure_theme()
        
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
    
    def _configure_theme(self):
        """Cấu hình theme hiện đại"""
        self.root.configure(bg=ModernTheme.GRAY_50)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook (tabs)
        style.configure('Modern.TNotebook', 
                       background=ModernTheme.WHITE,
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       padding=[20, 12],
                       font=ModernTheme.FONT_SUBHEADING,
                       background=ModernTheme.GRAY_100,
                       foreground=ModernTheme.GRAY_700)
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', ModernTheme.PRIMARY),
                           ('active', ModernTheme.PRIMARY_LIGHT)],
                 foreground=[('selected', ModernTheme.WHITE),
                           ('active', ModernTheme.WHITE)])
        
        # Configure frames
        style.configure('Card.TFrame',
                       background=ModernTheme.WHITE,
                       relief='flat',
                       borderwidth=1)
        
        # Configure labels
        style.configure('Heading.TLabel',
                       font=ModernTheme.FONT_HEADING,
                       foreground=ModernTheme.GRAY_900,
                       background=ModernTheme.WHITE)
        
        style.configure('Subheading.TLabel',
                       font=ModernTheme.FONT_SUBHEADING,
                       foreground=ModernTheme.GRAY_700,
                       background=ModernTheme.WHITE)
        
        # Configure buttons
        style.configure('Primary.TButton',
                       font=ModernTheme.FONT_PRIMARY,
                       foreground=ModernTheme.WHITE,
                       background=ModernTheme.PRIMARY,
                       borderwidth=0,
                       focuscolor='none',
                       padding=[16, 8])
        style.map('Primary.TButton',
                 background=[('active', ModernTheme.PRIMARY_LIGHT),
                           ('pressed', ModernTheme.PRIMARY_DARK)])
        
        style.configure('Secondary.TButton',
                       font=ModernTheme.FONT_PRIMARY,
                       foreground=ModernTheme.GRAY_700,
                       background=ModernTheme.GRAY_100,
                       borderwidth=0,
                       focuscolor='none',
                       padding=[16, 8])
        
        # Configure treeview
        style.configure('Modern.Treeview',
                       background=ModernTheme.WHITE,
                       foreground=ModernTheme.GRAY_900,
                       rowheight=35,
                       fieldbackground=ModernTheme.WHITE,
                       borderwidth=0)
        style.configure('Modern.Treeview.Heading',
                       font=ModernTheme.FONT_SUBHEADING,
                       foreground=ModernTheme.GRAY_700,
                       background=ModernTheme.GRAY_100,
                       borderwidth=1,
                       relief='flat')
        
        # Configure entry
        style.configure('Modern.TEntry',
                       fieldbackground=ModernTheme.WHITE,
                       borderwidth=1,
                       relief='solid',
                       padding=[12, 8])
    
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
        """Tạo giao diện hiện đại"""
        # Configure modern styles first
        self._configure_modern_styles()
        
        # Create main container
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
    
    def _configure_modern_styles(self):
        """Configure modern styles for ttk widgets"""
        style = ttk.Style()
        
        # Configure Treeview style
        style.configure("Modern.Treeview",
                       background=ModernTheme.WHITE,
                       foreground=ModernTheme.GRAY_900,
                       rowheight=40,
                       fieldbackground=ModernTheme.WHITE,
                       borderwidth=0)
        
        style.configure("Modern.Treeview.Heading",
                       background=ModernTheme.GRAY_100,
                       foreground=ModernTheme.GRAY_700,
                       relief="flat",
                       borderwidth=1)
        
        # Configure Notebook style
        style.configure("Modern.TNotebook",
                       background=ModernTheme.GRAY_50,
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure("Modern.TNotebook.Tab",
                       background=ModernTheme.GRAY_200,
                       foreground=ModernTheme.GRAY_700,
                       padding=[20, 12],
                       borderwidth=0)
        
        style.map("Modern.TNotebook.Tab",
                 background=[('selected', ModernTheme.WHITE),
                           ('active', ModernTheme.GRAY_100)])
        
        style.map("Modern.TNotebook.Tab",
                 foreground=[('selected', ModernTheme.GRAY_900),
                           ('active', ModernTheme.GRAY_800)])
    
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
        
        subtitle_label = tk.Label(title_frame, text="Hệ thống quản lý đoàn hội hiện đại", 
                                 font=ModernTheme.FONT_PRIMARY,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        subtitle_label.pack(anchor=tk.W)
        
        # Right side - Quick actions
        right_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Quick action buttons
        self._create_quick_actions(right_frame)
    
    def _create_quick_actions(self, parent):
        """Tạo quick action buttons"""
        actions = [
            ("➕", "Thêm thành viên", self._add_member_quick),
            ("📊", "Báo cáo", self._view_reports_quick),
            ("⚙️", "Cài đặt", self._show_settings),
        ]
        
        for icon, tooltip, command in actions:
            btn = tk.Button(parent, text=icon, font=("Segoe UI", 16),
                           bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                           border=0, cursor="hand2", width=3, height=1,
                           relief=tk.FLAT)
            btn.pack(side=tk.RIGHT, padx=4)
            btn.configure(command=command)
            
        # Hover effects với animation-like behavior
        def on_enter(e, button=btn):
            button.configure(bg=ModernTheme.GRAY_200)
            # Simulate animation with after method
            def animate_in():
                button.configure(relief=tk.RAISED, borderwidth=1)
            self.root.after(50, animate_in)
            
        def on_leave(e, button=btn):
            button.configure(bg=ModernTheme.GRAY_100)
            def animate_out():
                button.configure(relief=tk.FLAT, borderwidth=0)
            self.root.after(50, animate_out)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _create_main_content(self):
        """Tạo nội dung chính"""
        # Main container
        main_container = tk.Frame(self.root, bg=ModernTheme.GRAY_50)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Notebook với style hiện đại
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_MEDIUM, 
                          pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Tạo các tab với icon
        self._create_dashboard_tab()
        self._create_member_tab()
        self._create_report_tab()
        self._create_task_tab()
    
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
    
    # Quick Action Methods
    def _add_member_quick(self):
        """Quick action: Thêm thành viên"""
        self.notebook.select(1)  # Switch to member tab
        self.update_status("Chuyển đến tab Thành viên", temp=True)
    
    def _view_reports_quick(self):
        """Quick action: Xem báo cáo"""
        self.notebook.select(2)  # Switch to reports tab
        self.update_status("Chuyển đến tab Báo cáo", temp=True)
    
    def _show_settings(self):
        """Quick action: Hiển thị cài đặt"""
        self.update_status("Tính năng cài đặt đang phát triển", temp=True)
    
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
        """Tạo dashboard hiện đại với cards"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Create scrollable container
        canvas = tk.Canvas(dashboard_frame, bg=ModernTheme.GRAY_50, highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Welcome section
        self._create_welcome_section(scrollable_frame)
        
        # Statistics cards
        self._create_stats_cards(scrollable_frame)
        
        # Quick actions section
        self._create_quick_actions_section(scrollable_frame)
        
        # Recent activities
        self._create_recent_activities(scrollable_frame)
        
        # Load initial data
        self._refresh_dashboard()
    
    def _create_welcome_section(self, parent):
        """Tạo welcome section"""
        welcome_frame = tk.Frame(parent, bg=ModernTheme.WHITE, relief=tk.FLAT, bd=1)
        welcome_frame.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                          pady=(ModernTheme.PADDING_MEDIUM, ModernTheme.PADDING_SMALL))
        
        # Welcome content
        content_frame = tk.Frame(welcome_frame, bg=ModernTheme.WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                          pady=ModernTheme.PADDING_LARGE)
        
        # Welcome text
        welcome_label = tk.Label(content_frame, text="Chào mừng trở lại! 👋", 
                                font=("Segoe UI", 20, "bold"),
                                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        welcome_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(content_frame, text="Quản lý đoàn hội hiệu quả với dashboard tổng quan", 
                                 font=ModernTheme.FONT_PRIMARY,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
        subtitle_label.pack(anchor=tk.W, pady=(4, 0))
    
    def _create_stats_cards(self, parent):
        """Tạo statistics cards"""
        # Stats container
        stats_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        stats_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                            pady=ModernTheme.PADDING_SMALL)
        
        # Title
        title_label = tk.Label(stats_container, text="Thống kê tổng quan", 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Cards grid
        cards_frame = tk.Frame(stats_container, bg=ModernTheme.GRAY_50)
        cards_frame.pack(fill=tk.X)
        
        # Member stats card
        self.member_card = self._create_stat_card(cards_frame, "👥", "Thành viên", 
                                                 ModernTheme.PRIMARY, 0)
        self.member_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                             padx=(0, ModernTheme.PADDING_SMALL))
        
        # Report stats card
        self.report_card = self._create_stat_card(cards_frame, "📋", "Báo cáo", 
                                                 ModernTheme.SECONDARY, 1)
        self.report_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                             padx=ModernTheme.PADDING_SMALL)
        
        # Task stats card
        self.task_card = self._create_stat_card(cards_frame, "✅", "Công việc", 
                                               ModernTheme.ACCENT, 2)
        self.task_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                           padx=(ModernTheme.PADDING_SMALL, 0))
    
    def _create_stat_card(self, parent, icon, title, color, tab_index):
        """Tạo một stat card"""
        card = tk.Frame(parent, bg=ModernTheme.WHITE, relief=tk.FLAT, bd=1, cursor="hand2")
        
        # Card content
        content = tk.Frame(card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                    pady=ModernTheme.PADDING_LARGE)
        
        # Icon and title row
        header = tk.Frame(content, bg=ModernTheme.WHITE)
        header.pack(fill=tk.X)
        
        icon_label = tk.Label(header, text=icon, font=("Segoe UI", 24),
                             bg=ModernTheme.WHITE, fg=color)
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(header, text=title, font=ModernTheme.FONT_SUBHEADING,
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
        title_label.pack(side=tk.RIGHT)
        
        # Main number
        number_label = tk.Label(content, text="0", font=("Segoe UI", 32, "bold"),
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        number_label.pack(anchor=tk.W, pady=(ModernTheme.PADDING_MEDIUM, 0))
        
        # Subtitle
        subtitle_label = tk.Label(content, text="Tổng số", font=ModernTheme.FONT_SMALL,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        subtitle_label.pack(anchor=tk.W)
        
        # Store references for updates
        setattr(card, 'number_label', number_label)
        setattr(card, 'subtitle_label', subtitle_label)
        
        # Click handler
        def on_click(event, index=tab_index):
            self.notebook.select(index + 1)  # +1 because dashboard is at 0
        
        # Bind click events
        for widget in [card, content, header, icon_label, title_label, number_label, subtitle_label]:
            widget.bind("<Button-1>", on_click)
        
        # Hover effects
        def on_enter(event):
            card.configure(bg=ModernTheme.GRAY_50)
            content.configure(bg=ModernTheme.GRAY_50)
            header.configure(bg=ModernTheme.GRAY_50)
            for widget in [icon_label, title_label, number_label, subtitle_label]:
                widget.configure(bg=ModernTheme.GRAY_50)
                
        def on_leave(event):
            card.configure(bg=ModernTheme.WHITE)
            content.configure(bg=ModernTheme.WHITE)
            header.configure(bg=ModernTheme.WHITE)
            for widget in [icon_label, title_label, number_label, subtitle_label]:
                widget.configure(bg=ModernTheme.WHITE)
        
        for widget in [card, content, header, icon_label, title_label, number_label, subtitle_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        return card
    
    def _create_quick_actions_section(self, parent):
        """Tạo quick actions section"""
        actions_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        actions_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                              pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(actions_container, text="Thao tác nhanh", 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Actions grid
        actions_frame = tk.Frame(actions_container, bg=ModernTheme.GRAY_50)
        actions_frame.pack(fill=tk.X)
        
        actions = [
            ("➕", "Thêm thành viên", "Tạo hồ sơ thành viên mới", self._add_member_quick),
            ("📝", "Tạo báo cáo", "Soạn báo cáo mới", self._create_report_quick),
            ("📋", "Giao việc", "Phân công công việc mới", self._create_task_quick),
            ("📊", "Xem thống kê", "Chi tiết thống kê và báo cáo", self._view_statistics),
        ]
        
        for i, (icon, title, subtitle, command) in enumerate(actions):
            action_card = self._create_action_card(actions_frame, icon, title, subtitle, command)
            action_card.grid(row=i//2, column=i%2, sticky="ew", 
                           padx=(0, ModernTheme.PADDING_SMALL) if i%2==0 else (ModernTheme.PADDING_SMALL, 0),
                           pady=ModernTheme.PADDING_SMALL)
            
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
    
    def _create_action_card(self, parent, icon, title, subtitle, command):
        """Tạo action card"""
        card = tk.Frame(parent, bg=ModernTheme.WHITE, relief=tk.FLAT, bd=1, cursor="hand2")
        
        # Card content
        content = tk.Frame(card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                    pady=ModernTheme.PADDING_MEDIUM)
        
        # Icon
        icon_label = tk.Label(content, text=icon, font=("Segoe UI", 20),
                             bg=ModernTheme.WHITE, fg=ModernTheme.PRIMARY)
        icon_label.pack(anchor=tk.W)
        
        # Title
        title_label = tk.Label(content, text=title, font=ModernTheme.FONT_SUBHEADING,
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(4, 0))
        
        # Subtitle
        subtitle_label = tk.Label(content, text=subtitle, font=ModernTheme.FONT_SMALL,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        subtitle_label.pack(anchor=tk.W)
        
        # Click handlers
        for widget in [card, content, icon_label, title_label, subtitle_label]:
            widget.bind("<Button-1>", lambda e: command())
        
        # Hover effects
        def on_enter(event):
            card.configure(bg=ModernTheme.GRAY_50)
            content.configure(bg=ModernTheme.GRAY_50)
            for widget in [icon_label, title_label, subtitle_label]:
                widget.configure(bg=ModernTheme.GRAY_50)
                
        def on_leave(event):
            card.configure(bg=ModernTheme.WHITE)
            content.configure(bg=ModernTheme.WHITE)
            for widget in [icon_label, title_label, subtitle_label]:
                widget.configure(bg=ModernTheme.WHITE)
        
        for widget in [card, content, icon_label, title_label, subtitle_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        return card
    
    def _create_recent_activities(self, parent):
        """Tạo recent activities section"""
        activities_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        activities_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                                 pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(activities_container, text="Hoạt động gần đây", 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Activities card
        activities_card = tk.Frame(activities_container, bg=ModernTheme.WHITE, relief=tk.FLAT, bd=1)
        activities_card.pack(fill=tk.X)
        
        # Activities content
        content = tk.Frame(activities_card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                    pady=ModernTheme.PADDING_LARGE)
        
        # Placeholder activities
        activities = [
            ("👤", "Thành viên mới được thêm", "2 phút trước"),
            ("📋", "Báo cáo tháng 9 được duyệt", "1 giờ trước"),
            ("✅", "Hoàn thành công việc tổ chức sự kiện", "3 giờ trước"),
        ]
        
        for icon, activity, time in activities:
            activity_row = tk.Frame(content, bg=ModernTheme.WHITE)
            activity_row.pack(fill=tk.X, pady=4)
            
            icon_label = tk.Label(activity_row, text=icon, font=("Segoe UI", 14),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
            icon_label.pack(side=tk.LEFT, padx=(0, 12))
            
            text_frame = tk.Frame(activity_row, bg=ModernTheme.WHITE)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            activity_label = tk.Label(text_frame, text=activity, font=ModernTheme.FONT_PRIMARY,
                                     bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900, anchor=tk.W)
            activity_label.pack(fill=tk.X)
            
            time_label = tk.Label(text_frame, text=time, font=ModernTheme.FONT_SMALL,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500, anchor=tk.W)
            time_label.pack(fill=tk.X)
    
    # Quick action methods for dashboard
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
    
    def _create_member_tab(self):
        """Tạo tab quản lý thành viên"""
        member_frame = ttk.Frame(self.notebook)
        self.notebook.add(member_frame, text="👥 Thành viên")
        
        # Create modern layout
        self._create_modern_member_layout(member_frame)
    
    def _create_modern_member_layout(self, parent):
        """Tạo layout hiện đại cho member tab"""
        # Header section
        header_frame = tk.Frame(parent, bg=ModernTheme.WHITE, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 1))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=ModernTheme.WHITE)
        header_content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(header_content, text="Quản lý Thành viên", 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
        action_frame.pack(side=tk.RIGHT)
        
        # Primary button
        add_btn = tk.Button(action_frame, text="➕ Thêm thành viên", 
                           font=ModernTheme.FONT_PRIMARY,
                           bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                           border=0, cursor="hand2", padx=16, pady=8,
                           command=self._add_member)
        add_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Secondary buttons
        for text, command in [("✏️ Sửa", self._edit_member), ("🗑️ Xóa", self._delete_member)]:
            btn = tk.Button(action_frame, text=text, 
                           font=ModernTheme.FONT_PRIMARY,
                           bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                           border=0, cursor="hand2", padx=12, pady=8,
                           command=command)
            btn.pack(side=tk.RIGHT, padx=(0, 8))
        
        # Content area
        content_frame = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search section
        search_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        search_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                             pady=(ModernTheme.PADDING_MEDIUM, ModernTheme.PADDING_SMALL))
        
        search_content = tk.Frame(search_container, bg=ModernTheme.WHITE)
        search_content.pack(fill=tk.X, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        search_label = tk.Label(search_content, text="🔍", font=("Segoe UI", 16),
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        search_label.pack(side=tk.LEFT)
        
        self.member_search_var = tk.StringVar()
        search_entry = tk.Entry(search_content, textvariable=self.member_search_var,
                               font=ModernTheme.FONT_PRIMARY, relief=tk.FLAT,
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900,
                               border=0)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
        search_entry.bind('<KeyRelease>', self._search_members)
        
        # Placeholder text
        search_entry.insert(0, "Tìm kiếm thành viên...")
        search_entry.config(fg=ModernTheme.GRAY_400)
        
        def on_focus_in(event):
            if search_entry.get() == "Tìm kiếm thành viên...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=ModernTheme.GRAY_900)
        
        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Tìm kiếm thành viên...")
                search_entry.config(fg=ModernTheme.GRAY_400)
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Table container
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=ModernTheme.PADDING_MEDIUM, 
                            pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Create modern treeview
        self._create_member_table(table_container)
        
        # Load members
        self._refresh_members()
    
    def _create_member_table(self, parent):
        """Tạo bảng thành viên hiện đại"""
        # Treeview with modern style
        columns = ('ID', 'Mã TV', 'Họ tên', 'Loại', 'Chức vụ', 'Phòng ban', 'Trạng thái')
        self.member_tree = ttk.Treeview(parent, columns=columns, show='headings', 
                                       style='Modern.Treeview', height=15)
        
        # Configure columns
        column_widths = {'ID': 60, 'Mã TV': 100, 'Họ tên': 200, 'Loại': 120, 
                        'Chức vụ': 150, 'Phòng ban': 150, 'Trạng thái': 100}
        
        for col in columns:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=column_widths.get(col, 100), anchor=tk.W)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.member_tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.member_tree.xview)
        self.member_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with padding
        self.member_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                             padx=ModernTheme.PADDING_LARGE, pady=ModernTheme.PADDING_LARGE)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=ModernTheme.PADDING_LARGE)
        
        # Row selection styling
        self.member_tree.tag_configure('selected', background=ModernTheme.PRIMARY_LIGHT)
    
    def _create_report_tab(self):
        """Tạo tab quản lý báo cáo"""
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="📋 Báo cáo")
        
        # Create modern layout for reports
        self._create_modern_report_layout(report_frame)
    
    def _create_modern_report_layout(self, parent):
        """Tạo layout hiện đại cho report tab"""
        # Header section
        header_frame = tk.Frame(parent, bg=ModernTheme.WHITE, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 1))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=ModernTheme.WHITE)
        header_content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(header_content, text="Quản lý Báo cáo", 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
        action_frame.pack(side=tk.RIGHT)
        
        # Primary button
        create_btn = tk.Button(action_frame, text="📝 Tạo báo cáo", 
                              font=ModernTheme.FONT_PRIMARY,
                              bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                              border=0, cursor="hand2", padx=16, pady=8,
                              command=self._add_report)
        create_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Secondary buttons
        for text, command in [("👁️ Xem/Sửa", self._edit_report), ("✅ Duyệt", self._approve_report)]:
            btn = tk.Button(action_frame, text=text, 
                           font=ModernTheme.FONT_PRIMARY,
                           bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                           border=0, cursor="hand2", padx=12, pady=8,
                           command=command)
            btn.pack(side=tk.RIGHT, padx=(0, 8))
        
        # Content area
        content_frame = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter and search section
        filter_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        filter_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                             pady=(ModernTheme.PADDING_MEDIUM, ModernTheme.PADDING_SMALL))
        
        filter_content = tk.Frame(filter_container, bg=ModernTheme.WHITE)
        filter_content.pack(fill=tk.X, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Filter by status
        filter_frame = tk.Frame(filter_content, bg=ModernTheme.WHITE)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        filter_label = tk.Label(filter_frame, text="Trạng thái:", 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
        filter_label.pack(side=tk.LEFT)
        
        self.report_status_var = tk.StringVar(value="Tất cả")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.report_status_var,
                                   values=["Tất cả", "Nháp", "Đã nộp", "Đã duyệt", "Từ chối"],
                                   state="readonly", width=15)
        status_combo.pack(side=tk.LEFT, padx=(8, 0))
        status_combo.bind('<<ComboboxSelected>>', self._filter_reports)
        
        # Table container
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=ModernTheme.PADDING_MEDIUM, 
                            pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Create modern report table
        self._create_report_table(table_container)
        
        # Load reports
        self._refresh_reports()
    
    def _create_report_table(self, parent):
        """Tạo bảng báo cáo hiện đại"""
        # Treeview with modern style
        columns = ('ID', 'Tiêu đề', 'Loại', 'Kỳ', 'Trạng thái', 'Ngày tạo')
        self.report_tree = ttk.Treeview(parent, columns=columns, show='headings', 
                                       style='Modern.Treeview', height=15)
        
        # Configure columns
        column_widths = {'ID': 60, 'Tiêu đề': 250, 'Loại': 120, 'Kỳ': 120, 
                        'Trạng thái': 120, 'Ngày tạo': 120}
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=column_widths.get(col, 100), anchor=tk.W)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.report_tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.report_tree.xview)
        self.report_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with padding
        self.report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                             padx=ModernTheme.PADDING_LARGE, pady=ModernTheme.PADDING_LARGE)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=ModernTheme.PADDING_LARGE)
        
        # Row selection styling
        self.report_tree.tag_configure('selected', background=ModernTheme.PRIMARY_LIGHT)
    
    def _create_task_tab(self):
        """Tạo tab quản lý công việc"""
        task_frame = ttk.Frame(self.notebook)
        self.notebook.add(task_frame, text="✅ Công việc")
        
        # Create modern layout for tasks
        self._create_modern_task_layout(task_frame)
    
    def _create_modern_task_layout(self, parent):
        """Tạo layout hiện đại cho task tab"""
        # Header section
        header_frame = tk.Frame(parent, bg=ModernTheme.WHITE, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 1))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=ModernTheme.WHITE)
        header_content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(header_content, text="Quản lý Công việc", 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
        action_frame.pack(side=tk.RIGHT)
        
        # Primary button
        create_btn = tk.Button(action_frame, text="➕ Tạo công việc", 
                              font=ModernTheme.FONT_PRIMARY,
                              bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                              border=0, cursor="hand2", padx=16, pady=8,
                              command=self._add_task)
        create_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # Secondary buttons
        for text, command in [("✏️ Cập nhật", self._edit_task), ("✅ Hoàn thành", self._complete_task)]:
            btn = tk.Button(action_frame, text=text, 
                           font=ModernTheme.FONT_PRIMARY,
                           bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                           border=0, cursor="hand2", padx=12, pady=8,
                           command=command)
            btn.pack(side=tk.RIGHT, padx=(0, 8))
        
        # Content area
        content_frame = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter section
        filter_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        filter_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                             pady=(ModernTheme.PADDING_MEDIUM, ModernTheme.PADDING_SMALL))
        
        filter_content = tk.Frame(filter_container, bg=ModernTheme.WHITE)
        filter_content.pack(fill=tk.X, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Filter controls
        filter_frame = tk.Frame(filter_content, bg=ModernTheme.WHITE)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Priority filter
        priority_label = tk.Label(filter_frame, text="Ưu tiên:", 
                                 font=ModernTheme.FONT_PRIMARY,
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
        priority_label.pack(side=tk.LEFT)
        
        self.task_priority_var = tk.StringVar(value="Tất cả")
        priority_combo = ttk.Combobox(filter_frame, textvariable=self.task_priority_var,
                                     values=["Tất cả", "Thấp", "Trung bình", "Cao", "Khẩn cấp"],
                                     state="readonly", width=12)
        priority_combo.pack(side=tk.LEFT, padx=(8, 16))
        priority_combo.bind('<<ComboboxSelected>>', self._filter_tasks)
        
        # Status filter
        status_label = tk.Label(filter_frame, text="Trạng thái:", 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
        status_label.pack(side=tk.LEFT)
        
        self.task_status_var = tk.StringVar(value="Tất cả")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.task_status_var,
                                   values=["Tất cả", "Chờ thực hiện", "Đang thực hiện", "Hoàn thành", "Tạm dừng"],
                                   state="readonly", width=15)
        status_combo.pack(side=tk.LEFT, padx=(8, 0))
        status_combo.bind('<<ComboboxSelected>>', self._filter_tasks)
        
        # Table container
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=ModernTheme.PADDING_MEDIUM, 
                            pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Create modern task table
        self._create_task_table(table_container)
        
        # Load tasks
        self._refresh_tasks()
    
    def _create_task_table(self, parent):
        """Tạo bảng công việc hiện đại"""
        # Treeview with modern style
        columns = ('ID', 'Tiêu đề', 'Ưu tiên', 'Trạng thái', 'Người thực hiện', 'Hạn hoàn thành', 'Tiến độ')
        self.task_tree = ttk.Treeview(parent, columns=columns, show='headings', 
                                     style='Modern.Treeview', height=15)
        
        # Configure columns
        column_widths = {'ID': 60, 'Tiêu đề': 200, 'Ưu tiên': 100, 'Trạng thái': 120, 
                        'Người thực hiện': 150, 'Hạn hoàn thành': 120, 'Tiến độ': 80}
        
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=column_widths.get(col, 100), anchor=tk.W)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.task_tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.task_tree.xview)
        self.task_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with padding
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                           padx=ModernTheme.PADDING_LARGE, pady=ModernTheme.PADDING_LARGE)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=ModernTheme.PADDING_LARGE)
        
        # Row selection styling
        self.task_tree.tag_configure('selected', background=ModernTheme.PRIMARY_LIGHT)
        self.task_tree.tag_configure('high_priority', background='#fff5f5', foreground='#dc2626')
        self.task_tree.tag_configure('overdue', background='#fef2f2', foreground='#991b1b')
    
    def _refresh_dashboard(self):
        """Làm mới thống kê dashboard"""
        try:
            # Member statistics
            member_stats = self.member_use_case.get_member_statistics()
            if hasattr(self, 'member_card'):
                self.member_card.number_label.config(text=str(member_stats['total']))
                self.member_card.subtitle_label.config(text=f"Đang hoạt động: {member_stats['active']}")
            
            # Report statistics
            report_stats = self.report_use_case.get_report_statistics()
            if hasattr(self, 'report_card'):
                self.report_card.number_label.config(text=str(report_stats['total']))
                self.report_card.subtitle_label.config(text=f"Chờ duyệt: {report_stats['submitted']}")
            
            # Task statistics
            task_stats = self.task_use_case.get_task_statistics()
            if hasattr(self, 'task_card'):
                self.task_card.number_label.config(text=str(task_stats['total']))
                self.task_card.subtitle_label.config(text=f"Hoàn thành: {task_stats['completed']}")
            
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
    
    def _filter_reports(self, event=None):
        """Lọc báo cáo theo trạng thái"""
        # TODO: Implement filter functionality
        pass
    
    def _filter_tasks(self, event=None):
        """Lọc công việc theo điều kiện"""
        # TODO: Implement filter functionality
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