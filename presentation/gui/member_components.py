"""
Member Management Components
Specialized components for member management including member table,
search functionality, and member forms with enhanced CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, List, Tuple, Optional, Dict, Any
import datetime
from presentation.gui.theme import ModernTheme
from presentation.gui.base_components import BaseHeader, BaseTable, BaseSearch


class MemberTable:
    """Enhanced member table component with modern styling and features"""
    
    @staticmethod
    def create_member_table(parent) -> Tuple[ttk.Treeview, tk.Frame]:
        """
        Create modern member table
        
        Args:
            parent: Parent widget
            
        Returns:
            Tuple of (treeview, container_frame)
        """
        columns = ('ID', 'Mã TV', 'Họ tên', 'Loại', 'Chức vụ', 'Phòng ban', 'Trạng thái')
        column_widths = {
            'ID': 60, 'Mã TV': 120, 'Họ tên': 220, 'Loại': 140, 
            'Chức vụ': 180, 'Phòng ban': 150, 'Trạng thái': 130
        }
        
        # Configure table style
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        tree, container = BaseTable.create_modern_table(parent, columns, column_widths)
        tree.configure(height=15)
        
        return tree, container
    
    @staticmethod
    def create_enhanced_member_table(parent) -> Tuple[ttk.Treeview, tk.Frame]:
        """
        Create enhanced member table with checkboxes and better styling
        
        Args:
            parent: Parent widget
            
        Returns:
            Tuple of (treeview, container_frame)
        """
        # Container frame
        container = tk.Frame(parent, bg=ModernTheme.WHITE)
        
        # Table frame with header
        table_frame = tk.Frame(container, bg=ModernTheme.WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Define columns with better structure
        columns = ('Select', 'ID', 'Mã TV', 'Họ tên', 'Ngày sinh', 'Giới tính', 
                  'Số ĐT', 'Chức vụ', 'Phòng ban', 'Loại', 'Trạng thái')
        
        # Create treeview với chiều cao lớn hơn và font size lớn hơn
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Configure column widths và headings - Tăng kích thước
        column_configs = {
            'Select': (50, '☐', tk.CENTER),
            'ID': (60, 'ID', tk.CENTER),
            'Mã TV': (120, 'Mã thành viên', tk.W),
            'Họ tên': (200, 'Họ và tên', tk.W),
            'Ngày sinh': (100, 'Ngày sinh', tk.CENTER),
            'Giới tính': (80, 'Giới tính', tk.CENTER),
            'Số ĐT': (130, 'Số điện thoại', tk.W),
            'Chức vụ': (150, 'Chức vụ', tk.W),
            'Phòng ban': (130, 'Phòng ban', tk.W),
            'Loại': (140, 'Loại thành viên', tk.W),
            'Trạng thái': (120, 'Trạng thái', tk.CENTER)
        }
        
        for col, (width, heading, anchor) in column_configs.items():
            tree.column(col, width=width, minwidth=width, anchor=anchor)
            tree.heading(col, text=heading, anchor=anchor)
        
        # Configure row styles
        tree.tag_configure('oddrow', background='#f8f9fa')
        tree.tag_configure('evenrow', background='white')
        tree.tag_configure('selected', background='#e3f2fd')
        tree.tag_configure('active', foreground='#2e7d32')
        tree.tag_configure('inactive', foreground='#f57c00')
        tree.tag_configure('suspended', foreground='#d32f2f')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and tree
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add selection tracking
        selected_items = set()
        
        def toggle_selection(event):
            """Toggle item selection"""
            item = tree.selection()[0] if tree.selection() else None
            if item:
                if item in selected_items:
                    selected_items.remove(item)
                    tree.set(item, 'Select', '☐')
                    tree.item(item, tags=('oddrow',) if tree.index(item) % 2 else ('evenrow',))
                else:
                    selected_items.add(item)
                    tree.set(item, 'Select', '☑')
                    tree.item(item, tags=('selected',))
        
        def select_all():
            """Select/deselect all items"""
            if len(selected_items) == len(tree.get_children()):
                # Deselect all
                selected_items.clear()
                for item in tree.get_children():
                    tree.set(item, 'Select', '☐')
                    tree.item(item, tags=('oddrow',) if tree.index(item) % 2 else ('evenrow',))
            else:
                # Select all
                selected_items.clear()
                for item in tree.get_children():
                    selected_items.add(item)
                    tree.set(item, 'Select', '☑')
                    tree.item(item, tags=('selected',))
        
        # Bind events
        tree.bind('<Button-1>', lambda e: tree.after(10, lambda: toggle_selection(e) if tree.identify_column(e.x) == '#1' else None))
        tree.heading('Select', command=select_all)
        
        # Store selection reference
        tree.selected_items = selected_items
        
        return tree, container


class MemberSearch:
    """Member search component"""
    
    @staticmethod
    def create_member_search(parent, search_callback: Callable = None) -> Tuple[tk.Entry, tk.StringVar]:
        """
        Create compact member search box
        
        Args:
            parent: Parent widget
            search_callback: Search callback function
            
        Returns:
            Tuple of (entry_widget, string_var)
        """
        # Create search variable
        search_var = tk.StringVar()
        
        # Create compact search entry
        search_entry = tk.Entry(parent, textvariable=search_var,
                               font=("Arial", 10),
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=1, width=40)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Placeholder text
        def on_focus_in(event):
            if search_var.get() == "Tìm kiếm thành viên...":
                search_var.set("")
                search_entry.config(fg=ModernTheme.GRAY_900)
        
        def on_focus_out(event):
            if not search_var.get():
                search_var.set("Tìm kiếm thành viên...")
                search_entry.config(fg=ModernTheme.GRAY_500)
        
        # Set initial placeholder
        search_var.set("Tìm kiếm thành viên...")
        search_entry.config(fg=ModernTheme.GRAY_500)
        
        # Bind events
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        
        if search_callback:
            search_entry.bind("<KeyRelease>", search_callback)
        
        return search_entry, search_var


class MemberTab:
    """Enhanced complete member management tab component with full CRUD functionality"""
    
    @staticmethod
    def create_member_tab(parent, callbacks: Dict[str, Callable] = None) -> Tuple[tk.Frame, ttk.Treeview, tk.StringVar, Dict]:
        """
        Create enhanced member management tab with all CRUD features
        
        Args:
            parent: Parent widget (usually notebook)
            callbacks: Dict of callback functions for actions
            
        Returns:
            Tuple of (member_frame, member_tree, search_var, filter_vars)
        """
        member_frame = ttk.Frame(parent)
        
        # Default callbacks
        default_callbacks = {
            'add_member': lambda: None,
            'edit_member': lambda: None,
            'delete_member': lambda: None,
            'view_member': lambda: None,
            'search_members': lambda e=None: None,
            'filter_members': lambda: None,
            'export_members': lambda: None,
            'bulk_action': lambda action: None,
            'refresh_data': lambda: None
        }
        if callbacks:
            default_callbacks.update(callbacks)
        
        # Header with enhanced actions
        actions = [
            ("👁️ Xem", default_callbacks['view_member']),
            ("✏️ Sửa", default_callbacks['edit_member']),
            ("🗑️ Xóa", default_callbacks['delete_member']),
            ("📊 Xuất Excel", default_callbacks['export_members']),
            ("🔄 Làm mới", default_callbacks['refresh_data']),
            ("➕ Thêm thành viên", default_callbacks['add_member'])
        ]
        BaseHeader.create_header(member_frame, "Quản lý Thành viên", actions)
        
        # Content area
        content_frame = tk.Frame(member_frame, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Advanced filters
        filter_vars = MemberFilters.create_filter_panel(content_frame, default_callbacks['filter_members'])
        
        # Search section - Thu nhỏ lại
        search_frame = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        search_container = tk.Frame(search_frame, bg=ModernTheme.WHITE)
        search_container.pack(fill=tk.X, padx=15, pady=5)
        
        # Tạo search box nhỏ gọn hơn
        search_label = tk.Label(search_container, text="🔍 Tìm kiếm:", 
                               font=("Arial", 10),
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry, search_var = MemberSearch.create_member_search(
            search_container, default_callbacks['search_members'])
        search_entry.configure(width=40)  # Giới hạn độ rộng
        
        # Bulk actions panel - Thu nhỏ lại
        bulk_frame = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        bulk_frame.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        bulk_container = tk.Frame(bulk_frame, bg=ModernTheme.WHITE)
        bulk_container.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(bulk_container, text="Thao tác hàng loạt:", 
                font=("Arial", 9, "bold"),
                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700).pack(side=tk.LEFT)
        
        bulk_actions = [
            ("Kích hoạt", lambda: default_callbacks['bulk_action']('activate')),
            ("Tạm ngưng", lambda: default_callbacks['bulk_action']('deactivate')),
            ("Xóa được chọn", lambda: default_callbacks['bulk_action']('delete'))
        ]
        
        for text, command in bulk_actions:
            btn = tk.Button(bulk_container, text=text, 
                           font=("Arial", 8),
                           bg=ModernTheme.GRAY_200, fg=ModernTheme.GRAY_700,
                           border=0, cursor="hand2", padx=10, pady=4,
                           command=command)
            btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Table container - Tăng kích thước
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=20, pady=(0, 10))
        
        # Create enhanced member table
        member_tree, tree_container = MemberTable.create_enhanced_member_table(table_container)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Context menu for table
        context_menu = tk.Menu(member_tree, tearoff=0)
        context_menu.add_command(label="👁️ Xem chi tiết", command=default_callbacks['view_member'])
        context_menu.add_command(label="✏️ Chỉnh sửa", command=default_callbacks['edit_member'])
        context_menu.add_separator()
        context_menu.add_command(label="🗑️ Xóa", command=default_callbacks['delete_member'])
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        member_tree.bind("<Button-3>", show_context_menu)  # Right click
        member_tree.bind("<Double-1>", lambda e: default_callbacks['view_member']())  # Double click
        
        # Status bar
        status_frame = tk.Frame(member_frame, bg=ModernTheme.GRAY_100, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        status_label = tk.Label(status_frame, text="Sẵn sàng", 
                               font=("Arial", 9),
                               bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_600,
                               anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Store references for external access
        member_frame.status_label = status_label
        
        return member_frame, member_tree, search_var, filter_vars


class MemberForm:
    """Enhanced member form component for add/edit operations"""
    
    @staticmethod
    def create_member_form_dialog(parent, title: str = "Thông tin thành viên", 
                                 member_data: Dict = None) -> Optional[Dict]:
        """
        Create enhanced member form dialog with validation
        
        Args:
            parent: Parent widget
            title: Dialog title
            member_data: Existing member data for editing
            
        Returns:
            Dict with form data or None if cancelled
        """
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("580x750")
        dialog.resizable(True, True)  # Allow resizing for better scrollbar functionality
        dialog.minsize(550, 600)  # Set minimum size
        dialog.grab_set()  # Make it modal
        
        # Center the dialog
        dialog.transient(parent)
        dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        result = {}
        
        # Enhanced main container with improved scrollbar
        main_canvas = tk.Canvas(dialog, bg=ModernTheme.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=ModernTheme.WHITE)
        
        # Configure scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel binding for better scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel to canvas and all child widgets
        def bind_to_mousewheel(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_to_mousewheel(child)
        
        dialog.bind("<MouseWheel>", _on_mousewheel)
        main_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Pack scrollbar and canvas
        main_canvas.pack(side="left", fill="both", expand=True, padx=(20, 5), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # Title
        title_frame = tk.Frame(scrollable_frame, bg=ModernTheme.WHITE)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text=title, 
                              font=("Arial", 16, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.PRIMARY)
        title_label.pack()
        
        # Form sections
        sections = [
            ("👤 Thông tin cơ bản", [
                ("Mã thành viên *:", "member_code", "entry", None),
                ("Họ và tên *:", "full_name", "entry", None),
                ("Ngày sinh:", "date_of_birth", "date", None),
                ("Giới tính:", "gender", "combo", ["Nam", "Nữ", "Khác"])
            ]),
            ("📞 Thông tin liên hệ", [
                ("Số điện thoại:", "phone", "entry", None),
                ("Email:", "email", "entry", None),
                ("Địa chỉ:", "address", "text", None)
            ]),
            ("🏢 Thông tin công việc", [
                ("Chức vụ:", "position", "entry", None),
                ("Phòng ban:", "department", "combo", ["Hành chính", "Kỹ thuật", "Tài chính", "Nhân sự", "Khác"]),
                ("Loại thành viên:", "member_type", "combo", ["Đoàn viên", "Hội viên", "Ban chấp hành"]),
                ("Trạng thái:", "status", "combo", ["Đang hoạt động", "Tạm ngưng", "Đình chỉ"])
            ]),
            ("📝 Thông tin bổ sung", [
                ("Ngày tham gia:", "join_date", "date", None),
                ("Ghi chú:", "notes", "text", None)
            ])
        ]
        
        variables = {}
        validation_functions = {}
        
        for section_title, fields in sections:
            # Section header
            section_frame = tk.LabelFrame(scrollable_frame, text=section_title, 
                                        font=("Arial", 11, "bold"),
                                        bg=ModernTheme.WHITE, fg=ModernTheme.PRIMARY,
                                        padx=15, pady=10)
            section_frame.pack(fill=tk.X, pady=(0, 15))
            
            for label_text, field_name, field_type, options in fields:
                # Field container
                field_frame = tk.Frame(section_frame, bg=ModernTheme.WHITE)
                field_frame.pack(fill=tk.X, pady=5)
                
                # Label
                label = tk.Label(field_frame, text=label_text, 
                                font=("Arial", 10),
                                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700,
                                anchor=tk.W)
                label.pack(fill=tk.X)
                
                # Input field based on type
                var = tk.StringVar()
                widget = None
                
                if field_type == "combo":
                    # Enhanced combo picker with visual indicators
                    if field_name == "gender":
                        # Enhanced gender picker with icons
                        values = ["👨 Nam", "👩 Nữ", "⚧️ Khác"]
                        gender_colors = {
                            "👨 Nam": ModernTheme.INFO,
                            "👩 Nữ": "#e91e63",
                            "⚧️ Khác": ModernTheme.ACCENT
                        }
                        color_mapping = gender_colors
                    elif field_name == "department":
                        # Enhanced department picker with icons
                        values = ["🏢 Hành chính", "🔧 Kỹ thuật", "💰 Tài chính", "👥 Nhân sự", "📋 Khác"]
                        dept_colors = {
                            "🏢 Hành chính": ModernTheme.PRIMARY,
                            "🔧 Kỹ thuật": ModernTheme.WARNING,
                            "💰 Tài chính": ModernTheme.SUCCESS,
                            "👥 Nhân sự": ModernTheme.INFO,
                            "📋 Khác": ModernTheme.GRAY_500
                        }
                        color_mapping = dept_colors
                    elif field_name == "member_type":
                        # Enhanced member type picker with icons
                        values = ["👤 Đoàn viên", "👥 Hội viên", "👔 Ban chấp hành"]
                        type_colors = {
                            "👤 Đoàn viên": ModernTheme.PRIMARY,
                            "👥 Hội viên": ModernTheme.SUCCESS,
                            "👔 Ban chấp hành": ModernTheme.ACCENT
                        }
                        color_mapping = type_colors
                    elif field_name == "status":
                        # Enhanced status picker with icons
                        values = ["✅ Đang hoạt động", "⏸️ Tạm ngưng", "❌ Đình chỉ"]
                        status_colors = {
                            "✅ Đang hoạt động": ModernTheme.SUCCESS,
                            "⏸️ Tạm ngưng": ModernTheme.WARNING,
                            "❌ Đình chỉ": ModernTheme.DANGER
                        }
                        color_mapping = status_colors
                    else:
                        values = options or []
                        color_mapping = {}
                    
                    # Create custom picker container
                    picker_container = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                    picker_container.pack(fill=tk.X, pady=(4, 0))
                    
                    # Enhanced combobox with better styling
                    combo_style = ttk.Style()
                    combo_style.configure("Member.TCombobox",
                                         fieldbackground=ModernTheme.GRAY_50,
                                         background=ModernTheme.WHITE,
                                         borderwidth=1,
                                         relief="solid")
                    
                    widget = ttk.Combobox(picker_container, textvariable=var, values=values, 
                                        state="readonly", font=("Arial", 10),
                                        style="Member.TCombobox", height=6)
                    widget.pack(fill=tk.X, ipady=8)
                    
                    # Color indicator frame if colors available
                    if color_mapping:
                        indicator_frame = tk.Frame(picker_container, bg=ModernTheme.WHITE, height=4)
                        indicator_frame.pack(fill=tk.X, pady=(2, 0))
                        
                        color_indicator = tk.Frame(indicator_frame, height=3, bg=ModernTheme.GRAY_200)
                        color_indicator.pack(fill=tk.X)
                        
                        # Update color indicator when selection changes
                        def update_color_indicator(event=None):
                            selected_value = var.get()
                            if selected_value in color_mapping:
                                color_indicator.configure(bg=color_mapping[selected_value])
                            else:
                                color_indicator.configure(bg=ModernTheme.GRAY_200)
                        
                        widget.bind('<<ComboboxSelected>>', update_color_indicator)
                        var.trace('w', lambda *args: update_color_indicator())
                    
                    # Add field-specific hints
                    if field_name == "member_type":
                        hint_label = tk.Label(picker_container, text="💡 Chọn loại thành viên phù hợp", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(anchor=tk.W, pady=(2, 0))
                    elif field_name == "department":
                        hint_label = tk.Label(picker_container, text="💡 Phòng ban hoặc bộ phận công tác", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(anchor=tk.W, pady=(2, 0))
                    
                elif field_type == "text":
                    # Enhanced text area with better styling
                    text_container = tk.Frame(field_frame, bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                    text_container.pack(fill=tk.X, pady=(4, 0))
                    
                    # Text widget with scrollbar
                    text_frame = tk.Frame(text_container, bg=ModernTheme.GRAY_50)
                    text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                    
                    widget = tk.Text(text_frame, height=3, 
                                   font=("Arial", 10),
                                   bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                   relief=tk.FLAT, bd=0, wrap=tk.WORD,
                                   selectbackground=ModernTheme.PRIMARY,
                                   selectforeground=ModernTheme.WHITE)
                    
                    # Add scrollbar for text areas
                    scrollbar_text = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=widget.yview)
                    widget.configure(yscrollcommand=scrollbar_text.set)
                    
                    widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
                    
                    # Focus effects for text area
                    def on_text_focus_in(event):
                        text_container.configure(bg=ModernTheme.PRIMARY, relief=tk.SOLID, bd=1)
                        
                    def on_text_focus_out(event):
                        text_container.configure(bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                    
                    widget.bind('<FocusIn>', on_text_focus_in)
                    widget.bind('<FocusOut>', on_text_focus_out)
                    
                    # Add character counter for address and notes
                    if field_name in ["address", "notes"]:
                        count_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                        count_frame.pack(fill=tk.X, pady=(2, 0))
                        
                        char_count_label = tk.Label(count_frame, text="0 ký tự", 
                                                  font=('Arial', 8), 
                                                  bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        char_count_label.pack(side=tk.RIGHT)
                        
                        def update_char_count(*args):
                            content = widget.get("1.0", tk.END).strip()
                            char_count = len(content)
                            char_count_label.configure(text=f"{char_count} ký tự")
                        
                        # Bind to text changes
                        def on_text_change(event):
                            widget.after_idle(update_char_count)
                        
                        widget.bind('<KeyRelease>', on_text_change)
                        widget.bind('<Button-1>', on_text_change)
                        widget.bind('<Control-v>', on_text_change)  # Paste
                        
                        # Add field-specific hints
                        if field_name == "address":
                            hint_label = tk.Label(count_frame, text="💡 Địa chỉ liên hệ chi tiết", 
                                                font=('Arial', 8), 
                                                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                            hint_label.pack(side=tk.LEFT)
                        elif field_name == "notes":
                            hint_label = tk.Label(count_frame, text="💡 Ghi chú thêm về thành viên", 
                                                font=('Arial', 8), 
                                                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                            hint_label.pack(side=tk.LEFT)
                    
                elif field_type == "date":
                    # Enhanced date picker field
                    date_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                    date_frame.pack(fill=tk.X, pady=(4, 0))
                    
                    # Date input container with border
                    input_container = tk.Frame(date_frame, bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                    input_container.pack(fill=tk.X)
                    
                    widget = tk.Entry(input_container, textvariable=var, 
                                    font=("Arial", 10),
                                    bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                    relief=tk.FLAT, bd=0, width=12)
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)
                    
                    # Enhanced date picker function
                    def create_date_picker(entry_var):
                        def show_picker():
                            from tkinter import simpledialog
                            import datetime
                            
                            # Enhanced date input dialog
                            current_date = datetime.datetime.now().strftime('%d/%m/%Y')
                            initial_value = entry_var.get() if entry_var.get() else current_date
                            
                            date_str = simpledialog.askstring(
                                "📅 Chọn ngày", 
                                f"Nhập ngày (DD/MM/YYYY):\n\nVí dụ: {current_date}",
                                initialvalue=initial_value
                            )
                            if date_str:
                                # Validate date format
                                try:
                                    parsed_date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
                                    entry_var.set(date_str)
                                except ValueError:
                                    from tkinter import messagebox
                                    messagebox.showerror("❌ Lỗi", 
                                                       "Định dạng ngày không đúng!\n\nVui lòng sử dụng định dạng: DD/MM/YYYY\nVí dụ: 25/12/1990")
                        return show_picker
                    
                    # Styled date picker button
                    date_btn = tk.Button(input_container, text="📅", 
                                       font=('Arial', 12),
                                       bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                                       border=0, cursor="hand2", padx=12, pady=8,
                                       command=create_date_picker(var))
                    date_btn.pack(side=tk.RIGHT)
                    
                    # Enhanced help and quick date buttons
                    help_frame = tk.Frame(date_frame, bg=ModernTheme.WHITE)
                    help_frame.pack(fill=tk.X, pady=(4, 0))
                    
                    help_label = tk.Label(help_frame, text="💡 Định dạng: DD/MM/YYYY", 
                                        font=('Arial', 8), 
                                        bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500,
                                        anchor=tk.W)
                    help_label.pack(side=tk.LEFT)
                    
                    # Quick date buttons for common selections (especially for join_date)
                    if field_name == "join_date":
                        quick_dates_frame = tk.Frame(help_frame, bg=ModernTheme.WHITE)
                        quick_dates_frame.pack(side=tk.RIGHT)
                        
                        def set_current_date():
                            import datetime
                            today = datetime.datetime.now()
                            var.set(today.strftime('%d/%m/%Y'))
                        
                        today_btn = tk.Button(quick_dates_frame, text="Hôm nay",
                                            font=('Arial', 8),
                                            bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                                            border=0, cursor="hand2", padx=8, pady=2,
                                            command=set_current_date)
                        today_btn.pack(side=tk.LEFT, padx=(2, 0))
                    
                else:  # entry
                    # Enhanced entry field with better styling
                    entry_container = tk.Frame(field_frame, bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                    entry_container.pack(fill=tk.X, pady=(4, 0))
                    
                    widget = tk.Entry(entry_container, textvariable=var, 
                                    font=("Arial", 10),
                                    bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                    relief=tk.FLAT, bd=0)
                    widget.pack(fill=tk.X, padx=10, pady=8)
                    
                    # Add placeholder text and focus effects
                    def on_focus_in(event):
                        entry_container.configure(bg=ModernTheme.PRIMARY, relief=tk.SOLID, bd=1)
                        
                    def on_focus_out(event):
                        entry_container.configure(bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                    
                    widget.bind('<FocusIn>', on_focus_in)
                    widget.bind('<FocusOut>', on_focus_out)
                    
                    # Add field-specific hints and validation
                    hint_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                    hint_frame.pack(fill=tk.X, pady=(2, 0))
                    
                    if field_name == "member_code":
                        hint_label = tk.Label(hint_frame, text="💡 Mã thành viên duy nhất (ví dụ: TV2024001)", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(side=tk.LEFT)
                        
                        # Auto-generate button
                        def auto_generate_code():
                            import datetime
                            now = datetime.datetime.now()
                            year = now.year
                            # Simple auto-generation (in real app, you'd check existing codes)
                            code = f"TV{year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}"
                            var.set(code)
                        
                        auto_btn = tk.Button(hint_frame, text="🎲 Tự động tạo",
                                           font=('Arial', 8),
                                           bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                                           border=0, cursor="hand2", padx=6, pady=2,
                                           command=auto_generate_code)
                        auto_btn.pack(side=tk.RIGHT)
                        
                    elif field_name == "full_name":
                        hint_label = tk.Label(hint_frame, text="💡 Họ và tên đầy đủ của thành viên", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(side=tk.LEFT)
                        
                    elif field_name == "phone":
                        hint_label = tk.Label(hint_frame, text="💡 Số điện thoại liên hệ (ví dụ: 0901234567)", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(side=tk.LEFT)
                        
                        # Phone validation indicator
                        def validate_phone(*args):
                            phone_value = var.get().strip()
                            if phone_value:
                                clean_phone = phone_value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
                                if clean_phone.isdigit() and len(clean_phone) >= 10:
                                    hint_label.configure(text="✅ Số điện thoại hợp lệ", fg=ModernTheme.SUCCESS)
                                else:
                                    hint_label.configure(text="❌ Số điện thoại không hợp lệ", fg=ModernTheme.DANGER)
                            else:
                                hint_label.configure(text="💡 Số điện thoại liên hệ (ví dụ: 0901234567)", fg=ModernTheme.GRAY_500)
                        
                        var.trace('w', validate_phone)
                        
                    elif field_name == "email":
                        hint_label = tk.Label(hint_frame, text="💡 Địa chỉ email (ví dụ: email@example.com)", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(side=tk.LEFT)
                        
                        # Email validation indicator
                        def validate_email(*args):
                            email_value = var.get().strip()
                            if email_value:
                                if '@' in email_value and '.' in email_value.split('@')[1]:
                                    hint_label.configure(text="✅ Email hợp lệ", fg=ModernTheme.SUCCESS)
                                else:
                                    hint_label.configure(text="❌ Email không hợp lệ", fg=ModernTheme.DANGER)
                            else:
                                hint_label.configure(text="💡 Địa chỉ email (ví dụ: email@example.com)", fg=ModernTheme.GRAY_500)
                        
                        var.trace('w', validate_email)
                        
                    elif field_name == "position":
                        hint_label = tk.Label(hint_frame, text="💡 Chức vụ hiện tại của thành viên", 
                                            font=('Arial', 8), 
                                            bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                        hint_label.pack(side=tk.LEFT)
                
                # Set existing values
                if member_data and field_name in member_data:
                    value = member_data[field_name]
                    if field_type == "text" and widget:
                        widget.insert(tk.END, str(value) if value else "")
                    elif field_type == "date" and value:
                        if isinstance(value, datetime.datetime):
                            var.set(value.strftime('%d/%m/%Y'))
                        else:
                            var.set(str(value))
                    elif field_type == "combo":
                        # Map plain text to emoji versions for display
                        value_mapping = {}
                        if field_name == "gender":
                            value_mapping = {
                                "Nam": "👨 Nam", "male": "👨 Nam",
                                "Nữ": "👩 Nữ", "female": "👩 Nữ", 
                                "Khác": "⚧️ Khác", "other": "⚧️ Khác"
                            }
                        elif field_name == "department":
                            value_mapping = {
                                "Hành chính": "🏢 Hành chính", "admin": "🏢 Hành chính",
                                "Kỹ thuật": "🔧 Kỹ thuật", "technical": "🔧 Kỹ thuật",
                                "Tài chính": "💰 Tài chính", "finance": "💰 Tài chính",
                                "Nhân sự": "👥 Nhân sự", "hr": "👥 Nhân sự",
                                "Khác": "📋 Khác", "other": "📋 Khác"
                            }
                        elif field_name == "member_type":
                            value_mapping = {
                                "Đoàn viên": "👤 Đoàn viên", "union_member": "👤 Đoàn viên",
                                "Hội viên": "👥 Hội viên", "association_member": "👥 Hội viên",
                                "Ban chấp hành": "👔 Ban chấp hành", "executive": "👔 Ban chấp hành"
                            }
                        elif field_name == "status":
                            value_mapping = {
                                "Đang hoạt động": "✅ Đang hoạt động", "active": "✅ Đang hoạt động",
                                "Tạm ngưng": "⏸️ Tạm ngưng", "inactive": "⏸️ Tạm ngưng",
                                "Đình chỉ": "❌ Đình chỉ", "suspended": "❌ Đình chỉ"
                            }
                        
                        # Find matching display value
                        display_value = value_mapping.get(str(value), str(value))
                        if hasattr(widget, 'set'):
                            widget.set(display_value)
                        var.set(display_value)
                        
                        # Update color indicator if available
                        if 'update_color_indicator' in locals():
                            update_color_indicator()
                    else:
                        var.set(str(value) if value else "")
                
                variables[field_name] = (var, widget, field_type)
                
                # Add validation for required fields
                if "*" in label_text:
                    def create_validator(field):
                        def validator():
                            value = variables[field][0].get().strip()
                            return bool(value)
                        return validator
                    validation_functions[field_name] = create_validator(field_name)
        
        # Validation error label
        error_label = tk.Label(scrollable_frame, text="", 
                             font=("Arial", 10),
                             bg=ModernTheme.WHITE, fg=ModernTheme.ERROR,
                             wraplength=450)
        error_label.pack(pady=(10, 0))
        
        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg=ModernTheme.WHITE)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Enhanced validation function
        def validate_form():
            errors = []
            
            # Required field validation
            for field_name, validator in validation_functions.items():
                if not validator():
                    field_label = {
                        'member_code': 'Mã thành viên',
                        'full_name': 'Họ và tên'
                    }.get(field_name, field_name)
                    errors.append(f"❌ {field_label} không được để trống")
            
            # Enhanced email validation
            email_value = variables.get('email', [tk.StringVar()])[0].get().strip()
            if email_value:
                if '@' not in email_value or '.' not in email_value.split('@')[1]:
                    errors.append("❌ Email không hợp lệ - phải có dạng email@domain.com")
            
            # Enhanced phone validation
            phone_value = variables.get('phone', [tk.StringVar()])[0].get().strip()
            if phone_value:
                clean_phone = phone_value.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
                if not clean_phone.isdigit():
                    errors.append("❌ Số điện thoại chỉ được chứa số")
                elif len(clean_phone) < 10:
                    errors.append("❌ Số điện thoại phải có ít nhất 10 chữ số")
            
            # Date validation
            for field_name in ['date_of_birth', 'join_date']:
                if field_name in variables:
                    date_value = variables[field_name][0].get().strip()
                    if date_value:
                        try:
                            parsed_date = datetime.datetime.strptime(date_value, '%d/%m/%Y')
                            # Check reasonable date ranges
                            if field_name == 'date_of_birth':
                                current_year = datetime.datetime.now().year
                                birth_year = parsed_date.year
                                if birth_year < 1920 or birth_year > current_year - 16:
                                    errors.append("❌ Ngày sinh không hợp lý (từ 1920 đến hiện tại - 16 tuổi)")
                            elif field_name == 'join_date':
                                if parsed_date > datetime.datetime.now():
                                    errors.append("❌ Ngày tham gia không thể là tương lai")
                        except ValueError:
                            field_display = "Ngày sinh" if field_name == 'date_of_birth' else "Ngày tham gia"
                            errors.append(f"❌ {field_display} không đúng định dạng DD/MM/YYYY")
            
            # Member code uniqueness (basic check - you might want to check against database)
            member_code = variables.get('member_code', [tk.StringVar()])[0].get().strip()
            if member_code and len(member_code) < 5:
                errors.append("❌ Mã thành viên phải có ít nhất 5 ký tự")
            
            return errors
        
        # Enhanced save function
        def on_save():
            # Validate form
            errors = validate_form()
            if errors:
                error_label.config(text="\n".join(errors))
                return
            
            error_label.config(text="")
            
            # Collect form data
            for field_name, (var, widget, field_type) in variables.items():
                if field_type == "text" and widget:
                    result[field_name] = widget.get("1.0", tk.END).strip()
                else:
                    value = var.get().strip()
                    
                    # Convert emoji values back to plain text for database storage
                    if field_type == "combo":
                        reverse_mapping = {}
                        if field_name == "gender":
                            reverse_mapping = {
                                "👨 Nam": "Nam",
                                "👩 Nữ": "Nữ",
                                "⚧️ Khác": "Khác"
                            }
                        elif field_name == "department":
                            reverse_mapping = {
                                "🏢 Hành chính": "Hành chính",
                                "🔧 Kỹ thuật": "Kỹ thuật",
                                "💰 Tài chính": "Tài chính",
                                "👥 Nhân sự": "Nhân sự",
                                "📋 Khác": "Khác"
                            }
                        elif field_name == "member_type":
                            reverse_mapping = {
                                "👤 Đoàn viên": "Đoàn viên",
                                "👥 Hội viên": "Hội viên",
                                "👔 Ban chấp hành": "Ban chấp hành"
                            }
                        elif field_name == "status":
                            reverse_mapping = {
                                "✅ Đang hoạt động": "Đang hoạt động",
                                "⏸️ Tạm ngưng": "Tạm ngưng",
                                "❌ Đình chỉ": "Đình chỉ"
                            }
                        
                        result[field_name] = reverse_mapping.get(value, value)
                    
                    # Convert date strings
                    elif field_type == "date" and value:
                        try:
                            result[field_name] = datetime.datetime.strptime(value, '%d/%m/%Y')
                        except ValueError:
                            result[field_name] = value
                    else:
                        result[field_name] = value
            
            dialog.destroy()
        
        def on_cancel():
            result.clear()
            dialog.destroy()
        
        # Enhanced button styling
        cancel_btn = tk.Button(button_frame, text="❌ Hủy bỏ", 
                              font=("Arial", 10),
                              bg=ModernTheme.GRAY_200, fg=ModernTheme.GRAY_700,
                              border=0, cursor="hand2", padx=25, pady=12,
                              command=on_cancel)
        cancel_btn.pack(side=tk.RIGHT)
        
        save_btn = tk.Button(button_frame, text="💾 Lưu thành viên", 
                            font=("Arial", 10),
                            bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                            border=0, cursor="hand2", padx=25, pady=12,
                            command=on_save)
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Button hover effects
        def on_save_hover_enter(event):
            save_btn.configure(bg=ModernTheme.PRIMARY_DARK)
        
        def on_save_hover_leave(event):
            save_btn.configure(bg=ModernTheme.PRIMARY)
            
        def on_cancel_hover_enter(event):
            cancel_btn.configure(bg=ModernTheme.GRAY_300)
        
        def on_cancel_hover_leave(event):
            cancel_btn.configure(bg=ModernTheme.GRAY_200)
        
        save_btn.bind('<Enter>', on_save_hover_enter)
        save_btn.bind('<Leave>', on_save_hover_leave)
        cancel_btn.bind('<Enter>', on_cancel_hover_enter)
        cancel_btn.bind('<Leave>', on_cancel_hover_leave)
        
        # Bind Enter key to save
        dialog.bind('<Return>', lambda e: on_save())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        # Focus on first field and update scrollregion
        if variables:
            first_field = list(variables.values())[0]
            if first_field[1] and hasattr(first_field[1], 'focus'):
                first_field[1].focus()
        
        # Update scrollbar after dialog is fully rendered
        def update_scroll_region():
            dialog.update_idletasks()
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            # Ensure scrollbar is visible if needed
            bbox = main_canvas.bbox("all")
            if bbox and bbox[3] > main_canvas.winfo_height():
                scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        dialog.after(100, update_scroll_region)
        
        # Bind mousewheel to scrollable frame after it's created
        dialog.after(50, lambda: bind_to_mousewheel(scrollable_frame))
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result if result else None


class MemberActions:
    """Enhanced member action handlers and utilities"""
    
    @staticmethod
    def populate_member_tree(tree: ttk.Treeview, members: List[Any], enhanced_mode: bool = False):
        """
        Populate member tree with data
        
        Args:
            tree: Treeview widget
            members: List of member objects
            enhanced_mode: Whether using enhanced table format
        """
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Clear selection if enhanced mode
        if enhanced_mode and hasattr(tree, 'selected_items'):
            tree.selected_items.clear()
        
        # Mapping for user-friendly display
        member_type_display = {
            'union_member': '👤 Đoàn viên',
            'association_member': '👥 Hội viên', 
            'executive': '👔 Ban chấp hành'
        }
        
        status_display = {
            'active': '✅ Hoạt động',
            'inactive': '⏸️ Tạm ngưng',
            'suspended': '❌ Đình chỉ'
        }
        
        # Add members
        if not members:
            # Show empty state
            if enhanced_mode:
                tree.insert('', 'end', values=('☐', '', '', '🔍 Không có thành viên nào', '', '', '', '', '', '', ''))
            else:
                tree.insert('', 'end', values=('', '', '🔍 Không có thành viên nào', '', '', '', ''))
            return
        
        for i, member in enumerate(members):
            member_type_str = member.member_type.value if hasattr(member.member_type, 'value') else str(member.member_type)
            status_str = member.status.value if hasattr(member.status, 'value') else str(member.status)
            
            # Convert to user-friendly display
            member_type_display_str = member_type_display.get(member_type_str, member_type_str)
            status_display_str = status_display.get(status_str, status_str)
            
            # Format date of birth
            birth_date_str = ""
            if hasattr(member, 'date_of_birth') and member.date_of_birth:
                try:
                    if isinstance(member.date_of_birth, datetime.datetime):
                        birth_date_str = member.date_of_birth.strftime('%d/%m/%Y')
                    else:
                        birth_date_str = str(member.date_of_birth)
                except:
                    birth_date_str = ""
            
            # Determine row tags based on status
            tags = []
            if enhanced_mode:
                tags.append('oddrow' if i % 2 else 'evenrow')
                if status_str == 'active':
                    tags.append('active')
                elif status_str == 'inactive':
                    tags.append('inactive')
                elif status_str == 'suspended':
                    tags.append('suspended')
            
            if enhanced_mode:
                values = (
                    '☐',  # Select checkbox
                    getattr(member, 'id', ''),
                    getattr(member, 'member_code', ''),
                    getattr(member, 'full_name', ''),
                    birth_date_str,
                    getattr(member, 'gender', ''),
                    getattr(member, 'phone', ''),
                    getattr(member, 'position', ''),
                    getattr(member, 'department', ''),
                    member_type_display_str,
                    status_display_str
                )
            else:
                values = (
                    getattr(member, 'id', ''),
                    getattr(member, 'member_code', ''),
                    getattr(member, 'full_name', ''),
                    member_type_display_str,
                    getattr(member, 'position', ''),
                    getattr(member, 'department', ''),
                    status_display_str
                )
            
            item = tree.insert('', 'end', values=values, tags=tags)
    
    @staticmethod
    def get_selected_member_id(tree: ttk.Treeview, enhanced_mode: bool = False) -> Optional[int]:
        """
        Get selected member ID from tree
        
        Args:
            tree: Treeview widget
            enhanced_mode: Whether using enhanced table format
            
        Returns:
            Member ID or None if no selection
        """
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            id_index = 1 if enhanced_mode else 0  # Account for checkbox column
            try:
                member_id = item['values'][id_index]
                return int(member_id) if member_id else None
            except (ValueError, IndexError):
                return None
        return None
    
    @staticmethod
    def get_selected_member_ids(tree: ttk.Treeview, enhanced_mode: bool = False) -> List[int]:
        """
        Get all selected member IDs from enhanced tree
        
        Args:
            tree: Treeview widget
            enhanced_mode: Whether using enhanced table format
            
        Returns:
            List of member IDs
        """
        member_ids = []
        
        if enhanced_mode and hasattr(tree, 'selected_items'):
            # Get from checkbox selections
            for item in tree.selected_items:
                try:
                    values = tree.item(item)['values']
                    member_id = values[1]  # ID is in column 1 (after checkbox)
                    if member_id:
                        member_ids.append(int(member_id))
                except (ValueError, IndexError):
                    continue
        else:
            # Get from tree selection
            for item in tree.selection():
                try:
                    values = tree.item(item)['values']
                    member_id = values[0]  # ID is in column 0
                    if member_id:
                        member_ids.append(int(member_id))
                except (ValueError, IndexError):
                    continue
        
        return member_ids
    
    @staticmethod
    def search_members(tree: ttk.Treeview, search_term: str, all_members: List[Any], enhanced_mode: bool = False):
        """
        Filter members in tree based on search term
        
        Args:
            tree: Treeview widget
            search_term: Search string
            all_members: Complete list of members
            enhanced_mode: Whether using enhanced table format
        """
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        
        # If no search term, show all
        if not search_term or search_term == "Tìm kiếm thành viên...":
            MemberActions.populate_member_tree(tree, all_members, enhanced_mode)
            return
        
        # Filter members
        filtered_members = []
        search_lower = search_term.lower()
        
        for member in all_members:
            # Search in multiple fields
            search_fields = [
                getattr(member, 'full_name', ''),
                getattr(member, 'member_code', ''),
                getattr(member, 'position', ''),
                getattr(member, 'department', ''),
                getattr(member, 'phone', ''),
                getattr(member, 'email', '')
            ]
            
            if any(search_lower in str(field).lower() for field in search_fields):
                filtered_members.append(member)
        
        # Populate with filtered results
        MemberActions.populate_member_tree(tree, filtered_members, enhanced_mode)
    
    @staticmethod
    def apply_filters(tree: ttk.Treeview, all_members: List[Any], filters: Dict[str, tk.StringVar], enhanced_mode: bool = False):
        """
        Apply advanced filters to member list
        
        Args:
            tree: Treeview widget
            all_members: Complete list of members
            filters: Filter variables dictionary
            enhanced_mode: Whether using enhanced table format
        """
        filtered_members = all_members.copy()
        
        # Apply department filter
        dept_filter = filters.get('department', tk.StringVar()).get()
        if dept_filter and dept_filter != "Tất cả":
            filtered_members = [m for m in filtered_members 
                              if getattr(m, 'department', '').lower() == dept_filter.lower()]
        
        # Apply member type filter
        type_filter = filters.get('member_type', tk.StringVar()).get()
        if type_filter and type_filter != "Tất cả":
            type_mapping = {
                "Đoàn viên": "union_member",
                "Hội viên": "association_member", 
                "Ban chấp hành": "executive"
            }
            target_type = type_mapping.get(type_filter)
            if target_type:
                filtered_members = [m for m in filtered_members 
                                  if getattr(m, 'member_type', '').value == target_type]
        
        # Apply status filter
        status_filter = filters.get('status', tk.StringVar()).get()
        if status_filter and status_filter != "Tất cả":
            status_mapping = {
                "Đang hoạt động": "active",
                "Tạm ngưng": "inactive",
                "Đình chỉ": "suspended"
            }
            target_status = status_mapping.get(status_filter)
            if target_status:
                filtered_members = [m for m in filtered_members 
                                  if getattr(m, 'status', '').value == target_status]
        
        # Populate tree with filtered data
        MemberActions.populate_member_tree(tree, filtered_members, enhanced_mode)
    
    @staticmethod
    def get_member_dict_from_tree_item(tree: ttk.Treeview, item_id: str, enhanced_mode: bool = False) -> Dict:
        """
        Convert tree item to member data dictionary
        
        Args:
            tree: Treeview widget
            item_id: Tree item ID
            enhanced_mode: Whether using enhanced table format
            
        Returns:
            Member data dictionary
        """
        values = tree.item(item_id)['values']
        
        if enhanced_mode:
            return {
                'id': values[1],
                'member_code': values[2], 
                'full_name': values[3],
                'date_of_birth': values[4],
                'gender': values[5],
                'phone': values[6],
                'position': values[7],
                'department': values[8],
                'member_type': values[9],
                'status': values[10]
            }
        else:
            return {
                'id': values[0],
                'member_code': values[1],
                'full_name': values[2], 
                'member_type': values[3],
                'position': values[4],
                'department': values[5],
                'status': values[6]
            }
    
    @staticmethod
    def update_status_bar(status_label: tk.Label, message: str, message_type: str = "info"):
        """
        Update status bar with message
        
        Args:
            status_label: Status label widget
            message: Message to display
            message_type: Type of message (info, success, error, warning)
        """
        colors = {
            'info': ModernTheme.GRAY_600,
            'success': ModernTheme.SUCCESS,
            'error': ModernTheme.ERROR,
            'warning': ModernTheme.WARNING
        }
        
        status_label.config(text=message, fg=colors.get(message_type, ModernTheme.GRAY_600))
        
        # Auto-clear after 5 seconds for non-info messages
        if message_type != "info":
            status_label.after(5000, lambda: status_label.config(text="Sẵn sàng", fg=ModernTheme.GRAY_600))
    
    @staticmethod
    def show_member_details(parent, member_data: Dict):
        """
        Show detailed member information in a popup window with scrollbar
        
        Args:
            parent: Parent widget
            member_data: Member data dictionary
        """
        detail_window = tk.Toplevel(parent)
        detail_window.title(f"Chi tiết thành viên - {member_data.get('full_name', 'N/A')}")
        detail_window.geometry("650x600")
        detail_window.resizable(True, True)  # Allow resizing
        detail_window.minsize(600, 500)  # Set minimum size
        detail_window.grab_set()
        
        # Center the window
        detail_window.transient(parent)
        detail_window.geometry("+%d+%d" % (
            parent.winfo_rootx() + 100, 
            parent.winfo_rooty() + 50
        ))
        
        # Create scrollable main container
        main_canvas = tk.Canvas(detail_window, bg=ModernTheme.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(detail_window, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=ModernTheme.WHITE)
        
        # Configure scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel binding for better scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        detail_window.bind("<MouseWheel>", _on_mousewheel)
        main_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Pack scrollbar and canvas
        main_canvas.pack(side="left", fill="both", expand=True, padx=(20, 5), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # Content container inside scrollable frame
        content_frame = tk.Frame(scrollable_frame, bg=ModernTheme.WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(content_frame, 
                              text=f"👤 {member_data.get('full_name', 'N/A')}", 
                              font=("Arial", 16, "bold"),
                              bg=ModernTheme.WHITE, fg=ModernTheme.PRIMARY)
        title_label.pack(pady=(0, 20))
        
        # Details in two columns
        details_frame = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = tk.Frame(details_frame, bg=ModernTheme.WHITE)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(details_frame, bg=ModernTheme.WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Left column fields
        left_fields = [
            ("Mã thành viên:", member_data.get('member_code', 'N/A')),
            ("Họ và tên:", member_data.get('full_name', 'N/A')),
            ("Ngày sinh:", member_data.get('date_of_birth', 'N/A')),
            ("Giới tính:", member_data.get('gender', 'N/A')),
            ("Số điện thoại:", member_data.get('phone', 'N/A')),
            ("Email:", member_data.get('email', 'N/A'))
        ]
        
        # Right column fields  
        right_fields = [
            ("Địa chỉ:", member_data.get('address', 'N/A')),
            ("Chức vụ:", member_data.get('position', 'N/A')),
            ("Phòng ban:", member_data.get('department', 'N/A')),
            ("Loại thành viên:", member_data.get('member_type', 'N/A')),
            ("Trạng thái:", member_data.get('status', 'N/A')),
            ("Ngày tham gia:", member_data.get('join_date', 'N/A'))
        ]
        
        # Create detail fields
        for fields, frame in [(left_fields, left_frame), (right_fields, right_frame)]:
            for label_text, value in fields:
                field_frame = tk.Frame(frame, bg=ModernTheme.WHITE)
                field_frame.pack(fill=tk.X, pady=5)
                
                label = tk.Label(field_frame, text=label_text, 
                               font=("Arial", 10, "bold"),
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700,
                               anchor=tk.W)
                label.pack(fill=tk.X)
                
                value_label = tk.Label(field_frame, text=str(value), 
                                     font=("Arial", 10),
                                     bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                     anchor=tk.W, relief=tk.FLAT, padx=10, pady=5)
                value_label.pack(fill=tk.X, pady=(2, 0))
        
        # Notes section (full width)
        if member_data.get('notes'):
            notes_frame = tk.Frame(content_frame, bg=ModernTheme.WHITE)
            notes_frame.pack(fill=tk.X, pady=(20, 0))
            
            notes_label = tk.Label(notes_frame, text="Ghi chú:", 
                                 font=("Arial", 10, "bold"),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700,
                                 anchor=tk.W)
            notes_label.pack(fill=tk.X)
            
            notes_text = tk.Text(notes_frame, height=4, 
                                font=("Arial", 10),
                                bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                wrap=tk.WORD, relief=tk.FLAT, padx=10, pady=5)
            notes_text.pack(fill=tk.X, pady=(2, 0))
            notes_text.insert(tk.END, member_data.get('notes', ''))
            notes_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(content_frame, text="❌ Đóng", 
                             font=("Arial", 10),
                             bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                             border=0, cursor="hand2", padx=30, pady=12,
                             command=detail_window.destroy)
        close_btn.pack(pady=(20, 0))
        
        # Update scrollbar after window is fully rendered
        def update_scroll_region():
            detail_window.update_idletasks()
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        detail_window.after(100, update_scroll_region)
        close_btn.pack(pady=(20, 0))


class MemberFilters:
    """Advanced filtering component for member list"""
    
    @staticmethod
    def create_filter_panel(parent, filter_callback: Callable = None) -> Dict[str, tk.StringVar]:
        """
        Create advanced filter panel for members
        
        Args:
            parent: Parent widget
            filter_callback: Callback function when filters change
            
        Returns:
            Dict of filter variables
        """
        filter_frame = tk.LabelFrame(parent, text="🔍 Bộ lọc", 
                                   font=("Arial", 9, "bold"),
                                   bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700,
                                   padx=10, pady=5)
        filter_frame.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        filters = {}
        
        # Filter row
        filter_row = tk.Frame(filter_frame, bg=ModernTheme.WHITE)
        filter_row.pack(fill=tk.X)
        
        # Department filter
        dept_frame = tk.Frame(filter_row, bg=ModernTheme.WHITE)
        dept_frame.pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Label(dept_frame, text="Phòng ban:", 
                font=("Arial", 8),
                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700).pack()
        
        dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(dept_frame, textvariable=dept_var, 
                                 values=["Tất cả", "Hành chính", "Kỹ thuật", "Tài chính", "Nhân sự"],
                                 state="readonly", width=10, font=("Arial", 8))
        dept_combo.pack()
        dept_combo.set("Tất cả")
        filters['department'] = dept_var
        
        # Member type filter
        type_frame = tk.Frame(filter_row, bg=ModernTheme.WHITE)
        type_frame.pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Label(type_frame, text="Loại TV:", 
                font=("Arial", 8),
                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700).pack()
        
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(type_frame, textvariable=type_var,
                                 values=["Tất cả", "Đoàn viên", "Hội viên", "Ban chấp hành"],
                                 state="readonly", width=12, font=("Arial", 8))
        type_combo.pack()
        type_combo.set("Tất cả")
        filters['member_type'] = type_var
        
        # Status filter
        status_frame = tk.Frame(filter_row, bg=ModernTheme.WHITE)
        status_frame.pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Label(status_frame, text="Trạng thái:", 
                font=("Arial", 8),
                bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700).pack()
        
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(status_frame, textvariable=status_var,
                                   values=["Tất cả", "Đang hoạt động", "Tạm ngưng", "Đình chỉ"],
                                   state="readonly", width=10, font=("Arial", 8))
        status_combo.pack()
        status_combo.set("Tất cả")
        filters['status'] = status_var
        
        # Apply filter button
        apply_btn = tk.Button(filter_row, text="Áp dụng", 
                             font=("Arial", 8),
                             bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                             border=0, cursor="hand2", padx=12, pady=3,
                             command=filter_callback if filter_callback else lambda: None)
        apply_btn.pack(side=tk.LEFT, padx=(8, 0))
        
        # Clear filter button
        def clear_filters():
            for var in filters.values():
                var.set("Tất cả")
            if filter_callback:
                filter_callback()
        
        clear_btn = tk.Button(filter_row, text="Xóa", 
                             font=("Arial", 8),
                             bg=ModernTheme.GRAY_200, fg=ModernTheme.GRAY_700,
                             border=0, cursor="hand2", padx=12, pady=3,
                             command=clear_filters)
        clear_btn.pack(side=tk.LEFT, padx=(3, 0))
        
        return filters


class MemberExport:
    """Member data export functionality"""
    
    @staticmethod
    def export_to_csv(parent, members: List[Any], filename: str = None):
        """
        Export member data to CSV file
        
        Args:
            parent: Parent widget for file dialog
            members: List of member objects
            filename: Optional filename
        """
        try:
            import csv
            
            if not filename:
                filename = filedialog.asksaveasfilename(
                    parent=parent,
                    title="Xuất danh sách thành viên",
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
            
            if not filename:
                return
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = [
                    'Mã thành viên', 'Họ tên', 'Ngày sinh', 'Giới tính',
                    'Số điện thoại', 'Email', 'Địa chỉ', 'Chức vụ', 
                    'Phòng ban', 'Loại thành viên', 'Trạng thái', 'Ngày tham gia'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for member in members:
                    writer.writerow({
                        'Mã thành viên': member.member_code,
                        'Họ tên': member.full_name,
                        'Ngày sinh': member.date_of_birth.strftime('%d/%m/%Y') if member.date_of_birth else '',
                        'Giới tính': member.gender,
                        'Số điện thoại': member.phone,
                        'Email': member.email,
                        'Địa chỉ': member.address,
                        'Chức vụ': member.position,
                        'Phòng ban': member.department,
                        'Loại thành viên': member.get_member_type_display() if hasattr(member, 'get_member_type_display') else member.member_type,
                        'Trạng thái': member.get_status_display() if hasattr(member, 'get_status_display') else member.status,
                        'Ngày tham gia': member.join_date.strftime('%d/%m/%Y') if member.join_date else ''
                    })
            
            messagebox.showinfo("Thành công", f"Đã xuất {len(members)} thành viên ra file: {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")


class MemberStats:
    """Member statistics component"""
    
    @staticmethod
    def create_stats_panel(parent, stats_data: Dict) -> tk.Frame:
        """
        Create member statistics panel
        
        Args:
            parent: Parent widget
            stats_data: Statistics data dictionary
            
        Returns:
            Stats panel frame
        """
        stats_frame = tk.LabelFrame(parent, text="📊 Thống kê", 
                                  font=("Arial", 9, "bold"),
                                  bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700,
                                  padx=10, pady=5)
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 5))
        
        # Stats container
        container = tk.Frame(stats_frame, bg=ModernTheme.WHITE)
        container.pack(fill=tk.X)
        
        # Statistics items
        stats_items = [
            ("👥 Tổng số:", stats_data.get('total', 0), ModernTheme.PRIMARY),
            ("👤 Đoàn viên:", stats_data.get('union_members', 0), ModernTheme.SUCCESS),
            ("👥 Hội viên:", stats_data.get('association_members', 0), ModernTheme.INFO),
            ("👔 Cán bộ:", stats_data.get('executives', 0), ModernTheme.WARNING),
            ("✅ Hoạt động:", stats_data.get('active', 0), ModernTheme.SUCCESS),
            ("⏸️ Tạm ngưng:", stats_data.get('inactive', 0), ModernTheme.GRAY_500)
        ]
        
        for i, (label, value, color) in enumerate(stats_items):
            stat_item = tk.Frame(container, bg=ModernTheme.WHITE)
            stat_item.pack(side=tk.LEFT, padx=(0, 15) if i < len(stats_items) - 1 else 0)
            
            # Value
            value_label = tk.Label(stat_item, text=str(value), 
                                 font=("Arial", 12, "bold"),
                                 bg=ModernTheme.WHITE, fg=color)
            value_label.pack()
            
            # Label
            label_label = tk.Label(stat_item, text=label, 
                                 font=("Arial", 8),
                                 bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_600)
            label_label.pack()
        
        return stats_frame