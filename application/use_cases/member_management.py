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