"""
Dashboard Components
Specialized components for the dashboard tab including statistics cards,
quick actions, and recent ac        content = tk.Frame(card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_MEDIUM, 
                    pady=ModernTheme.PADDING_SMALL)ities
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple, Optional, Dict, Any
from presentation.gui.theme import ModernTheme
from presentation.gui.base_components import BaseCard


class DashboardStatsCard:
    """Statistics card for dashboard"""
    
    @staticmethod
    def create_stats_card(parent, icon: str, title: str, color: str = ModernTheme.PRIMARY, 
                         tab_index: int = 0, notebook_ref=None) -> tk.Frame:
        """
        Create a statistics card for dashboard
        
        Args:
            parent: Parent widget
            icon: Icon emoji or text
            title: Card title
            color: Card accent color
            tab_index: Index for navigation
            notebook_ref: Reference to notebook widget
            
        Returns:
            Card frame with number_label and subtitle_label attributes
        """
        card = BaseCard.create_card(parent, cursor="hand2")
        
        # Card content
        content = tk.Frame(card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                    pady=ModernTheme.PADDING_LARGE)
        
        # Icon and title row
        header = tk.Frame(content, bg=ModernTheme.WHITE)
        header.pack(fill=tk.X)
        
        icon_label = tk.Label(header, text=icon, font=("Segoe UI", 20),
                             bg=ModernTheme.WHITE, fg=color)
        icon_label.pack(side=tk.LEFT)
        
        title_label = tk.Label(header, text=title, font=("Segoe UI", 12, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
        title_label.pack(side=tk.RIGHT)
        
        # Main number
        number_label = tk.Label(content, text="0", font=("Segoe UI", 28, "bold"),
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        number_label.pack(anchor=tk.W, pady=(ModernTheme.PADDING_SMALL, 0))
        
        # Subtitle
        subtitle_label = tk.Label(content, text="Tổng số", font=("Segoe UI", 9),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        subtitle_label.pack(anchor=tk.W)
        
        # Store references for updates
        setattr(card, 'number_label', number_label)
        setattr(card, 'subtitle_label', subtitle_label)
        
        # Click handler
        def on_click(event, index=tab_index):
            if notebook_ref:
                notebook_ref.select(index + 1)  # +1 because dashboard is at 0
        
        # Bind click events
        widgets = [card, content, header, icon_label, title_label, number_label, subtitle_label]
        for widget in widgets:
            widget.bind("<Button-1>", on_click)
        
        # Add hover effects
        BaseCard.add_card_hover_effects(card, [content, header, icon_label, title_label, number_label, subtitle_label])
        
        return card


class DashboardQuickActions:
    """Quick actions section for dashboard"""
    
    @staticmethod
    def create_quick_actions_section(parent, actions: List[Tuple[str, str, str, Callable]]) -> tk.Frame:
        """
        Create quick actions section
        
        Args:
            parent: Parent widget
            actions: List of (icon, title, subtitle, callback) tuples
            
        Returns:
            Actions container frame
        """
        actions_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        actions_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                              pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(actions_container, text="Thao tác nhanh", 
                              font=("Segoe UI", 14, "bold"),
                              bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Actions grid
        actions_frame = tk.Frame(actions_container, bg=ModernTheme.GRAY_50)
        actions_frame.pack(fill=tk.X)
        
        for i, (icon, title, subtitle, command) in enumerate(actions):
            action_card = DashboardQuickActions._create_action_card(
                actions_frame, icon, title, subtitle, command)
            action_card.grid(row=i//2, column=i%2, sticky="ew", 
                           padx=(0, ModernTheme.PADDING_SMALL) if i%2==0 else (ModernTheme.PADDING_SMALL, 0),
                           pady=ModernTheme.PADDING_SMALL)
            
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        return actions_container
    
    @staticmethod
    def _create_action_card(parent, icon: str, title: str, subtitle: str, command: Callable) -> tk.Frame:
        """Create an individual action card"""
        card = BaseCard.create_card(parent, cursor="hand2")
        
        # Card content
        content = tk.Frame(card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_MEDIUM, 
                    pady=ModernTheme.PADDING_MEDIUM)
        
        # Icon
        icon_label = tk.Label(content, text=icon, font=("Segoe UI", 16),
                             bg=ModernTheme.WHITE, fg=ModernTheme.PRIMARY)
        icon_label.pack(anchor=tk.W)
        
        # Title
        title_label = tk.Label(content, text=title, font=("Segoe UI", 11, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(4, 0))
        
        # Subtitle
        subtitle_label = tk.Label(content, text=subtitle, font=("Segoe UI", 9),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        subtitle_label.pack(anchor=tk.W)
        
        # Click handlers
        widgets = [card, content, icon_label, title_label, subtitle_label]
        for widget in widgets:
            widget.bind("<Button-1>", lambda e: command())
        
        # Add hover effects
        BaseCard.add_card_hover_effects(card, [content, icon_label, title_label, subtitle_label])
        
        return card


class DashboardRecentActivities:
    """Recent activities section for dashboard"""
    
    @staticmethod
    def create_recent_activities(parent, activities: List[Tuple[str, str, str]] = None) -> tk.Frame:
        """
        Create recent activities section
        
        Args:
            parent: Parent widget
            activities: List of (icon, activity_text, time_text) tuples
            
        Returns:
            Activities container frame
        """
        if activities is None:
            activities = [
                ("👤", "Thành viên mới được thêm", "2 phút trước"),
                ("📋", "Báo cáo tháng 9 được duyệt", "1 giờ trước"),
                ("✅", "Hoàn thành công việc tổ chức sự kiện", "3 giờ trước"),
            ]
        
        activities_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        activities_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                                 pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(activities_container, text="Hoạt động gần đây", 
                              font=("Segoe UI", 14, "bold"),
                              bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Activities card
        activities_card = BaseCard.create_card(activities_container)
        activities_card.pack(fill=tk.X)
        
        # Activities content
        content = tk.Frame(activities_card, bg=ModernTheme.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                    pady=ModernTheme.PADDING_LARGE)
        
        for icon, activity, time in activities:
            DashboardRecentActivities._create_activity_row(content, icon, activity, time)
        
        return activities_container
    
    @staticmethod
    def _create_activity_row(parent, icon: str, activity: str, time: str):
        """Create an individual activity row"""
        activity_row = tk.Frame(parent, bg=ModernTheme.WHITE)
        activity_row.pack(fill=tk.X, pady=4)
        
        icon_label = tk.Label(activity_row, text=icon, font=("Segoe UI", 12),
                             bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
        icon_label.pack(side=tk.LEFT, padx=(0, 12))
        
        text_frame = tk.Frame(activity_row, bg=ModernTheme.WHITE)
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        activity_label = tk.Label(text_frame, text=activity, font=("Segoe UI", 10),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900, anchor=tk.W)
        activity_label.pack(fill=tk.X)
        
        time_label = tk.Label(text_frame, text=time, font=("Segoe UI", 9),
                             bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500, anchor=tk.W)
        time_label.pack(fill=tk.X)


class DashboardTab:
    """Complete dashboard tab component"""
    
    @staticmethod
    def create_dashboard_tab(parent, notebook_ref=None, quick_action_callbacks: Dict[str, Callable] = None) -> tk.Frame:
        """
        Create complete dashboard tab
        
        Args:
            parent: Parent widget (usually notebook)
            notebook_ref: Reference to notebook for navigation
            quick_action_callbacks: Dict of callback functions
            
        Returns:
            Dashboard frame
        """
        dashboard_frame = ttk.Frame(parent)
        
        # Main container
        main_container = tk.Frame(dashboard_frame, bg=ModernTheme.GRAY_50)
        main_container.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_MEDIUM, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Welcome section
        DashboardTab._create_welcome_section(main_container)
        
        # Statistics cards
        stats_container = DashboardTab._create_stats_section(main_container, notebook_ref)
        
        # Quick actions
        if quick_action_callbacks:
            actions = [
                ("➕", "Thêm thành viên", "Tạo hồ sơ thành viên mới", 
                 quick_action_callbacks.get('add_member', lambda: None)),
                ("📝", "Tạo báo cáo", "Soạn báo cáo mới", 
                 quick_action_callbacks.get('create_report', lambda: None)),
                ("📋", "Giao việc", "Phân công công việc mới", 
                 quick_action_callbacks.get('create_task', lambda: None)),
                ("📊", "Xem thống kê", "Chi tiết thống kê và báo cáo", 
                 quick_action_callbacks.get('view_statistics', lambda: None)),
            ]
            DashboardQuickActions.create_quick_actions_section(main_container, actions)
        
        # Recent activities
        DashboardRecentActivities.create_recent_activities(main_container)
        
        return dashboard_frame, stats_container
    
    @staticmethod
    def _create_welcome_section(parent):
        """Create welcome section"""
        welcome_container = tk.Frame(parent, bg=ModernTheme.WHITE)
        welcome_container.pack(fill=tk.X, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        welcome_content = tk.Frame(welcome_container, bg=ModernTheme.WHITE)
        welcome_content.pack(fill=tk.X, padx=ModernTheme.PADDING_LARGE, 
                            pady=ModernTheme.PADDING_LARGE)
        
        # Welcome text
        welcome_label = tk.Label(welcome_content, text="Chào mừng bạn đến với hệ thống quản lý đoàn - hội", 
                                font=("Segoe UI", 16, "bold"),
                                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        welcome_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(welcome_content, text="Tổng quan và quản lý tất cả hoạt động của tổ chức", 
                                 font=("Segoe UI", 11),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
        subtitle_label.pack(anchor=tk.W, pady=(4, 0))
    
    @staticmethod
    def _create_stats_section(parent, notebook_ref=None) -> Dict[str, tk.Frame]:
        """Create statistics cards section"""
        stats_container = tk.Frame(parent, bg=ModernTheme.GRAY_50)
        stats_container.pack(fill=tk.X, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Title
        title_label = tk.Label(stats_container, text="Thống kê tổng quan", 
                              font=("Segoe UI", 14, "bold"),
                              bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900)
        title_label.pack(anchor=tk.W, pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Cards container
        cards_frame = tk.Frame(stats_container, bg=ModernTheme.GRAY_50)
        cards_frame.pack(fill=tk.X)
        
        # Create stats cards
        cards_data = [
            ("👥", "Thành viên", ModernTheme.PRIMARY, 0),
            ("📋", "Báo cáo", ModernTheme.SECONDARY, 1),
            ("✅", "Công việc", ModernTheme.ACCENT, 2),
        ]
        
        cards = {}
        for i, (icon, title, color, tab_index) in enumerate(cards_data):
            card = DashboardStatsCard.create_stats_card(
                cards_frame, icon, title, color, tab_index, notebook_ref)
            card.grid(row=0, column=i, sticky="ew", padx=ModernTheme.PADDING_SMALL)
            cards[title.lower() + '_card'] = card
        
        # Configure grid weights
        for i in range(len(cards_data)):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        return cards