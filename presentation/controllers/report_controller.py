"""
Report Controller
Xử lý tương tác giữa GUI và business logic cho quản lý báo cáo
"""

from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from tkinter import messagebox

from domain.entities.report import Report, ReportType, ReportStatus
from application.use_cases.report_management import ReportManagementUseCase
from infrastructure.repositories.report_repository_impl import ReportRepository
from config.logging_config import setup_logging

# Thiết lập logging
setup_logging()
logger = logging.getLogger(__name__)


class ReportController:
    """Controller cho quản lý báo cáo"""
    
    def __init__(self, report_use_case: ReportManagementUseCase = None):
        """Khởi tạo controller"""
        if report_use_case:
            self.report_use_case = report_use_case
        else:
            # Fallback to create use case internally
            self.report_repository = ReportRepository()
            self.report_use_case = ReportManagementUseCase(self.report_repository)
        logger.info("ReportController khởi tạo thành công")
    
    def get_all_reports(self) -> List[Report]:
        """Lấy tất cả báo cáo"""
        try:
            reports = self.report_use_case.get_all_reports()
            logger.info(f"Lấy được {len(reports)} báo cáo")
            return reports
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách báo cáo: {e}")
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách báo cáo: {e}")
            return []
    
    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """Lấy báo cáo theo ID"""
        try:
            report = self.report_use_case.get_report_by_id(report_id)
            if report:
                logger.info(f"Lấy báo cáo ID {report_id} thành công")
            else:
                logger.warning(f"Không tìm thấy báo cáo ID {report_id}")
            return report
        except Exception as e:
            logger.error(f"Lỗi khi lấy báo cáo ID {report_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin báo cáo: {e}")
            return None
    
    def create_report(self, report_data: Dict[str, Any]) -> bool:
        """Tạo báo cáo mới"""
        try:
            # Validate dữ liệu đầu vào
            if not self._validate_report_data(report_data):
                return False
            
            # Chuyển đổi dữ liệu
            processed_data = self._process_report_data(report_data)
            
            # Tạo báo cáo
            report = self.report_use_case.create_report(processed_data)
            
            logger.info(f"Tạo báo cáo mới thành công: ID {report.id}")
            messagebox.showinfo("Thành công", "Tạo báo cáo thành công!")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi tạo báo cáo: {e}")
            messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {e}")
            return False
    
    def update_report(self, report_id: int, report_data: Dict[str, Any]) -> bool:
        """Cập nhật báo cáo"""
        try:
            # Validate dữ liệu đầu vào
            if not self._validate_report_data(report_data):
                return False
            
            # Chuyển đổi dữ liệu
            processed_data = self._process_report_data(report_data)
            
            # Cập nhật báo cáo
            report = self.report_use_case.update_report(report_id, processed_data)
            
            logger.info(f"Cập nhật báo cáo ID {report_id} thành công")
            messagebox.showinfo("Thành công", "Cập nhật báo cáo thành công!")
            return True
            
        except ValueError as e:
            logger.warning(f"Lỗi validation khi cập nhật báo cáo ID {report_id}: {e}")
            messagebox.showwarning("Cảnh báo", str(e))
            return False
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật báo cáo ID {report_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể cập nhật báo cáo: {e}")
            return False
    
    def delete_report(self, report_id: int) -> bool:
        """Xóa báo cáo"""
        try:
            # Xác nhận xóa
            result = messagebox.askyesno(
                "Xác nhận", 
                "Bạn có chắc chắn muốn xóa báo cáo này?"
            )
            if not result:
                return False
            
            # Xóa báo cáo
            success = self.report_use_case.delete_report(report_id)
            
            if success:
                logger.info(f"Xóa báo cáo ID {report_id} thành công")
                messagebox.showinfo("Thành công", "Xóa báo cáo thành công!")
                return True
            else:
                logger.warning(f"Không thể xóa báo cáo ID {report_id}")
                return False
                
        except ValueError as e:
            logger.warning(f"Lỗi validation khi xóa báo cáo ID {report_id}: {e}")
            messagebox.showwarning("Cảnh báo", str(e))
            return False
        except Exception as e:
            logger.error(f"Lỗi khi xóa báo cáo ID {report_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể xóa báo cáo: {e}")
            return False
    
    def submit_report(self, report_id: int, submitted_by_id: int) -> bool:
        """Nộp báo cáo"""
        try:
            report = self.report_use_case.submit_report(report_id, submitted_by_id)
            
            logger.info(f"Nộp báo cáo ID {report_id} thành công")
            messagebox.showinfo("Thành công", "Nộp báo cáo thành công!")
            return True
            
        except ValueError as e:
            logger.warning(f"Lỗi validation khi nộp báo cáo ID {report_id}: {e}")
            messagebox.showwarning("Cảnh báo", str(e))
            return False
        except Exception as e:
            logger.error(f"Lỗi khi nộp báo cáo ID {report_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể nộp báo cáo: {e}")
            return False
    
    def approve_report(self, report_id: int, approved_by_id: int) -> bool:
        """Duyệt báo cáo"""
        try:
            report = self.report_use_case.approve_report(report_id, approved_by_id)
            
            logger.info(f"Duyệt báo cáo ID {report_id} thành công")
            messagebox.showinfo("Thành công", "Duyệt báo cáo thành công!")
            return True
            
        except ValueError as e:
            logger.warning(f"Lỗi validation khi duyệt báo cáo ID {report_id}: {e}")
            messagebox.showwarning("Cảnh báo", str(e))
            return False
        except Exception as e:
            logger.error(f"Lỗi khi duyệt báo cáo ID {report_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể duyệt báo cáo: {e}")
            return False
    
    def reject_report(self, report_id: int, approved_by_id: int, reason: str) -> bool:
        """Từ chối báo cáo"""
        try:
            if not reason.strip():
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập lý do từ chối!")
                return False
            
            report = self.report_use_case.reject_report(report_id, approved_by_id, reason)
            
            logger.info(f"Từ chối báo cáo ID {report_id} thành công")
            messagebox.showinfo("Thành công", "Từ chối báo cáo thành công!")
            return True
            
        except ValueError as e:
            logger.warning(f"Lỗi validation khi từ chối báo cáo ID {report_id}: {e}")
            messagebox.showwarning("Cảnh báo", str(e))
            return False
        except Exception as e:
            logger.error(f"Lỗi khi từ chối báo cáo ID {report_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể từ chối báo cáo: {e}")
            return False
    
    def get_reports_by_status(self, status: ReportStatus) -> List[Report]:
        """Lấy báo cáo theo trạng thái"""
        try:
            reports = self.report_use_case.get_reports_by_status(status)
            logger.info(f"Lấy được {len(reports)} báo cáo với trạng thái {status}")
            return reports
        except Exception as e:
            logger.error(f"Lỗi khi lấy báo cáo theo trạng thái {status}: {e}")
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách báo cáo: {e}")
            return []
    
    def get_reports_by_type(self, report_type: ReportType) -> List[Report]:
        """Lấy báo cáo theo loại"""
        try:
            reports = self.report_use_case.get_reports_by_type(report_type)
            logger.info(f"Lấy được {len(reports)} báo cáo loại {report_type}")
            return reports
        except Exception as e:
            logger.error(f"Lỗi khi lấy báo cáo theo loại {report_type}: {e}")
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách báo cáo: {e}")
            return []
    
    def search_reports(self, title: str) -> List[Report]:
        """Tìm kiếm báo cáo theo tiêu đề"""
        try:
            if not title.strip():
                return self.get_all_reports()
            
            reports = self.report_use_case.search_reports_by_title(title)
            logger.info(f"Tìm kiếm '{title}' - tìm được {len(reports)} báo cáo")
            return reports
        except Exception as e:
            logger.error(f"Lỗi khi tìm kiếm báo cáo với từ khóa '{title}': {e}")
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm báo cáo: {e}")
            return []
    
    def get_report_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê báo cáo"""
        try:
            stats = self.report_use_case.get_report_statistics()
            logger.info("Lấy thống kê báo cáo thành công")
            return stats
        except Exception as e:
            logger.error(f"Lỗi khi lấy thống kê báo cáo: {e}")
            messagebox.showerror("Lỗi", f"Không thể lấy thống kê báo cáo: {e}")
            return {}
    
    def _validate_report_data(self, data: Dict[str, Any]) -> bool:
        """Validate dữ liệu báo cáo"""
        # Kiểm tra các trường bắt buộc
        if not data.get('title', '').strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tiêu đề báo cáo!")
            return False
        
        if not data.get('period', '').strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập kỳ báo cáo!")
            return False
        
        if not data.get('content', '').strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung báo cáo!")
            return False
        
        return True
    
    def _process_report_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Xử lý và chuyển đổi dữ liệu báo cáo"""
        processed_data = {}
        
        # Chuyển đổi loại báo cáo từ string sang enum - Xử lý cả emoji version và plain text
        report_type_mapping = {
            "📅 Báo cáo tháng": ReportType.MONTHLY,
            "Báo cáo tháng": ReportType.MONTHLY,
            "monthly": ReportType.MONTHLY,
            "📈 Báo cáo quý": ReportType.QUARTERLY,
            "Báo cáo quý": ReportType.QUARTERLY,
            "quarterly": ReportType.QUARTERLY,
            "📋 Báo cáo năm": ReportType.ANNUAL,
            "Báo cáo năm": ReportType.ANNUAL,
            "annual": ReportType.ANNUAL,
            "⭐ Báo cáo đặc biệt": ReportType.SPECIAL,
            "Báo cáo đặc biệt": ReportType.SPECIAL,
            "special": ReportType.SPECIAL
        }
        
        # Chuyển đổi trạng thái từ string sang enum - Xử lý cả emoji version và plain text
        status_mapping = {
            "📝 Nháp": ReportStatus.DRAFT,
            "Nháp": ReportStatus.DRAFT,
            "draft": ReportStatus.DRAFT,
            "📤 Đã nộp": ReportStatus.SUBMITTED,
            "Đã nộp": ReportStatus.SUBMITTED,
            "submitted": ReportStatus.SUBMITTED,
            "✅ Đã duyệt": ReportStatus.APPROVED,
            "Đã duyệt": ReportStatus.APPROVED,
            "approved": ReportStatus.APPROVED,
            "❌ Từ chối": ReportStatus.REJECTED,
            "Từ chối": ReportStatus.REJECTED,
            "rejected": ReportStatus.REJECTED
        }
        
        # Xử lý các trường
        processed_data['title'] = data.get('title', '').strip()
        processed_data['period'] = data.get('period', '').strip()
        processed_data['content'] = data.get('content', '').strip()
        processed_data['attachments'] = data.get('attachments', '')
        processed_data['created_by'] = data.get('created_by', 1)  # Default to user ID 1 if not specified
        
        # Xử lý report_type
        report_type_str = data.get('report_type', '📅 Báo cáo tháng')
        processed_data['report_type'] = report_type_mapping.get(report_type_str, ReportType.MONTHLY)
        
        # Xử lý status
        status_str = data.get('status', '📝 Nháp')
        processed_data['status'] = status_mapping.get(status_str, ReportStatus.DRAFT)
        
        return processed_data
    
    def format_report_data_for_display(self, report: Report) -> Dict[str, str]:
        """Chuyển đổi dữ liệu báo cáo để hiển thị trong form"""
        # Mapping ngược lại cho hiển thị - sử dụng emoji version để đồng nhất
        type_display_mapping = {
            ReportType.MONTHLY: "📅 Báo cáo tháng",
            ReportType.QUARTERLY: "📈 Báo cáo quý", 
            ReportType.ANNUAL: "📋 Báo cáo năm",
            ReportType.SPECIAL: "⭐ Báo cáo đặc biệt"
        }
        
        status_display_mapping = {
            ReportStatus.DRAFT: "📝 Nháp",
            ReportStatus.SUBMITTED: "📤 Đã nộp",
            ReportStatus.APPROVED: "✅ Đã duyệt",
            ReportStatus.REJECTED: "❌ Từ chối"
        }
        
        return {
            'title': report.title or '',
            'report_type': type_display_mapping.get(report.report_type, "📅 Báo cáo tháng"),
            'period': report.period or '',
            'status': status_display_mapping.get(report.status, "📝 Nháp"),
            'content': report.content or ''
        }