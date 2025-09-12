from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class MemberType(Enum):
    """Loại thành viên"""
    UNION_MEMBER = "union_member"  # Đoàn viên
    ASSOCIATION_MEMBER = "association_member"  # Hội viên
    EXECUTIVE = "executive"  # Ban chấp hành


class MemberStatus(Enum):
    """Trạng thái thành viên"""
    ACTIVE = "active"  # Đang hoạt động
    INACTIVE = "inactive"  # Tạm ngưng
    SUSPENDED = "suspended"  # Đình chỉ


@dataclass
class Member:
    """Entity cho Đoàn viên/Hội viên"""
    id: Optional[int] = None
    member_code: str = ""
    full_name: str = ""
    date_of_birth: Optional[datetime] = None
    gender: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    position: str = ""
    department: str = ""
    member_type: MemberType = MemberType.UNION_MEMBER
    status: MemberStatus = MemberStatus.ACTIVE
    join_date: Optional[datetime] = None
    notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        """Kiểm tra thành viên có đang hoạt động không"""
        return self.status == MemberStatus.ACTIVE

    def get_display_name(self) -> str:
        """Lấy tên hiển thị với mã thành viên"""
        return f"{self.member_code} - {self.full_name}"