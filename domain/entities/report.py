from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ReportType(Enum):
    """Loại báo cáo"""
    MONTHLY = "monthly"  # Báo cáo tháng
    QUARTERLY = "quarterly"  # Báo cáo quý
    ANNUAL = "annual"  # Báo cáo năm
    SPECIAL = "special"  # Báo cáo đặc biệt


class ReportStatus(Enum):
    """Trạng thái báo cáo"""
    DRAFT = "draft"  # Bản nháp
    SUBMITTED = "submitted"  # Đã nộp
    APPROVED = "approved"  # Đã duyệt
    REJECTED = "rejected"  # Từ chối


@dataclass
class Report:
    """Entity cho Báo cáo"""
    id: Optional[int] = None
    title: str = ""
    report_type: ReportType = ReportType.MONTHLY
    period: str = ""  # Kỳ báo cáo (VD: 2024-01, Q1-2024)
    content: str = ""
    attachments: str = ""  # JSON string chứa danh sách file đính kèm
    status: ReportStatus = ReportStatus.DRAFT
    submitted_by: Optional[int] = None  # ID của người nộp
    submitted_at: Optional[datetime] = None
    approved_by: Optional[int] = None  # ID của người duyệt
    approved_at: Optional[datetime] = None
    rejection_reason: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def submit(self, submitted_by_id: int):
        """Nộp báo cáo"""
        self.status = ReportStatus.SUBMITTED
        self.submitted_by = submitted_by_id
        self.submitted_at = datetime.now()
        self.updated_at = datetime.now()

    def approve(self, approved_by_id: int):
        """Duyệt báo cáo"""
        self.status = ReportStatus.APPROVED
        self.approved_by = approved_by_id
        self.approved_at = datetime.now()
        self.updated_at = datetime.now()

    def reject(self, approved_by_id: int, reason: str):
        """Từ chối báo cáo"""
        self.status = ReportStatus.REJECTED
        self.approved_by = approved_by_id
        self.approved_at = datetime.now()
        self.rejection_reason = reason
        self.updated_at = datetime.now()

    def is_editable(self) -> bool:
        """Kiểm tra báo cáo có thể chỉnh sửa không"""
        return self.status in [ReportStatus.DRAFT, ReportStatus.REJECTED]