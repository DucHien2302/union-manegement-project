from typing import List, Optional
from datetime import datetime
from domain.entities.report import Report, ReportType, ReportStatus
from domain.repositories.report_repository import IReportRepository


class ReportManagementUseCase:
    """Use case cho quản lý báo cáo"""
    
    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository
    
    def create_report(self, report_data: dict) -> Report:
        """Tạo báo cáo mới"""
        report = Report(
            title=report_data.get('title', ''),
            report_type=report_data.get('report_type', ReportType.MONTHLY),
            period=report_data.get('period', ''),
            content=report_data.get('content', ''),
            attachments=report_data.get('attachments', ''),
            status=ReportStatus.DRAFT,
            submitted_by=report_data.get('submitted_by')
        )
        
        return self.report_repository.create(report)
    
    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """Lấy báo cáo theo ID"""
        return self.report_repository.get_by_id(report_id)
    
    def get_all_reports(self) -> List[Report]:
        """Lấy tất cả báo cáo"""
        return self.report_repository.get_all()
    
    def get_reports_by_type(self, report_type: ReportType) -> List[Report]:
        """Lấy báo cáo theo loại"""
        return self.report_repository.get_by_type(report_type)
    
    def get_reports_by_status(self, status: ReportStatus) -> List[Report]:
        """Lấy báo cáo theo trạng thái"""
        return self.report_repository.get_by_status(status)
    
    def get_reports_by_period(self, period: str) -> List[Report]:
        """Lấy báo cáo theo kỳ"""
        return self.report_repository.get_by_period(period)
    
    def get_reports_by_submitter(self, submitter_id: int) -> List[Report]:
        """Lấy báo cáo theo người nộp"""
        return self.report_repository.get_by_submitter(submitter_id)
    
    def get_draft_reports(self) -> List[Report]:
        """Lấy các báo cáo nháp"""
        return self.report_repository.get_by_status(ReportStatus.DRAFT)
    
    def get_pending_reports(self) -> List[Report]:
        """Lấy các báo cáo chờ duyệt"""
        return self.report_repository.get_by_status(ReportStatus.SUBMITTED)
    
    def search_reports_by_title(self, title: str) -> List[Report]:
        """Tìm kiếm báo cáo theo tiêu đề"""
        return self.report_repository.search_by_title(title)
    
    def update_report(self, report_id: int, update_data: dict) -> Report:
        """Cập nhật báo cáo"""
        existing_report = self.report_repository.get_by_id(report_id)
        if not existing_report:
            raise ValueError(f"Không tìm thấy báo cáo với ID {report_id}")
        
        # Kiểm tra báo cáo có thể chỉnh sửa không
        if not existing_report.is_editable():
            raise ValueError("Báo cáo này không thể chỉnh sửa")
        
        # Cập nhật các thuộc tính
        for key, value in update_data.items():
            if hasattr(existing_report, key) and key not in ['id', 'created_at']:
                setattr(existing_report, key, value)
        
        existing_report.updated_at = datetime.now()
        return self.report_repository.update(existing_report)
    
    def submit_report(self, report_id: int, submitted_by_id: int) -> Report:
        """Nộp báo cáo"""
        report = self.report_repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Không tìm thấy báo cáo với ID {report_id}")
        
        if report.status != ReportStatus.DRAFT:
            raise ValueError("Chỉ có thể nộp báo cáo ở trạng thái nháp")
        
        report.submit(submitted_by_id)
        return self.report_repository.update(report)
    
    def approve_report(self, report_id: int, approved_by_id: int) -> Report:
        """Duyệt báo cáo"""
        report = self.report_repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Không tìm thấy báo cáo với ID {report_id}")
        
        if report.status != ReportStatus.SUBMITTED:
            raise ValueError("Chỉ có thể duyệt báo cáo ở trạng thái đã nộp")
        
        report.approve(approved_by_id)
        return self.report_repository.update(report)
    
    def reject_report(self, report_id: int, approved_by_id: int, reason: str) -> Report:
        """Từ chối báo cáo"""
        report = self.report_repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Không tìm thấy báo cáo với ID {report_id}")
        
        if report.status != ReportStatus.SUBMITTED:
            raise ValueError("Chỉ có thể từ chối báo cáo ở trạng thái đã nộp")
        
        report.reject(approved_by_id, reason)
        return self.report_repository.update(report)
    
    def delete_report(self, report_id: int) -> bool:
        """Xóa báo cáo"""
        report = self.report_repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Không tìm thấy báo cáo với ID {report_id}")
        
        # Chỉ cho phép xóa báo cáo nháp hoặc bị từ chối
        if report.status not in [ReportStatus.DRAFT, ReportStatus.REJECTED]:
            raise ValueError("Chỉ có thể xóa báo cáo ở trạng thái nháp hoặc bị từ chối")
        
        return self.report_repository.delete(report_id)
    
    def get_report_statistics(self) -> dict:
        """Lấy thống kê báo cáo"""
        total_reports = len(self.report_repository.get_all())
        draft_reports = self.report_repository.count_by_status(ReportStatus.DRAFT)
        submitted_reports = self.report_repository.count_by_status(ReportStatus.SUBMITTED)
        approved_reports = self.report_repository.count_by_status(ReportStatus.APPROVED)
        rejected_reports = self.report_repository.count_by_status(ReportStatus.REJECTED)
        
        return {
            'total': total_reports,
            'draft': draft_reports,
            'submitted': submitted_reports,
            'approved': approved_reports,
            'rejected': rejected_reports,
            'approval_rate': (approved_reports / (approved_reports + rejected_reports) * 100) 
                           if (approved_reports + rejected_reports) > 0 else 0
        }
    
    def get_reports_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Report]:
        """Lấy báo cáo trong khoảng thời gian"""
        return self.report_repository.get_by_date_range(start_date, end_date)