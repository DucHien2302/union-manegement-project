from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.report import Report, ReportType, ReportStatus


class IReportRepository(ABC):
    """Interface cho Report Repository"""
    
    @abstractmethod
    def create(self, report: Report) -> Report:
        """Tạo báo cáo mới"""
        pass
    
    @abstractmethod
    def get_by_id(self, report_id: int) -> Optional[Report]:
        """Lấy báo cáo theo ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Report]:
        """Lấy tất cả báo cáo"""
        pass
    
    @abstractmethod
    def get_by_type(self, report_type: ReportType) -> List[Report]:
        """Lấy báo cáo theo loại"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: ReportStatus) -> List[Report]:
        """Lấy báo cáo theo trạng thái"""
        pass
    
    @abstractmethod
    def get_by_period(self, period: str) -> List[Report]:
        """Lấy báo cáo theo kỳ"""
        pass
    
    @abstractmethod
    def get_by_submitter(self, submitter_id: int) -> List[Report]:
        """Lấy báo cáo theo người nộp"""
        pass
    
    @abstractmethod
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Report]:
        """Lấy báo cáo trong khoảng thời gian"""
        pass
    
    @abstractmethod
    def search_by_title(self, title: str) -> List[Report]:
        """Tìm kiếm báo cáo theo tiêu đề"""
        pass
    
    @abstractmethod
    def update(self, report: Report) -> Report:
        """Cập nhật báo cáo"""
        pass
    
    @abstractmethod
    def delete(self, report_id: int) -> bool:
        """Xóa báo cáo"""
        pass
    
    @abstractmethod
    def count_by_status(self, status: ReportStatus) -> int:
        """Đếm số báo cáo theo trạng thái"""
        pass