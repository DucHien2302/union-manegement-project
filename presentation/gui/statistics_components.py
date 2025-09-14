"""
Statistics Window Component - Charts Only
Simple statistics charts display window for the dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Tuple, Optional
import threading
from datetime import datetime, timedelta
from presentation.gui.theme import ModernTheme
from presentation.gui.base_components import BaseCard
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class StatisticsWindow:
    """Statistics window showing only charts"""
    
    def __init__(self, parent, member_use_case=None, report_use_case=None, task_use_case=None):
        self.parent = parent
        self.member_use_case = member_use_case
        self.report_use_case = report_use_case
        self.task_use_case = task_use_case
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Biểu đồ thống kê")
        self.window.geometry("1200x800")
        self.window.configure(bg=ModernTheme.GRAY_50)
        
        # Center the window
        self._center_window()
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Initialize data
        self.stats_data = {}
        self.charts = {}
        
        # Create UI
        self._create_ui()
        
        # Load data
        self._load_statistics_data()
    
    def _center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_ui(self):
        """Create the main UI components"""
        # Header
        self._create_header()
        
        # Main content area - charts only
        self._create_charts_content()
        
        # Footer with actions
        self._create_footer()
    
    def _create_header(self):
        """Create window header"""
        header_frame = tk.Frame(self.window, bg=ModernTheme.WHITE, height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_container = tk.Frame(header_frame, bg=ModernTheme.WHITE)
        title_container.pack(expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(title_container, text="📊 Biểu đồ thống kê", 
                              font=("Segoe UI", 18, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(title_container, text=f"Dữ liệu tính đến {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                                 font=("Segoe UI", 11),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
        subtitle_label.pack()
    
    def _create_charts_content(self):
        """Create charts content"""
        if not MATPLOTLIB_AVAILABLE:
            # Show message if matplotlib not available
            message_frame = tk.Frame(self.window, bg=ModernTheme.GRAY_50)
            message_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            message_label = tk.Label(message_frame, 
                                   text="📊 Chức năng biểu đồ cần cài đặt thư viện matplotlib\n\nVui lòng chạy: pip install matplotlib",
                                   font=("Segoe UI", 12),
                                   bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_600,
                                   justify=tk.CENTER)
            message_label.pack(expand=True)
            
            self.charts_frame = message_frame
            return
        
        # Chart container
        chart_container = tk.Frame(self.window, bg=ModernTheme.GRAY_50)
        chart_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create chart sections
        self._create_chart_sections(chart_container)
        
        self.charts_frame = chart_container
    
    def _create_chart_sections(self, parent):
        """Create chart sections"""
        if not MATPLOTLIB_AVAILABLE:
            return
            
        # Charts container
        charts_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        charts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chart grid layout
        self.chart_frames = {}
        
        # Top row - Member and Report charts
        top_frame = tk.Frame(charts_container, bg=ModernTheme.GRAY_50)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Member chart
        member_chart_frame = tk.Frame(top_frame, bg=ModernTheme.WHITE, relief=tk.RAISED, bd=1)
        member_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.chart_frames['members'] = member_chart_frame
        
        # Report chart
        report_chart_frame = tk.Frame(top_frame, bg=ModernTheme.WHITE, relief=tk.RAISED, bd=1)
        report_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.chart_frames['reports'] = report_chart_frame
        
        # Bottom row - Task chart
        bottom_frame = tk.Frame(charts_container, bg=ModernTheme.GRAY_50)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        task_chart_frame = tk.Frame(bottom_frame, bg=ModernTheme.WHITE, relief=tk.RAISED, bd=1)
        task_chart_frame.pack(fill=tk.BOTH, expand=True)
        self.chart_frames['tasks'] = task_chart_frame
    
    def _create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.window, bg=ModernTheme.WHITE, height=60)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        # Button container
        button_container = tk.Frame(footer_frame, bg=ModernTheme.WHITE)
        button_container.pack(expand=True, fill=tk.BOTH)
        
        # Buttons
        refresh_btn = tk.Button(button_container, text="🔄 Làm mới", 
                               font=("Segoe UI", 10, "bold"),
                               bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                               relief=tk.FLAT, padx=20, pady=8,
                               command=self._refresh_data)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10), pady=15)
        
        close_btn = tk.Button(button_container, text="❌ Đóng", 
                             font=("Segoe UI", 10, "bold"),
                             bg=ModernTheme.GRAY_600, fg=ModernTheme.WHITE,
                             relief=tk.FLAT, padx=20, pady=8,
                             command=self.window.destroy)
        close_btn.pack(side=tk.RIGHT, pady=15)
    
    def _load_statistics_data(self):
        """Load all statistics data"""
        try:
            # Show loading message
            self._show_loading_message()
            
            # Load data in background thread
            thread = threading.Thread(target=self._load_data_async)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu thống kê: {e}")
    
    def _show_loading_message(self):
        """Show loading message"""
        loading_label = tk.Label(self.window, text="⏳ Đang tải dữ liệu thống kê...", 
                                font=("Segoe UI", 12),
                                bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_600)
        loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.loading_label = loading_label
    
    def _load_data_async(self):
        """Load data asynchronously"""
        try:
            stats_data = {}
            
            # Load member statistics
            if self.member_use_case:
                stats_data['members'] = self.member_use_case.get_member_statistics()
            
            # Load report statistics
            if self.report_use_case:
                stats_data['reports'] = self.report_use_case.get_report_statistics()
            
            # Load task statistics
            if self.task_use_case:
                stats_data['tasks'] = self.task_use_case.get_task_statistics()
            
            self.stats_data = stats_data
            
            # Update UI on main thread
            self.window.after(0, self._update_ui_with_data)
            
        except Exception as e:
            self.window.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}"))
    
    def _update_ui_with_data(self):
        """Update UI with loaded data"""
        try:
            # Hide loading message
            if hasattr(self, 'loading_label'):
                self.loading_label.destroy()
            
            # Update charts only
            if MATPLOTLIB_AVAILABLE:
                self._update_charts()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật giao diện: {e}")
    
    def _update_charts(self):
        """Update charts with loaded data"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        try:
            # Update member chart
            if 'members' in self.stats_data and 'members' in self.chart_frames:
                self._create_member_chart()
            
            # Update report chart
            if 'reports' in self.stats_data and 'reports' in self.chart_frames:
                self._create_report_chart()
            
            # Update task chart
            if 'tasks' in self.stats_data and 'tasks' in self.chart_frames:
                self._create_task_chart()
                
        except Exception as e:
            print(f"Error updating charts: {e}")
    
    def _create_member_chart(self):
        """Create member statistics chart"""
        frame = self.chart_frames['members']
        
        # Clear existing content
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Chart title
        title_label = tk.Label(frame, text="Thống kê thành viên", 
                              font=("Segoe UI", 12, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(pady=(10, 5))
        
        # Create figure
        fig = Figure(figsize=(5, 3), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Data
        member_stats = self.stats_data['members']
        labels = ['Đoàn viên', 'Hội viên', 'Cán bộ']
        sizes = [
            member_stats.get('union_members', 0),
            member_stats.get('association_members', 0),
            member_stats.get('executives', 0)
        ]
        colors = ['#3b82f6', '#10b981', '#f59e0b']  # Modern colors
        
        # Create pie chart
        if sum(sizes) > 0:
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        else:
            ax.text(0.5, 0.5, 'Chưa có dữ liệu', ha='center', va='center', transform=ax.transAxes)
        
        ax.set_title('Phân loại thành viên')
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def _create_report_chart(self):
        """Create report statistics chart"""
        frame = self.chart_frames['reports']
        
        # Clear existing content
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Chart title
        title_label = tk.Label(frame, text="Thống kê báo cáo", 
                              font=("Segoe UI", 12, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(pady=(10, 5))
        
        # Create figure
        fig = Figure(figsize=(5, 3), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Data
        report_stats = self.stats_data['reports']
        categories = ['Nháp', 'Chờ duyệt', 'Đã duyệt', 'Từ chối']
        values = [
            report_stats.get('draft', 0),
            report_stats.get('submitted', 0),
            report_stats.get('approved', 0),
            report_stats.get('rejected', 0)
        ]
        
        # Create bar chart
        bars = ax.bar(categories, values, color=['#94a3b8', '#f59e0b', '#10b981', '#ef4444'])
        ax.set_title('Trạng thái báo cáo')
        ax.set_ylabel('Số lượng')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            if value > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(value),
                       ha='center', va='bottom')
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def _create_task_chart(self):
        """Create task statistics chart"""
        frame = self.chart_frames['tasks']
        
        # Clear existing content
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Chart title
        title_label = tk.Label(frame, text="Thống kê công việc", 
                              font=("Segoe UI", 12, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(pady=(10, 5))
        
        # Create figure
        fig = Figure(figsize=(10, 3), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Data
        task_stats = self.stats_data['tasks']
        categories = ['Chưa bắt đầu', 'Đang thực hiện', 'Hoàn thành', 'Quá hạn']
        values = [
            task_stats.get('not_started', 0),
            task_stats.get('in_progress', 0),
            task_stats.get('completed', 0),
            task_stats.get('overdue', 0)
        ]
        
        # Create horizontal bar chart
        bars = ax.barh(categories, values, color=['#94a3b8', '#3b82f6', '#10b981', '#ef4444'])
        ax.set_title('Trạng thái công việc')
        ax.set_xlabel('Số lượng')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            if value > 0:
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, str(value),
                       ha='left', va='center')
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def _refresh_data(self):
        """Refresh all statistics data"""
        self._load_statistics_data()


def show_statistics_window(parent, member_use_case=None, report_use_case=None, task_use_case=None):
    """Show statistics window with charts only"""
    return StatisticsWindow(parent, member_use_case, report_use_case, task_use_case)