from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List


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
    
    def get_age(self) -> Optional[int]:
        """Tính tuổi từ ngày sinh"""
        if self.date_of_birth:
            today = datetime.now()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def get_status_display(self) -> str:
        """Lấy tên hiển thị trạng thái"""
        status_map = {
            MemberStatus.ACTIVE: "Đang hoạt động",
            MemberStatus.INACTIVE: "Tạm ngưng",
            MemberStatus.SUSPENDED: "Đình chỉ"
        }
        return status_map.get(self.status, "Không xác định")
    
    def get_member_type_display(self) -> str:
        """Lấy tên hiển thị loại thành viên"""
        type_map = {
            MemberType.UNION_MEMBER: "Đoàn viên",
            MemberType.ASSOCIATION_MEMBER: "Hội viên",
            MemberType.EXECUTIVE: "Ban chấp hành"
        }
        return type_map.get(self.member_type, "Không xác định")
    
    def validate(self) -> List[str]:
        """Kiểm tra tính hợp lệ của dữ liệu thành viên"""
        errors = []
        
        if not self.member_code.strip():
            errors.append("Mã thành viên không được để trống")
        
        if not self.full_name.strip():
            errors.append("Họ tên không được để trống")
        
        if self.email and "@" not in self.email:
            errors.append("Email không hợp lệ")
        
        if self.phone and not self.phone.replace(" ", "").replace("-", "").isdigit():
            errors.append("Số điện thoại không hợp lệ")
        
        if self.date_of_birth and self.date_of_birth > datetime.now():
            errors.append("Ngày sinh không thể ở tương lai")
        
        return errors
    
    def is_valid(self) -> bool:
        """Kiểm tra thành viên có hợp lệ không"""
        return len(self.validate()) == 0