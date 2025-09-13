from typing import List, Optional
from datetime import datetime
from domain.entities.member import Member, MemberType, MemberStatus
from domain.repositories.member_repository import IMemberRepository


class MemberManagementUseCase:
    """Use case cho quản lý thành viên"""
    
    def __init__(self, member_repository: IMemberRepository):
        self.member_repository = member_repository
    
    def create_member(self, member_data: dict) -> Member:
        """Tạo thành viên mới"""
        # Kiểm tra mã thành viên đã tồn tại chưa
        existing_member = self.member_repository.get_by_member_code(member_data.get('member_code', ''))
        if existing_member:
            raise ValueError(f"Mã thành viên '{member_data['member_code']}' đã tồn tại")
        
        # Tạo entity Member
        member = Member(
            member_code=member_data.get('member_code', ''),
            full_name=member_data.get('full_name', ''),
            date_of_birth=member_data.get('date_of_birth'),
            gender=member_data.get('gender', ''),
            phone=member_data.get('phone', ''),
            email=member_data.get('email', ''),
            address=member_data.get('address', ''),
            position=member_data.get('position', ''),
            department=member_data.get('department', ''),
            member_type=member_data.get('member_type', MemberType.UNION_MEMBER),
            status=member_data.get('status', MemberStatus.ACTIVE),
            join_date=member_data.get('join_date', datetime.now()),
            notes=member_data.get('notes', '')
        )
        
        return self.member_repository.create(member)
    
    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """Lấy thông tin thành viên theo ID"""
        return self.member_repository.get_by_id(member_id)
    
    def get_member_by_code(self, member_code: str) -> Optional[Member]:
        """Lấy thông tin thành viên theo mã"""
        return self.member_repository.get_by_member_code(member_code)
    
    def get_all_members(self) -> List[Member]:
        """Lấy danh sách tất cả thành viên"""
        return self.member_repository.get_all()
    
    def get_members_by_type(self, member_type: MemberType) -> List[Member]:
        """Lấy danh sách thành viên theo loại"""
        return self.member_repository.get_by_type(member_type)
    
    def get_active_members(self) -> List[Member]:
        """Lấy danh sách thành viên đang hoạt động"""
        return self.member_repository.get_by_status(MemberStatus.ACTIVE)
    
    def search_members_by_name(self, name: str) -> List[Member]:
        """Tìm kiếm thành viên theo tên"""
        return self.member_repository.search_by_name(name)
    
    def update_member(self, member_id: int, update_data: dict) -> Member:
        """Cập nhật thông tin thành viên"""
        existing_member = self.member_repository.get_by_id(member_id)
        if not existing_member:
            raise ValueError(f"Không tìm thấy thành viên với ID {member_id}")
        
        # Kiểm tra nếu mã thành viên bị thay đổi và đã tồn tại
        new_member_code = update_data.get('member_code')
        if new_member_code and new_member_code != existing_member.member_code:
            existing_code_member = self.member_repository.get_by_member_code(new_member_code)
            if existing_code_member:
                raise ValueError(f"Mã thành viên '{new_member_code}' đã tồn tại")
        
        # Cập nhật các thuộc tính
        for key, value in update_data.items():
            if hasattr(existing_member, key):
                setattr(existing_member, key, value)
        
        existing_member.updated_at = datetime.now()
        return self.member_repository.update(existing_member)
    
    def deactivate_member(self, member_id: int, reason: str = "") -> Member:
        """Tạm ngưng hoạt động của thành viên"""
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError(f"Không tìm thấy thành viên với ID {member_id}")
        
        member.status = MemberStatus.INACTIVE
        if reason:
            member.notes += f"\nTạm ngưng: {reason} ({datetime.now().strftime('%d/%m/%Y')})"
        member.updated_at = datetime.now()
        
        return self.member_repository.update(member)
    
    def activate_member(self, member_id: int) -> Member:
        """Kích hoạt lại thành viên"""
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError(f"Không tìm thấy thành viên với ID {member_id}")
        
        member.status = MemberStatus.ACTIVE
        member.notes += f"\nKích hoạt lại: {datetime.now().strftime('%d/%m/%Y')}"
        member.updated_at = datetime.now()
        
        return self.member_repository.update(member)
    
    def delete_member(self, member_id: int) -> bool:
        """Xóa thành viên"""
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError(f"Không tìm thấy thành viên với ID {member_id}")
        
        return self.member_repository.delete(member_id)
    
    def get_member_statistics(self) -> dict:
        """Lấy thống kê thành viên"""
        total_members = len(self.member_repository.get_all())
        union_members = self.member_repository.count_by_type(MemberType.UNION_MEMBER)
        association_members = self.member_repository.count_by_type(MemberType.ASSOCIATION_MEMBER)
        executives = self.member_repository.count_by_type(MemberType.EXECUTIVE)
        active_members = len(self.member_repository.get_by_status(MemberStatus.ACTIVE))
        inactive_members = len(self.member_repository.get_by_status(MemberStatus.INACTIVE))
        
        return {
            'total': total_members,
            'union_members': union_members,
            'association_members': association_members,
            'executives': executives,
            'active': active_members,
            'inactive': inactive_members
        }
    
    def get_members_by_department(self, department: str) -> List[Member]:
        """Lấy danh sách thành viên theo phòng ban"""
        return self.member_repository.get_members_by_department(department)
    
    def get_paginated_members(self, page: int = 1, page_size: int = 20) -> tuple[List[Member], int]:
        """Lấy danh sách thành viên có phân trang"""
        if hasattr(self.member_repository, 'get_paginated_members'):
            return self.member_repository.get_paginated_members(page, page_size)
        
        # Fallback nếu repository chưa có phương thức này
        all_members = self.get_all_members()
        total = len(all_members)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        return all_members[start_idx:end_idx], total
    
    def search_members(self, search_term: str, search_fields: List[str] = None) -> List[Member]:
        """Tìm kiếm thành viên theo nhiều trường"""
        if hasattr(self.member_repository, 'search_members'):
            return self.member_repository.search_members(search_term, search_fields)
        
        # Fallback sử dụng search_by_name
        return self.search_members_by_name(search_term)
    
    def validate_member_data(self, member_data: dict) -> List[str]:
        """Kiểm tra tính hợp lệ của dữ liệu thành viên"""
        errors = []
        
        # Kiểm tra các trường bắt buộc
        required_fields = ['member_code', 'full_name']
        for field in required_fields:
            if not member_data.get(field, '').strip():
                errors.append(f"Trường '{field}' không được để trống")
        
        # Kiểm tra email
        email = member_data.get('email', '')
        if email and '@' not in email:
            errors.append("Email không hợp lệ")
        
        # Kiểm tra phone
        phone = member_data.get('phone', '')
        if phone and not phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '').isdigit():
            errors.append("Số điện thoại không hợp lệ")
        
        return errors
    
    def bulk_update_member_status(self, member_ids: List[int], new_status: MemberStatus) -> int:
        """Cập nhật trạng thái hàng loạt"""
        if hasattr(self.member_repository, 'bulk_update_status'):
            return self.member_repository.bulk_update_status(member_ids, new_status)
        
        # Fallback - cập nhật từng thành viên
        updated_count = 0
        for member_id in member_ids:
            try:
                member = self.get_member_by_id(member_id)
                if member:
                    member.status = new_status
                    member.updated_at = datetime.now()
                    self.member_repository.update(member)
                    updated_count += 1
            except Exception:
                continue
        
        return updated_count
    
    def export_members_data(self, filters: dict = None) -> List[dict]:
        """Xuất dữ liệu thành viên để export"""
        if filters:
            # Áp dụng các bộ lọc nếu có
            members = self.get_all_members()  # Có thể cải thiện với filter cụ thể
        else:
            members = self.get_all_members()
        
        export_data = []
        for member in members:
            export_data.append({
                'Mã thành viên': member.member_code,
                'Họ tên': member.full_name,
                'Ngày sinh': member.date_of_birth.strftime('%d/%m/%Y') if member.date_of_birth else '',
                'Giới tính': member.gender,
                'Số điện thoại': member.phone,
                'Email': member.email,
                'Địa chỉ': member.address,
                'Chức vụ': member.position,
                'Phòng ban': member.department,
                'Loại thành viên': member.get_member_type_display(),
                'Trạng thái': member.get_status_display(),
                'Ngày tham gia': member.join_date.strftime('%d/%m/%Y') if member.join_date else '',
                'Ghi chú': member.notes
            })
        
        return export_data