"""
Base UI Components
Common reusable UI elements for the Union Management System
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple, Optional, Dict, Any
from presentation.gui.theme import ModernTheme


class BaseHeader:
    """Base header component with consistent styling"""
    
    @staticmethod
    def create_header(parent, title: str, actions: List[Tuple[str, Callable]] = None) -> tk.Frame:
        """
        Create a modern header with title and action buttons
        
        Args:
            parent: Parent widget
            title: Header title text
            actions: List of (button_text, callback) tuples
            
        Returns:
            Header frame
        """
        # Header section
        header_frame = tk.Frame(parent, bg=ModernTheme.WHITE, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 1))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=ModernTheme.WHITE)
        header_content.pack(fill=tk.BOTH, expand=True, 
                           padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Title
        title_label = tk.Label(header_content, text=title, 
                              font=ModernTheme.FONT_HEADING,
                              bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900)
        title_label.pack(side=tk.LEFT)
        
        # Action buttons
        if actions:
            action_frame = tk.Frame(header_content, bg=ModernTheme.WHITE)
            action_frame.pack(side=tk.RIGHT)
            
            for i, (button_text, callback) in enumerate(actions):
                is_primary = i == len(actions) - 1  # Last button is primary
                
                btn = tk.Button(action_frame, text=button_text, 
                               font=ModernTheme.FONT_PRIMARY,
                               bg=ModernTheme.PRIMARY if is_primary else ModernTheme.GRAY_100,
                               fg=ModernTheme.WHITE if is_primary else ModernTheme.GRAY_700,
                               border=0, cursor="hand2", padx=16 if is_primary else 12, pady=8,
                               command=callback)
                
                if is_primary:
                    btn.pack(side=tk.RIGHT, padx=(8, 0))
                else:
                    btn.pack(side=tk.RIGHT, padx=(0, 8))
                
                # Add hover effects
                BaseButton.add_hover_effects(btn, is_primary)
        
        return header_frame


class BaseButton:
    """Base button component with hover effects"""
    
    @staticmethod
    def create_primary_button(parent, text: str, command: Callable, **kwargs) -> tk.Button:
        """Create a primary button with modern styling"""
        btn = tk.Button(parent, text=text, 
                       font=ModernTheme.FONT_PRIMARY,
                       bg=ModernTheme.PRIMARY, fg=ModernTheme.WHITE,
                       border=0, cursor="hand2", padx=16, pady=8,
                       command=command, **kwargs)
        
        BaseButton.add_hover_effects(btn, is_primary=True)
        return btn
    
    @staticmethod
    def create_secondary_button(parent, text: str, command: Callable, **kwargs) -> tk.Button:
        """Create a secondary button with modern styling"""
        btn = tk.Button(parent, text=text, 
                       font=ModernTheme.FONT_PRIMARY,
                       bg=ModernTheme.GRAY_100, fg=ModernTheme.GRAY_700,
                       border=0, cursor="hand2", padx=12, pady=8,
                       command=command, **kwargs)
        
        BaseButton.add_hover_effects(btn, is_primary=False)
        return btn
    
    @staticmethod
    def add_hover_effects(btn: tk.Button, is_primary: bool = True):
        """Add hover effects to button"""
        if is_primary:
            normal_bg = ModernTheme.PRIMARY
            hover_bg = ModernTheme.PRIMARY_DARK
            normal_fg = ModernTheme.WHITE
            hover_fg = ModernTheme.WHITE
        else:
            normal_bg = ModernTheme.GRAY_100
            hover_bg = ModernTheme.GRAY_200
            normal_fg = ModernTheme.GRAY_700
            hover_fg = ModernTheme.GRAY_800
        
        def on_enter(e):
            btn.configure(bg=hover_bg, fg=hover_fg)
        
        def on_leave(e):
            btn.configure(bg=normal_bg, fg=normal_fg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)


class BaseTable:
    """Base table component with modern styling"""
    
    @staticmethod
    def create_modern_table(parent, columns: List[str], column_widths: Dict[str, int] = None) -> Tuple[ttk.Treeview, tk.Frame]:
        """
        Create a modern table with scrollbars
        
        Args:
            parent: Parent widget
            columns: List of column names
            column_widths: Dict mapping column names to widths
            
        Returns:
            Tuple of (treeview, container_frame)
        """
        # Table container
        table_container = tk.Frame(parent, bg=ModernTheme.WHITE)
        
        # Treeview with modern style
        tree = ttk.Treeview(table_container, columns=columns, show='headings', 
                           style='Modern.Treeview', height=15)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            width = column_widths.get(col, 100) if column_widths else 100
            tree.column(col, width=width, anchor=tk.W)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with padding
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                 padx=ModernTheme.PADDING_LARGE, pady=ModernTheme.PADDING_LARGE)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=ModernTheme.PADDING_LARGE)
        
        # Row selection styling
        tree.tag_configure('selected', background=ModernTheme.PRIMARY_LIGHT)
        
        return tree, table_container


class BaseFilter:
    """Base filter component"""
    
    @staticmethod
    def create_filter_section(parent, filters: List[Tuple[str, List[str], Callable]]) -> Dict[str, tk.StringVar]:
        """
        Create a filter section with multiple combo boxes
        
        Args:
            parent: Parent widget
            filters: List of (label, options, callback) tuples
            
        Returns:
            Dict mapping filter names to StringVar objects
        """
        # Filter container
        filter_container = tk.Frame(parent, bg=ModernTheme.WHITE)
        filter_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                             pady=(ModernTheme.PADDING_MEDIUM, ModernTheme.PADDING_SMALL))
        
        filter_content = tk.Frame(filter_container, bg=ModernTheme.WHITE)
        filter_content.pack(fill=tk.X, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        filter_frame = tk.Frame(filter_content, bg=ModernTheme.WHITE)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        variables = {}
        
        for i, (label, options, callback) in enumerate(filters):
            # Label
            filter_label = tk.Label(filter_frame, text=f"{label}:", 
                                   font=ModernTheme.FONT_PRIMARY,
                                   bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_700)
            filter_label.pack(side=tk.LEFT)
            
            # Combobox
            var = tk.StringVar(value=options[0] if options else "")
            combo = ttk.Combobox(filter_frame, textvariable=var,
                               values=options, state="readonly", width=15)
            combo.pack(side=tk.LEFT, padx=(8, 16 if i < len(filters) - 1 else 0))
            
            if callback:
                combo.bind('<<ComboboxSelected>>', callback)
            
            variables[label.lower().replace(" ", "_")] = var
        
        return variables


class BaseSearch:
    """Base search component"""
    
    @staticmethod
    def create_search_box(parent, placeholder: str = "Tìm kiếm...", callback: Callable = None) -> Tuple[tk.Entry, tk.StringVar]:
        """
        Create a modern search box with placeholder
        
        Args:
            parent: Parent widget
            placeholder: Placeholder text
            callback: Search callback function
            
        Returns:
            Tuple of (entry_widget, string_var)
        """
        # Search container
        search_container = tk.Frame(parent, bg=ModernTheme.WHITE)
        search_container.pack(fill=tk.X, padx=ModernTheme.PADDING_MEDIUM, 
                             pady=(ModernTheme.PADDING_MEDIUM, ModernTheme.PADDING_SMALL))
        
        search_content = tk.Frame(search_container, bg=ModernTheme.WHITE)
        search_content.pack(fill=tk.X, padx=ModernTheme.PADDING_LARGE, 
                           pady=ModernTheme.PADDING_MEDIUM)
        
        # Search icon
        search_label = tk.Label(search_content, text="🔍", font=("Segoe UI", 16),
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_500)
        search_label.pack(side=tk.LEFT)
        
        # Search entry
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_content, textvariable=search_var,
                               font=ModernTheme.FONT_PRIMARY, relief=tk.FLAT,
                               bg=ModernTheme.WHITE, fg=ModernTheme.GRAY_900,
                               border=0)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
        
        if callback:
            search_entry.bind('<KeyRelease>', callback)
        
        # Placeholder functionality
        search_entry.insert(0, placeholder)
        search_entry.config(fg=ModernTheme.GRAY_400)
        
        def on_focus_in(event):
            if search_entry.get() == placeholder:
                search_entry.delete(0, tk.END)
                search_entry.config(fg=ModernTheme.GRAY_900)
        
        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, placeholder)
                search_entry.config(fg=ModernTheme.GRAY_400)
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        return search_entry, search_var


class BaseCard:
    """Base card component for dashboard and other sections"""
    
    @staticmethod
    def create_card(parent, **kwargs) -> tk.Frame:
        """Create a base card with consistent styling"""
        card = tk.Frame(parent, bg=ModernTheme.WHITE, relief=tk.FLAT, bd=1, **kwargs)
        return card
    
    @staticmethod
    def add_card_hover_effects(card: tk.Frame, child_widgets: List[tk.Widget] = None):
        """Add hover effects to card"""
        def on_enter(event):
            card.configure(bg=ModernTheme.GRAY_50)
            if child_widgets:
                for widget in child_widgets:
                    widget.configure(bg=ModernTheme.GRAY_50)
        
        def on_leave(event):
            card.configure(bg=ModernTheme.WHITE)
            if child_widgets:
                for widget in child_widgets:
                    widget.configure(bg=ModernTheme.WHITE)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        if child_widgets:
            for widget in child_widgets:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)