"""
Member Management Components
Specialized components for member management including member table,
search functionality, and member forms
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple, Optional, Dict, Any
from presentation.gui.theme import ModernTheme
from presentation.gui.base_components import BaseHeader, BaseTable, BaseSearch


class MemberTable:
    """Member table component with modern styling"""
    
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
            'ID': 60, 'Mã TV': 100, 'Họ tên': 200, 'Loại': 120, 
            'Chức vụ': 150, 'Phòng ban': 150, 'Trạng thái': 100
        }
        
        tree, container = BaseTable.create_modern_table(parent, columns, column_widths)
        tree.configure(height=15)
        
        return tree, container


class MemberSearch:
    """Member search component"""
    
    @staticmethod
    def create_member_search(parent, search_callback: Callable = None) -> Tuple[tk.Entry, tk.StringVar]:
        """
        Create member search box
        
        Args:
            parent: Parent widget
            search_callback: Search callback function
            
        Returns:
            Tuple of (entry_widget, string_var)
        """
        return BaseSearch.create_search_box(parent, "Tìm kiếm thành viên...", search_callback)


class MemberTab:
    """Complete member management tab component"""
    
    @staticmethod
    def create_member_tab(parent, callbacks: Dict[str, Callable] = None) -> Tuple[tk.Frame, ttk.Treeview, tk.StringVar]:
        """
        Create complete member management tab
        
        Args:
            parent: Parent widget (usually notebook)
            callbacks: Dict of callback functions for actions
            
        Returns:
            Tuple of (member_frame, member_tree, search_var)
        """
        member_frame = ttk.Frame(parent)
        
        # Default callbacks
        default_callbacks = {
            'add_member': lambda: None,
            'edit_member': lambda: None,
            'delete_member': lambda: None,
            'search_members': lambda e=None: None
        }
        if callbacks:
            default_callbacks.update(callbacks)
        
        # Header with actions
        actions = [
            ("✏️ Sửa", default_callbacks['edit_member']),
            ("🗑️ Xóa", default_callbacks['delete_member']),
            ("➕ Thêm thành viên", default_callbacks['add_member'])
        ]
        BaseHeader.create_header(member_frame, "Quản lý Thành viên", actions)
        
        # Content area
        content_frame = tk.Frame(member_frame, bg=ModernTheme.GRAY_50)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search section
        search_entry, search_var = MemberSearch.create_member_search(
            content_frame, default_callbacks['search_members'])
        
        # Table container
        table_container = tk.Frame(content_frame, bg=ModernTheme.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, 
                            padx=ModernTheme.PADDING_MEDIUM, 
                            pady=(0, ModernTheme.PADDING_MEDIUM))
        
        # Create member table
        member_tree, _ = MemberTable.create_member_table(table_container)
        
        return member_frame, member_tree, search_var


class MemberForm:
    """Member form component for add/edit operations"""
    
    @staticmethod
    def create_member_form_dialog(parent, title: str = "Thông tin thành viên", 
                                 member_data: Dict = None) -> Optional[Dict]:
        """
        Create member form dialog
        
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
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make it modal
        
        # Center the dialog
        dialog.transient(parent)
        dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        result = {}
        
        # Main container
        main_frame = tk.Frame(dialog, bg=ModernTheme.WHITE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=ModernTheme.PADDING_LARGE, 
                       pady=ModernTheme.PADDING_LARGE)
        
        # Form fields
        fields = [
            ("Mã thành viên:", "member_code"),
            ("Họ và tên:", "full_name"),
            ("Ngày sinh:", "birth_date"),
            ("Giới tính:", "gender"),
            ("Số điện thoại:", "phone"),
            ("Email:", "email"),
            ("Địa chỉ:", "address"),
            ("Chức vụ:", "position"),
            ("Phòng ban:", "department"),
            ("Loại thành viên:", "member_type"),
            ("Trạng thái:", "status")
        ]
        
        variables = {}
        
        for label_text, field_name in fields:
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
            if field_name in ["gender", "member_type", "status"]:
                # Combo box for predefined values
                var = tk.StringVar()
                
                if field_name == "gender":
                    values = ["Nam", "Nữ", "Khác"]
                elif field_name == "member_type":
                    values = ["Đoàn viên", "Hội viên", "Cán bộ"]
                else:  # status
                    values = ["Hoạt động", "Tạm dừng", "Nghỉ"]
                
                combo = ttk.Combobox(field_frame, textvariable=var, values=values, 
                                   state="readonly", font=ModernTheme.FONT_PRIMARY)
                combo.pack(fill=tk.X, pady=(4, 0))
                
                if member_data and field_name in member_data:
                    combo.set(member_data[field_name])
                
                variables[field_name] = var
            else:
                # Regular entry
                var = tk.StringVar()
                entry = tk.Entry(field_frame, textvariable=var, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.GRAY_50, fg=ModernTheme.GRAY_900,
                               relief=tk.FLAT, bd=5)
                entry.pack(fill=tk.X, pady=(4, 0))
                
                if member_data and field_name in member_data:
                    entry.insert(0, str(member_data[field_name]))
                
                variables[field_name] = var
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=ModernTheme.WHITE)
        button_frame.pack(fill=tk.X, pady=(ModernTheme.PADDING_LARGE, 0))
        
        # Buttons
        def on_save():
            # Collect form data
            for field_name, var in variables.items():
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


class MemberActions:
    """Member action handlers and utilities"""
    
    @staticmethod
    def populate_member_tree(tree: ttk.Treeview, members: List[Any]):
        """
        Populate member tree with data
        
        Args:
            tree: Treeview widget
            members: List of member objects
        """
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Add members
        for member in members:
            tree.insert('', 'end', values=(
                member.id,
                member.member_code,
                member.full_name,
                member.member_type.value if hasattr(member.member_type, 'value') else member.member_type,
                member.position,
                member.department,
                member.status.value if hasattr(member.status, 'value') else member.status
            ))
    
    @staticmethod
    def get_selected_member_id(tree: ttk.Treeview) -> Optional[int]:
        """
        Get selected member ID from tree
        
        Args:
            tree: Treeview widget
            
        Returns:
            Member ID or None if no selection
        """
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            return int(item['values'][0])  # ID is first column
        return None
    
    @staticmethod
    def search_members(tree: ttk.Treeview, search_term: str, all_members: List[Any]):
        """
        Filter members in tree based on search term
        
        Args:
            tree: Treeview widget
            search_term: Search string
            all_members: Complete list of members
        """
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)
        
        # If no search term, show all
        if not search_term or search_term == "Tìm kiếm thành viên...":
            MemberActions.populate_member_tree(tree, all_members)
            return
        
        # Filter members
        filtered_members = []
        search_lower = search_term.lower()
        
        for member in all_members:
            if (search_lower in member.full_name.lower() or
                search_lower in member.member_code.lower() or
                search_lower in (member.position or "").lower() or
                search_lower in (member.department or "").lower()):
                filtered_members.append(member)
        
        # Populate with filtered results
        MemberActions.populate_member_tree(tree, filtered_members)