"""
Member Management Controller
Kết nối giữa GUI và business logic cho quản lý thành viên
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from typing import List, Optional, Dict, Any
import traceback

from domain.entities.member import Member, MemberType, MemberStatus
from application.use_cases.member_management import MemberManagementUseCase
from infrastructure.repositories.member_repository_impl import MemberRepository
from presentation.gui.member_components import (
    MemberTab, MemberForm, MemberActions, MemberExport, 
    MemberFilters, MemberStats
)


class MemberController:
    """Controller cho quản lý thành viên với đầy đủ chức năng CRUD"""
    
    def __init__(self, parent_widget: tk.Widget):
        self.parent = parent_widget
        self.member_repository = MemberRepository()
        self.member_use_case = MemberManagementUseCase(self.member_repository)
        
        # GUI components
        self.member_frame = None
        self.member_tree = None
        self.search_var = None
        self.filter_vars = {}
        self.status_label = None
        
        # Data
        self.all_members = []
        self.filtered_members = []
        
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self):
        """Thiết lập giao diện người dùng"""
        callbacks = {
            'add_member': self.add_member,
            'edit_member': self.edit_member,
            'delete_member': self.delete_member,
            'view_member': self.view_member,
            'search_members': self.search_members,
            'filter_members': self.filter_members,
            'export_members': self.export_members,
            'bulk_action': self.bulk_action,
            'refresh_data': self.refresh_data
        }
        
        # Tạo tab quản lý thành viên
        result = MemberTab.create_member_tab(self.parent, callbacks)
        self.member_frame, self.member_tree, self.search_var, self.filter_vars = result
        
        # Lưu tham chiếu status label
        if hasattr(self.member_frame, 'status_label'):
            self.status_label = self.member_frame.status_label
    
    def _load_initial_data(self):
        """Tải dữ liệu ban đầu"""
        try:
            self.refresh_data()
        except Exception as e:
            self._show_error("Lỗi tải dữ liệu", f"Không thể tải danh sách thành viên: {str(e)}")
    
    def refresh_data(self):
        """Làm mới dữ liệu từ database"""
        try:
            self._update_status("Đang tải dữ liệu...", "info")
            
            # Lấy danh sách thành viên
            self.all_members = self.member_use_case.get_all_members()
            self.filtered_members = self.all_members.copy()
            
            # Cập nhật bảng
            MemberActions.populate_member_tree(self.member_tree, self.all_members, enhanced_mode=True)
            
            # Cập nhật thống kê
            stats = self.member_use_case.get_member_statistics()
            self._update_statistics(stats)
            
            self._update_status(f"Đã tải {len(self.all_members)} thành viên", "success")
            
        except Exception as e:
            self._show_error("Lỗi làm mới dữ liệu", str(e))
            self._update_status("Lỗi tải dữ liệu", "error")
    
    def add_member(self):
        """Thêm thành viên mới"""
        try:
            form_data = MemberForm.create_member_form_dialog(
                self.parent, "Thêm thành viên mới"
            )
            
            if not form_data:
                return
            
            # Validate dữ liệu
            errors = self.member_use_case.validate_member_data(form_data)
            if errors:
                messagebox.showerror("Lỗi validation", "\n".join(errors))
                return
            
            # Chuyển đổi dữ liệu
            member_data = self._convert_form_data(form_data)
            
            # Tạo thành viên mới
            new_member = self.member_use_case.create_member(member_data)
            
            # Làm mới danh sách
            self.refresh_data()
            
            self._update_status(f"Đã thêm thành viên: {new_member.full_name}", "success")
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            self._show_error("Lỗi thêm thành viên", str(e))
    
    def edit_member(self):
        """Chỉnh sửa thành viên"""
        try:
            member_id = MemberActions.get_selected_member_id(self.member_tree, enhanced_mode=True)
            if not member_id:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn thành viên cần chỉnh sửa")
                return
            
            # Lấy thông tin thành viên hiện tại
            member = self.member_use_case.get_member_by_id(member_id)
            if not member:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin thành viên")
                return
            
            # Chuyển đổi sang form data
            current_data = self._convert_member_to_form_data(member)
            
            # Hiển thị form chỉnh sửa
            form_data = MemberForm.create_member_form_dialog(
                self.parent, f"Chỉnh sửa thành viên - {member.full_name}", current_data
            )
            
            if not form_data:
                return
            
            # Validate dữ liệu
            errors = self.member_use_case.validate_member_data(form_data)
            if errors:
                messagebox.showerror("Lỗi validation", "\n".join(errors))
                return
            
            # Chuyển đổi và cập nhật
            update_data = self._convert_form_data(form_data)
            updated_member = self.member_use_case.update_member(member_id, update_data)
            
            # Làm mới danh sách
            self.refresh_data()
            
            self._update_status(f"Đã cập nhật thành viên: {updated_member.full_name}", "success")
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            self._show_error("Lỗi cập nhật thành viên", str(e))
    
    def delete_member(self):
        """Xóa thành viên"""
        try:
            member_id = MemberActions.get_selected_member_id(self.member_tree, enhanced_mode=True)
            if not member_id:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn thành viên cần xóa")
                return
            
            # Lấy thông tin thành viên
            member = self.member_use_case.get_member_by_id(member_id)
            if not member:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin thành viên")
                return
            
            # Xác nhận xóa
            result = messagebox.askyesno(
                "Xác nhận xóa", 
                f"Bạn có chắc chắn muốn xóa thành viên '{member.full_name}'?\n\nHành động này không thể hoàn tác!"
            )
            
            if result:
                self.member_use_case.delete_member(member_id)
                self.refresh_data()
                self._update_status(f"Đã xóa thành viên: {member.full_name}", "success")
            
        except Exception as e:
            self._show_error("Lỗi xóa thành viên", str(e))
    
    def view_member(self):
        """Xem chi tiết thành viên"""
        try:
            member_id = MemberActions.get_selected_member_id(self.member_tree, enhanced_mode=True)
            if not member_id:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn thành viên để xem chi tiết")
                return
            
            # Lấy thông tin thành viên
            member = self.member_use_case.get_member_by_id(member_id)
            if not member:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin thành viên")
                return
            
            # Chuyển đổi sang dictionary để hiển thị
            member_data = self._convert_member_to_display_data(member)
            
            # Hiển thị chi tiết
            MemberActions.show_member_details(self.parent, member_data)
            
        except Exception as e:
            self._show_error("Lỗi xem chi tiết thành viên", str(e))
    
    def search_members(self, event=None):
        """Tìm kiếm thành viên"""
        try:
            search_term = self.search_var.get().strip()
            
            if not search_term or search_term == "Tìm kiếm thành viên...":
                # Hiển thị tất cả
                self.filtered_members = self.all_members.copy()
            else:
                # Tìm kiếm
                self.filtered_members = self.member_use_case.search_members(search_term)
            
            # Áp dụng filter nếu có
            self._apply_current_filters()
            
            # Cập nhật bảng
            MemberActions.populate_member_tree(self.member_tree, self.filtered_members, enhanced_mode=True)
            
            self._update_status(f"Tìm thấy {len(self.filtered_members)} thành viên", "info")
            
        except Exception as e:
            self._show_error("Lỗi tìm kiếm", str(e))
    
    def filter_members(self):
        """Áp dụng bộ lọc nâng cao"""
        try:
            self._apply_current_filters()
            MemberActions.populate_member_tree(self.member_tree, self.filtered_members, enhanced_mode=True)
            self._update_status(f"Hiển thị {len(self.filtered_members)} thành viên sau khi lọc", "info")
            
        except Exception as e:
            self._show_error("Lỗi áp dụng bộ lọc", str(e))
    
    def bulk_action(self, action: str):
        """Thực hiện thao tác hàng loạt"""
        try:
            selected_ids = MemberActions.get_selected_member_ids(self.member_tree, enhanced_mode=True)
            
            if not selected_ids:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một thành viên")
                return
            
            if action == 'activate':
                self._bulk_update_status(selected_ids, MemberStatus.ACTIVE, "kích hoạt")
            elif action == 'deactivate':
                self._bulk_update_status(selected_ids, MemberStatus.INACTIVE, "tạm ngưng")
            elif action == 'delete':
                self._bulk_delete(selected_ids)
            
        except Exception as e:
            self._show_error(f"Lỗi thao tác hàng loạt", str(e))
    
    def export_members(self):
        """Xuất danh sách thành viên"""
        try:
            if not self.filtered_members:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất")
                return
            
            filename = filedialog.asksaveasfilename(
                parent=self.parent,
                title="Xuất danh sách thành viên",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                MemberExport.export_to_csv(self.parent, self.filtered_members, filename)
                self._update_status(f"Đã xuất {len(self.filtered_members)} thành viên", "success")
            
        except Exception as e:
            self._show_error("Lỗi xuất file", str(e))
    
    def _apply_current_filters(self):
        """Áp dụng các bộ lọc hiện tại"""
        MemberActions.apply_filters(
            self.member_tree, 
            self.all_members, 
            self.filter_vars, 
            enhanced_mode=True
        )
        
        # Cập nhật filtered_members dựa trên kết quả hiển thị
        self.filtered_members = []
        for item in self.member_tree.get_children():
            values = self.member_tree.item(item)['values']
            if len(values) > 1 and values[1]:  # Có ID
                member_id = int(values[1])
                member = next((m for m in self.all_members if m.id == member_id), None)
                if member:
                    self.filtered_members.append(member)
    
    def _bulk_update_status(self, member_ids: List[int], new_status: MemberStatus, action_name: str):
        """Cập nhật trạng thái hàng loạt"""
        result = messagebox.askyesno(
            "Xác nhận", 
            f"Bạn có chắc chắn muốn {action_name} {len(member_ids)} thành viên được chọn?"
        )
        
        if result:
            updated_count = self.member_use_case.bulk_update_member_status(member_ids, new_status)
            self.refresh_data()
            self._update_status(f"Đã {action_name} {updated_count} thành viên", "success")
    
    def _bulk_delete(self, member_ids: List[int]):
        """Xóa hàng loạt"""
        result = messagebox.askyesno(
            "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa {len(member_ids)} thành viên được chọn?\n\nHành động này không thể hoàn tác!"
        )
        
        if result:
            deleted_count = 0
            for member_id in member_ids:
                try:
                    self.member_use_case.delete_member(member_id)
                    deleted_count += 1
                except Exception:
                    continue
            
            self.refresh_data()
            self._update_status(f"Đã xóa {deleted_count} thành viên", "success")
    
    def _convert_form_data(self, form_data: Dict) -> Dict:
        """Chuyển đổi dữ liệu từ form sang format phù hợp cho use case"""
        import datetime
        
        # Mapping cho member type
        member_type_mapping = {
            "Đoàn viên": MemberType.UNION_MEMBER,
            "Hội viên": MemberType.ASSOCIATION_MEMBER,
            "Ban chấp hành": MemberType.EXECUTIVE
        }
        
        # Mapping cho status
        status_mapping = {
            "Đang hoạt động": MemberStatus.ACTIVE,
            "Tạm ngưng": MemberStatus.INACTIVE,
            "Đình chỉ": MemberStatus.SUSPENDED
        }
        
        converted_data = form_data.copy()
        
        # Chuyển đổi member_type
        if 'member_type' in converted_data:
            converted_data['member_type'] = member_type_mapping.get(
                converted_data['member_type'], MemberType.UNION_MEMBER
            )
        
        # Chuyển đổi status
        if 'status' in converted_data:
            converted_data['status'] = status_mapping.get(
                converted_data['status'], MemberStatus.ACTIVE
            )
        
        # Chuyển đổi date fields - convert empty string to None
        date_fields = ['date_of_birth', 'join_date']
        for field in date_fields:
            if field in converted_data:
                date_value = converted_data[field]
                if not date_value:
                    # None hoặc empty -> None (NULL trong database)
                    converted_data[field] = None
                elif isinstance(date_value, str):
                    # Nếu là string, kiểm tra và parse
                    date_str = date_value.strip()
                    if not date_str:
                        converted_data[field] = None
                    else:
                        try:
                            # Parse dd/mm/yyyy format
                            parsed_date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
                            converted_data[field] = parsed_date.date()
                        except ValueError:
                            # Nếu parse lỗi, set về None
                            converted_data[field] = None
                elif isinstance(date_value, datetime.datetime):
                    # Nếu đã là datetime, convert về date
                    converted_data[field] = date_value.date()
                elif isinstance(date_value, datetime.date):
                    # Nếu đã là date, giữ nguyên
                    converted_data[field] = date_value
        
        return converted_data
    
    def _convert_member_to_form_data(self, member: Member) -> Dict:
        """Chuyển đổi Member entity sang dữ liệu form"""
        # Mapping ngược cho hiển thị
        member_type_display = {
            MemberType.UNION_MEMBER: "Đoàn viên",
            MemberType.ASSOCIATION_MEMBER: "Hội viên",
            MemberType.EXECUTIVE: "Ban chấp hành"
        }
        
        status_display = {
            MemberStatus.ACTIVE: "Đang hoạt động",
            MemberStatus.INACTIVE: "Tạm ngưng",
            MemberStatus.SUSPENDED: "Đình chỉ"
        }
        
        return {
            'member_code': member.member_code,
            'full_name': member.full_name,
            'date_of_birth': member.date_of_birth.strftime('%d/%m/%Y') if member.date_of_birth else '',
            'gender': member.gender,
            'phone': member.phone,
            'email': member.email,
            'address': member.address,
            'position': member.position,
            'department': member.department,
            'member_type': member_type_display.get(member.member_type, "Đoàn viên"),
            'status': status_display.get(member.status, "Đang hoạt động"),
            'join_date': member.join_date.strftime('%d/%m/%Y') if member.join_date else '',
            'notes': member.notes
        }
    
    def _convert_member_to_display_data(self, member: Member) -> Dict:
        """Chuyển đổi Member entity sang dữ liệu hiển thị"""
        return {
            'member_code': member.member_code,
            'full_name': member.full_name,
            'date_of_birth': member.date_of_birth.strftime('%d/%m/%Y') if member.date_of_birth else 'N/A',
            'gender': member.gender or 'N/A',
            'phone': member.phone or 'N/A',
            'email': member.email or 'N/A',
            'address': member.address or 'N/A',
            'position': member.position or 'N/A',
            'department': member.department or 'N/A',
            'member_type': member.get_member_type_display() if hasattr(member, 'get_member_type_display') else str(member.member_type),
            'status': member.get_status_display() if hasattr(member, 'get_status_display') else str(member.status),
            'join_date': member.join_date.strftime('%d/%m/%Y') if member.join_date else 'N/A',
            'notes': member.notes or 'N/A'
        }
    
    def _update_statistics(self, stats: Dict):
        """Cập nhật panel thống kê"""
        if hasattr(self.member_frame, 'stats_panel'):
            # Xóa panel cũ
            self.member_frame.stats_panel.destroy()
            
            # Tạo panel mới với dữ liệu cập nhật
            self.member_frame.stats_panel = MemberStats.create_stats_panel(
                self.member_frame.winfo_children()[1],  # content_frame
                stats
            )
    
    def _update_status(self, message: str, message_type: str = "info"):
        """Cập nhật thanh trạng thái"""
        if self.status_label:
            MemberActions.update_status_bar(self.status_label, message, message_type)
    
    def _show_error(self, title: str, message: str):
        """Hiển thị lỗi với chi tiết"""
        error_details = f"{message}\n\nChi tiết lỗi:\n{traceback.format_exc()}"
        messagebox.showerror(title, message)
        print(f"ERROR: {title} - {error_details}")  # Log để debug
    
    def get_main_frame(self) -> tk.Frame:
        """Lấy frame chính của component"""
        return self.member_frame