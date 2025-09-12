"""
Modern UI Theme Configuration
Provides consistent styling, colors, fonts, and spacing for the Union Management System
"""

import tkinter as tk
from tkinter import ttk


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


class StyleManager:
    """Manages TTK styles for consistent theming"""
    
    @staticmethod
    def configure_modern_styles():
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
        
        # Configure Button styles
        style.configure("Primary.TButton",
                       background=ModernTheme.PRIMARY,
                       foreground=ModernTheme.WHITE,
                       borderwidth=0,
                       focuscolor="none")
        
        style.map("Primary.TButton",
                 background=[('active', ModernTheme.PRIMARY_DARK),
                           ('pressed', ModernTheme.PRIMARY_DARK)])
        
        style.configure("Secondary.TButton",
                       background=ModernTheme.GRAY_100,
                       foreground=ModernTheme.GRAY_700,
                       borderwidth=0,
                       focuscolor="none")
        
        style.map("Secondary.TButton",
                 background=[('active', ModernTheme.GRAY_200),
                           ('pressed', ModernTheme.GRAY_200)])

    @staticmethod
    def apply_theme_to_root(root):
        """Apply modern theme to root window"""
        root.configure(bg=ModernTheme.GRAY_50)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Apply modern styles
        StyleManager.configure_modern_styles()