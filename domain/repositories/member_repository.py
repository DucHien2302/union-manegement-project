from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.member import Member, MemberType, MemberStatus


class IMemberRepository(ABC):
    """Interface cho Member Repository"""
    
    @abstractmethod
    def create(self, member: Member) -> Member:
        """Tạo thành viên mới"""
        pass
    
    @abstractmethod
    def get_by_id(self, member_id: int) -> Optional[Member]:
        """Lấy thành viên theo ID"""
        pass
    
    @abstractmethod
    def get_by_member_code(self, member_code: str) -> Optional[Member]:
        """Lấy thành viên theo mã thành viên"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Member]:
        """Lấy tất cả thành viên"""
        pass
    
    @abstractmethod
    def get_by_type(self, member_type: MemberType) -> List[Member]:
        """Lấy thành viên theo loại"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: MemberStatus) -> List[Member]:
        """Lấy thành viên theo trạng thái"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Member]:
        """Tìm kiếm thành viên theo tên"""
        pass
    
    @abstractmethod
    def update(self, member: Member) -> Member:
        """Cập nhật thông tin thành viên"""
        pass
    
    @abstractmethod
    def delete(self, member_id: int) -> bool:
        """Xóa thành viên"""
        pass
    
    @abstractmethod
    def count_by_type(self, member_type: MemberType) -> int:
        """Đếm số thành viên theo loại"""
        pass