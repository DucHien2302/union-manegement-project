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
                    # Enhanced report type picker with visual indicators
                    values = ["📅 Báo cáo tháng", "📈 Báo cáo quý", "📋 Báo cáo năm", "⭐ Báo cáo đặc biệt"]
                    type_colors = {
                        "📅 Báo cáo tháng": ModernTheme.INFO,
                        "📈 Báo cáo quý": ModernTheme.SUCCESS,
                        "📋 Báo cáo năm": ModernTheme.WARNING,
                        "⭐ Báo cáo đặc biệt": ModernTheme.ACCENT
                    }
                else:  # status
                    # Enhanced status picker with visual indicators
                    values = ["📝 Nháp", "📤 Đã nộp", "✅ Đã duyệt", "❌ Từ chối"]
                    status_colors = {
                        "📝 Nháp": ModernTheme.GRAY_500,
                        "📤 Đã nộp": ModernTheme.PRIMARY,
                        "✅ Đã duyệt": ModernTheme.SUCCESS,
                        "❌ Từ chối": ModernTheme.DANGER
                    }
                
                # Create custom picker container
                picker_container = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                picker_container.pack(fill=tk.X, pady=(4, 0))
                
                # Enhanced combobox with better styling
                combo_style = ttk.Style()
                combo_style.configure("Modern.TCombobox",
                                     fieldbackground=ModernTheme.GRAY_50,
                                     background=ModernTheme.WHITE,
                                     borderwidth=1,
                                     relief="solid")
                
                combo = ttk.Combobox(picker_container, textvariable=var, values=values, 
                                   state="readonly", font=ModernTheme.FONT_PRIMARY,
                                   style="Modern.TCombobox", height=6)
                combo.pack(fill=tk.X, ipady=8)
                
                # Color indicator frame
                indicator_frame = tk.Frame(picker_container, bg=ModernTheme.WHITE, height=4)
                indicator_frame.pack(fill=tk.X, pady=(2, 0))
                
                color_indicator = tk.Frame(indicator_frame, height=3, bg=ModernTheme.GRAY_200)
                color_indicator.pack(fill=tk.X)
                
                # Update color indicator when selection changes
                def update_color_indicator(event=None):
                    selected_value = var.get()
                    if field_name == "report_type" and selected_value in type_colors:
                        color_indicator.configure(bg=type_colors[selected_value])
                    elif field_name == "status" and selected_value in status_colors:
                        color_indicator.configure(bg=status_colors[selected_value])
                    else:
                        color_indicator.configure(bg=ModernTheme.GRAY_200)
                
                combo.bind('<<ComboboxSelected>>', update_color_indicator)
                var.trace('w', lambda *args: update_color_indicator())
                
                # Set initial value if report_data exists
                if report_data and field_name in report_data:
                    initial_value = report_data[field_name]
                    print(f"🔍 Debug - Setting {field_name} to: {initial_value}")
                    
                    # Map plain text to emoji versions
                    value_mapping = {}
                    if field_name == "report_type":
                        value_mapping = {
                            "Báo cáo tháng": "📅 Báo cáo tháng", "monthly": "📅 Báo cáo tháng",
                            "Báo cáo quý": "📈 Báo cáo quý", "quarterly": "📈 Báo cáo quý",
                            "Báo cáo năm": "📋 Báo cáo năm", "annual": "📋 Báo cáo năm",
                            "Báo cáo đặc biệt": "⭐ Báo cáo đặc biệt", "special": "⭐ Báo cáo đặc biệt"
                        }
                    else:  # status
                        value_mapping = {
                            "Nháp": "📝 Nháp", "draft": "📝 Nháp",
                            "Đã nộp": "📤 Đã nộp", "submitted": "📤 Đã nộp",
                            "Đã duyệt": "✅ Đã duyệt", "approved": "✅ Đã duyệt",
                            "Từ chối": "❌ Từ chối", "rejected": "❌ Từ chối"
                        }
                    
                    # Find matching value
                    display_value = value_mapping.get(initial_value, initial_value)
                    if display_value in values:
                        combo.set(display_value)
                        var.set(display_value)
                        update_color_indicator()
                    else:
                        # Try partial match
                        for key, val in value_mapping.items():
                            if initial_value.lower() in key.lower() or key.lower() in initial_value.lower():
                                combo.set(val)
                                var.set(val)
                                update_color_indicator()
                                print(f"✅ Found partial match: {val}")
                                break
                
                variables[field_name] = var
                
            elif field_type == "text":
                # Enhanced text area with better styling
                text_container = tk.Frame(field_frame, bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                text_container.pack(fill=tk.X, pady=(4, 0))
                
                # Text widget with scrollbar
                text_frame = tk.Frame(text_container, bg=ModernTheme.GRAY_50)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                text_widget = tk.Text(text_frame, height=8, 
                                    font=ModernTheme.FONT_PRIMARY,
                                    bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                                    relief=tk.FLAT, bd=0, wrap=tk.WORD,
                                    selectbackground=ModernTheme.PRIMARY,
                                    selectforeground=ModernTheme.WHITE)
                
                # Add scrollbar for text areas
                scrollbar_text = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
                text_widget.configure(yscrollcommand=scrollbar_text.set)
                
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Focus effects for text area
                def on_text_focus_in(event):
                    text_container.configure(bg=ModernTheme.PRIMARY, relief=tk.SOLID, bd=1)
                    
                def on_text_focus_out(event):
                    text_container.configure(bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                
                text_widget.bind('<FocusIn>', on_text_focus_in)
                text_widget.bind('<FocusOut>', on_text_focus_out)
                
                # Add character counter and word counter for content
                if field_name == "content":
                    count_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                    count_frame.pack(fill=tk.X, pady=(2, 0))
                    
                    word_count_label = tk.Label(count_frame, text="0 từ", 
                                              font=('Segoe UI', 8), 
                                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                    word_count_label.pack(side=tk.LEFT)
                    
                    char_count_label = tk.Label(count_frame, text="0 ký tự", 
                                              font=('Segoe UI', 8), 
                                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                    char_count_label.pack(side=tk.RIGHT)
                    
                    def update_counts(*args):
                        content = text_widget.get("1.0", tk.END).strip()
                        char_count = len(content)
                        word_count = len(content.split()) if content else 0
                        char_count_label.configure(text=f"{char_count} ký tự")
                        word_count_label.configure(text=f"{word_count} từ")
                    
                    # Bind to text changes
                    def on_text_change(event):
                        text_widget.after_idle(update_counts)
                    
                    text_widget.bind('<KeyRelease>', on_text_change)
                    text_widget.bind('<Button-1>', on_text_change)
                    text_widget.bind('<Control-v>', on_text_change)  # Paste
                    
                    # Quick format buttons for report content
                    format_frame = tk.Frame(count_frame, bg=ModernTheme.WHITE)
                    format_frame.pack(side=tk.LEFT, padx=(20, 0))
                    
                    def insert_template(template_type):
                        templates = {
                            "summary": "\n--- TÓM TẮT THỰC HIỆN ---\n\n",
                            "detail": "\n--- CHI TIẾT CÔNG VIỆC ---\n\n",
                            "issues": "\n--- VẤN ĐỀ GẶP PHẢI ---\n\n",
                            "next": "\n--- KẾ HOẠCH TIẾP THEO ---\n\n"
                        }
                        template = templates.get(template_type, "")
                        text_widget.insert(tk.INSERT, template)
                        update_counts()
                    
                    format_buttons = [
                        ("📋 Tóm tắt", "summary"),
                        ("📝 Chi tiết", "detail"),
                        ("⚠️ Vấn đề", "issues"),
                        ("🎯 Kế hoạch", "next")
                    ]
                    
                    for btn_text, template_type in format_buttons:
                        format_btn = tk.Button(format_frame, text=btn_text,
                                             font=('Segoe UI', 8),
                                             bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                                             border=0, cursor="hand2", padx=6, pady=2,
                                             command=lambda t=template_type: insert_template(t))
                        format_btn.pack(side=tk.LEFT, padx=(2, 0))
                
                # Add field-specific hints
                if field_name == "content":
                    hint_label = tk.Label(field_frame, text="💡 Nội dung chi tiết của báo cáo - sử dụng các mẫu phía trên để định dạng", 
                                        font=('Segoe UI', 9), 
                                        bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                    hint_label.pack(anchor=tk.W, pady=(2, 0))
                
                if report_data and field_name in report_data:
                    text_widget.insert(tk.END, str(report_data[field_name]))
                    if field_name == "content":
                        update_counts()
                
                variables[field_name] = text_widget  # Store widget instead of StringVar
                
            else:  # entry
                var = tk.StringVar()
                
                # Enhanced entry field with better styling
                entry_container = tk.Frame(field_frame, bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                entry_container.pack(fill=tk.X, pady=(4, 0))
                
                entry = tk.Entry(entry_container, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=0)
                entry.pack(fill=tk.X, padx=10, pady=8)
                
                # Add placeholder text and focus effects
                def on_focus_in(event):
                    entry_container.configure(bg=ModernTheme.PRIMARY, relief=tk.SOLID, bd=1)
                    
                def on_focus_out(event):
                    entry_container.configure(bg=ModernTheme.GRAY_50, relief=tk.FLAT, bd=1)
                
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)
                
                # Add field-specific hints and quick buttons
                if field_name == "title":
                    hint_label = tk.Label(field_frame, text="💡 Tiêu đề ngắn gọn và rõ ràng cho báo cáo", 
                                        font=('Segoe UI', 9), 
                                        bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                    hint_label.pack(anchor=tk.W, pady=(2, 0))
                elif field_name == "period":
                    hint_frame = tk.Frame(field_frame, bg=ModernTheme.WHITE)
                    hint_frame.pack(fill=tk.X, pady=(2, 0))
                    
                    hint_label = tk.Label(hint_frame, text="💡 Kỳ báo cáo (ví dụ: Tháng 12/2024, Quý 4/2024)", 
                                        font=('Segoe UI', 9), 
                                        bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
                    hint_label.pack(side=tk.LEFT)
                    
                    # Quick period buttons
                    quick_periods_frame = tk.Frame(hint_frame, bg=ModernTheme.WHITE)
                    quick_periods_frame.pack(side=tk.RIGHT)
                    
                    def set_current_period(period_type):
                        import datetime
                        now = datetime.datetime.now()
                        if period_type == "month":
                            period = f"Tháng {now.month:02d}/{now.year}"
                        elif period_type == "quarter":
                            quarter = (now.month - 1) // 3 + 1
                            period = f"Quý {quarter}/{now.year}"
                        elif period_type == "year":
                            period = f"Năm {now.year}"
                        var.set(period)
                    
                    # Quick period buttons
                    period_buttons = [
                        ("Tháng này", "month"),
                        ("Quý này", "quarter"),
                        ("Năm này", "year")
                    ]
                    
                    for btn_text, period_type in period_buttons:
                        period_btn = tk.Button(quick_periods_frame, text=btn_text,
                                             font=('Segoe UI', 8),
                                             bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                                             border=0, cursor="hand2", padx=6, pady=2,
                                             command=lambda p=period_type: set_current_period(p))
                        period_btn.pack(side=tk.LEFT, padx=(2, 0))
                
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
            title_value = variables['title'].get().strip() if variables['title'].get() else ""
            if not title_value:
                errors.append("❌ Tiêu đề báo cáo không được để trống")
            
            report_type_value = variables['report_type'].get()
            if not report_type_value:
                errors.append("❌ Vui lòng chọn loại báo cáo")
            
            period_value = variables['period'].get().strip() if variables['period'].get() else ""
            if not period_value:
                errors.append("❌ Kỳ báo cáo không được để trống")
            
            status_value = variables['status'].get()
            if not status_value:
                errors.append("❌ Vui lòng chọn trạng thái")
            
            # Validate content length
            content_value = variables['content'].get("1.0", tk.END).strip() if isinstance(variables['content'], tk.Text) else ""
            if len(content_value) < 10:
                errors.append("❌ Nội dung báo cáo phải có ít nhất 10 ký tự")
            
            # Validate title length
            if len(title_value) > 150:
                errors.append("❌ Tiêu đề không được vượt quá 150 ký tự")
            
            # Validate period format (basic check)
            if period_value and not any(keyword in period_value.lower() for keyword in ['tháng', 'quý', 'năm']):
                errors.append("❌ Kỳ báo cáo nên bao gồm 'Tháng', 'Quý' hoặc 'Năm'")
            
            return errors
        
        def on_save():
            nonlocal is_saved
            
            # Validate form
            errors = validate_form()
            if errors:
                from tkinter import messagebox
                error_message = "Vui lòng kiểm tra lại các thông tin sau:\n\n" + "\n".join(errors)
                messagebox.showerror("⚠️ Lỗi nhập liệu", error_message)
                return
            
            # Collect form data
            for field_name, var in variables.items():
                if isinstance(var, tk.Text):
                    result[field_name] = var.get("1.0", tk.END).strip()
                else:
                    value = var.get()
                    # Convert emoji values back to plain text for database storage
                    if field_name == "report_type":
                        type_reverse_mapping = {
                            "📅 Báo cáo tháng": "Báo cáo tháng",
                            "📈 Báo cáo quý": "Báo cáo quý",
                            "📋 Báo cáo năm": "Báo cáo năm",
                            "⭐ Báo cáo đặc biệt": "Báo cáo đặc biệt"
                        }
                        result[field_name] = type_reverse_mapping.get(value, value)
                    elif field_name == "status":
                        status_reverse_mapping = {
                            "📝 Nháp": "Nháp",
                            "📤 Đã nộp": "Đã nộp",
                            "✅ Đã duyệt": "Đã duyệt",
                            "❌ Từ chối": "Từ chối"
                        }
                        result[field_name] = status_reverse_mapping.get(value, value)
                    else:
                        result[field_name] = value
            is_saved = True
            dialog.destroy()
        
        def on_cancel():
            nonlocal is_saved
            result.clear()
            is_saved = False
            dialog.destroy()
        
        # Create buttons with enhanced styling and spacing
        button_container = tk.Frame(button_frame, bg=ModernTheme.WHITE)
        button_container.pack(expand=True, fill=tk.BOTH)
        
        # Enhanced cancel button
        cancel_btn = tk.Button(button_container, text="❌ Hủy bỏ", 
                              font=ModernTheme.FONT_PRIMARY,
                              bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                              border=0, cursor="hand2", padx=25, pady=12,
                              command=on_cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(ModernTheme.PADDING_SMALL, ModernTheme.PADDING_MEDIUM), 
                       pady=ModernTheme.PADDING_SMALL)
        
        # Enhanced save button
        save_btn = tk.Button(button_container, text="💾 Lưu báo cáo", 
                            font=ModernTheme.FONT_PRIMARY,
                            bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                            border=0, cursor="hand2", padx=25, pady=12,
                            command=on_save)
        save_btn.pack(side=tk.RIGHT, padx=(0, ModernTheme.PADDING_SMALL), 
                     pady=ModernTheme.PADDING_SMALL)
        
        # Button hover effects
        def on_save_hover_enter(event):
            save_btn.configure(bg=ModernTheme.PRIMARY_DARK)
        
        def on_save_hover_leave(event):
            save_btn.configure(bg=ModernTheme.PRIMARY)
            
        def on_cancel_hover_enter(event):
            cancel_btn.configure(bg=ModernTheme.GRAY_200)
        
        def on_cancel_hover_leave(event):
            cancel_btn.configure(bg=ModernTheme.GRAY_100)
        
        save_btn.bind('<Enter>', on_save_hover_enter)
        save_btn.bind('<Leave>', on_save_hover_leave)
        cancel_btn.bind('<Enter>', on_cancel_hover_enter)
        cancel_btn.bind('<Leave>', on_cancel_hover_leave)
        
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