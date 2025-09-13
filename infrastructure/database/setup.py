"""
Database setup script cho Union Management System
Chỉ hỗ trợ PostgreSQL database
"""
import sys
import os

# Thêm thư mục gốc của project vào Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from infrastructure.database.connection import Base, db_manager
from infrastructure.database.models import MemberModel, ReportModel, TaskModel
from domain.entities.member import MemberType, MemberStatus
from domain.entities.report import ReportType, ReportStatus
from domain.entities.task import TaskPriority, TaskStatus


def create_tables():
    """Tạo các bảng trong database"""
    try:
        engine = db_manager.get_engine()
        
        # Tạo tất cả các bảng
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def drop_tables():
    """Xóa tất cả các bảng (sử dụng cẩn thận!)"""
    try:
        engine = db_manager.get_engine()
        
        # Xóa tất cả các bảng
        Base.metadata.drop_all(engine)
        print("⚠️ All tables dropped!")
        return True
        
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return False


def insert_sample_members():
    """Thêm dữ liệu mẫu cho bảng members"""
    try:
        engine = db_manager.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Kiểm tra xem đã có dữ liệu chưa
        existing_count = session.query(MemberModel).count()
        if existing_count > 0:
            print(f"📊 Members table already has {existing_count} records. Skipping sample data insertion.")
            session.close()
            return True
        
        sample_members = [
            MemberModel(
                member_code="DV001",
                full_name="Nguyễn Văn An",
                date_of_birth=datetime(1985, 3, 15),
                gender="Nam",
                phone="0912345678",
                email="an.nguyen@company.com",
                address="123 Đường Lê Lợi, Quận 1, TP.HCM",
                position="Trưởng phòng Kế toán",
                department="Phòng Kế toán",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2020, 1, 15),
                notes="Thành viên tích cực, có kinh nghiệm làm việc 10 năm"
            ),
            MemberModel(
                member_code="DV002",
                full_name="Trần Thị Bình",
                date_of_birth=datetime(1990, 7, 22),
                gender="Nữ",
                phone="0987654321",
                email="binh.tran@company.com",
                address="456 Đường Nguyễn Huệ, Quận 3, TP.HCM",
                position="Chuyên viên Nhân sự",
                department="Phòng Nhân sự",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2021, 3, 10),
                notes="Nhiệt tình tham gia các hoạt động đoàn thể"
            ),
            MemberModel(
                member_code="HV001",
                full_name="Lê Minh Cường",
                date_of_birth=datetime(1982, 11, 8),
                gender="Nam",
                phone="0909123456",
                email="cuong.le@company.com",
                address="789 Đường Võ Văn Tần, Quận 3, TP.HCM",
                position="Phó Giám đốc",
                department="Ban Giám đốc",
                member_type=MemberType.ASSOCIATION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2018, 6, 1),
                notes="Lãnh đạo có tầm nhìn chiến lược"
            ),
            MemberModel(
                member_code="BCH001",
                full_name="Phạm Thị Dung",
                date_of_birth=datetime(1978, 4, 12),
                gender="Nữ",
                phone="0911987654",
                email="dung.pham@company.com",
                address="321 Đường Pasteur, Quận 1, TP.HCM",
                position="Bí thư Đoàn thanh niên",
                department="Đoàn thanh niên",
                member_type=MemberType.EXECUTIVE,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2015, 9, 15),
                notes="Bí thư có nhiều đóng góp cho tổ chức"
            ),
            MemberModel(
                member_code="DV003",
                full_name="Hoàng Văn Em",
                date_of_birth=datetime(1995, 12, 25),
                gender="Nam",
                phone="0988777666",
                email="em.hoang@company.com",
                address="654 Đường Điện Biên Phủ, Quận Bình Thạnh, TP.HCM",
                position="Lập trình viên",
                department="Phòng IT",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2022, 8, 20),
                notes="Thành viên trẻ, nhiều sáng tạo"
            ),
            MemberModel(
                member_code="DV004",
                full_name="Võ Thị Phương",
                date_of_birth=datetime(1988, 2, 14),
                gender="Nữ",
                phone="0977888999",
                email="phuong.vo@company.com",
                address="147 Đường Cách Mạng Tháng 8, Quận 10, TP.HCM",
                position="Kế toán viên",
                department="Phòng Kế toán",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.INACTIVE,
                join_date=datetime(2019, 5, 10),
                notes="Tạm nghỉ việc để chăm sóc con nhỏ"
            )
        ]
        
        # Thêm dữ liệu vào session
        session.add_all(sample_members)
        session.commit()
        session.close()
        
        print(f"✅ Successfully inserted {len(sample_members)} sample members!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample members: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        return False


def insert_sample_reports():
    """Thêm dữ liệu mẫu cho bảng reports"""
    try:
        engine = db_manager.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Kiểm tra xem đã có dữ liệu chưa
        existing_count = session.query(ReportModel).count()
        if existing_count > 0:
            print(f"📊 Reports table already has {existing_count} records. Skipping sample data insertion.")
            session.close()
            return True
        
        # Lấy một số member ID để làm submitted_by và approved_by
        member_ids = session.query(MemberModel.id).limit(3).all()
        if not member_ids:
            print("⚠️ No members found. Please insert members first.")
            session.close()
            return False
        
        member_ids = [mid[0] for mid in member_ids]
        
        sample_reports = [
            ReportModel(
                title="Báo cáo hoạt động đoàn thể tháng 1/2024",
                report_type=ReportType.MONTHLY,
                period="2024-01",
                content="""
### Báo cáo hoạt động đoàn thể tháng 1/2024

**I. Tình hình thành viên:**
- Tổng số đoàn viên: 150 người
- Số đoàn viên tham gia hoạt động: 135 người (90%)

**II. Các hoạt động đã thực hiện:**
1. Tổ chức họp mặt đầu năm
2. Triển khai kế hoạch hoạt động năm 2024
3. Thăm hỏi đoàn viên có hoàn cảnh khó khăn

**III. Tài chính:**
- Thu: 15,000,000 VNĐ
- Chi: 12,000,000 VNĐ
- Tồn quỹ: 3,000,000 VNĐ

**IV. Kế hoạch tháng tới:**
- Tổ chức hoạt động từ thiện
- Triển khai chương trình đào tạo kỹ năng
                """,
                attachments='[{"name": "bang_thong_ke_01_2024.xlsx", "path": "/uploads/reports/bang_thong_ke_01_2024.xlsx"}]',
                status=ReportStatus.APPROVED,
                submitted_by=member_ids[0],
                submitted_at=datetime(2024, 2, 5, 9, 30),
                approved_by=member_ids[1],
                approved_at=datetime(2024, 2, 6, 14, 15)
            ),
            ReportModel(
                title="Báo cáo quý I/2024",
                report_type=ReportType.QUARTERLY,
                period="Q1-2024",
                content="""
### Báo cáo tổng kết quý I/2024

**I. Tổng quan:**
Quý I/2024 là quý khởi đầu năm với nhiều hoạt động tích cực của tổ chức đoàn thể.

**II. Các chỉ tiêu đạt được:**
- Tỷ lệ tham gia hoạt động: 85%
- Số hoạt động tổ chức: 15 hoạt động
- Số đoàn viên mới: 8 người

**III. Những thành tựu nổi bật:**
1. Thành công trong việc tổ chức Hội nghị đại biểu
2. Triển khai hiệu quả chương trình an sinh xã hội
3. Tăng cường kết nối giữa các đoàn viên

**IV. Khó khăn và thách thức:**
- Một số đoàn viên chưa tích cực tham gia
- Nguồn kinh phí hạn chế cho các hoạt động lớn

**V. Định hướng quý II:**
- Tăng cường các hoạt động gắn kết
- Mở rộng các chương trình hỗ trợ đoàn viên
                """,
                attachments='[{"name": "bao_cao_quy_1_2024.pdf", "path": "/uploads/reports/bao_cao_quy_1_2024.pdf"}, {"name": "bang_bieu_thong_ke.xlsx", "path": "/uploads/reports/bang_bieu_thong_ke.xlsx"}]',
                status=ReportStatus.SUBMITTED,
                submitted_by=member_ids[1],
                submitted_at=datetime(2024, 4, 10, 16, 45)
            ),
            ReportModel(
                title="Báo cáo tổng kết năm 2023",
                report_type=ReportType.ANNUAL,
                period="2023",
                content="""
### Báo cáo tổng kết hoạt động năm 2023

**I. Tình hình chung:**
Năm 2023 là năm đạt được nhiều thành tựu quan trọng trong hoạt động đoàn thể.

**II. Các chỉ số quan trọng:**
- Tổng số đoàn viên cuối năm: 145 người (tăng 15 người so với đầu năm)
- Tỷ lệ tham gia hoạt động trung bình: 88%
- Số hoạt động tổ chức: 48 hoạt động
- Tổng kinh phí hoạt động: 180,000,000 VNĐ

**III. Những thành tựu nổi bật:**
1. Thành công tổ chức Đại hội đoàn viên lần thứ V
2. Triển khai hiệu quả 5 chương trình lớn
3. Hỗ trợ 25 gia đình đoàn viên có hoàn cảnh khó khăn
4. Tổ chức thành công 3 chuyến du lịch gắn kết

**IV. Công tác tài chính:**
- Tổng thu: 200,000,000 VNĐ
- Tổng chi: 180,000,000 VNĐ
- Dư quỹ cuối năm: 20,000,000 VNĐ

**V. Kế hoạch năm 2024:**
- Mục tiêu tăng 20 đoàn viên mới
- Triển khai 6 chương trình trọng điểm
- Nâng cao chất lượng các hoạt động
                """,
                attachments='[{"name": "bao_cao_nam_2023_full.pdf", "path": "/uploads/reports/bao_cao_nam_2023_full.pdf"}, {"name": "tai_chinh_2023.xlsx", "path": "/uploads/reports/tai_chinh_2023.xlsx"}, {"name": "hinh_anh_hoat_dong_2023.zip", "path": "/uploads/reports/hinh_anh_hoat_dong_2023.zip"}]',
                status=ReportStatus.APPROVED,
                submitted_by=member_ids[2],
                submitted_at=datetime(2024, 1, 15, 10, 0),
                approved_by=member_ids[0],
                approved_at=datetime(2024, 1, 20, 11, 30)
            ),
            ReportModel(
                title="Báo cáo đặc biệt: Hoạt động ứng phó COVID-19",
                report_type=ReportType.SPECIAL,
                period="2023-Special",
                content="""
### Báo cáo đặc biệt: Hoạt động ứng phó với tình hình COVID-19

**I. Bối cảnh:**
Trong bối cảnh dịch COVID-19 diễn biến phức tạp, tổ chức đã triển khai nhiều hoạt động hỗ trợ đoàn viên.

**II. Các hoạt động đã thực hiện:**

**1. Hỗ trợ y tế:**
- Phát 500 khẩu trang N95
- Tặng 200 bộ kit test nhanh
- Hỗ trợ thuốc điều trị cho 30 gia đình

**2. Hỗ trợ kinh tế:**
- Hỗ trợ tiền mặt cho 15 gia đình khó khăn (5,000,000 VNĐ/gia đình)
- Phát 100 suất quà gồm gạo, dầu ăn, thực phẩm khô

**3. Hỗ trợ tinh thần:**
- Tổ chức 10 buổi tư vấn tâm lý online
- Kết nối hỗ trợ giữa các đoàn viên

**III. Kết quả đạt được:**
- 100% đoàn viên được hỗ trợ thông tin về phòng chống dịch
- 90% đoàn viên và gia đình được tiêm vaccine đầy đủ
- Không có ca nào diễn biến nặng trong tổ chức

**IV. Kinh phí sử dụng:**
- Tổng chi: 120,000,000 VNĐ
- Nguồn: Quỹ dự phòng tổ chức (60%) + Quyên góp đoàn viên (40%)

**V. Bài học kinh nghiệm:**
- Tầm quan trọng của việc chuẩn bị sẵn sàng
- Sức mạnh của sự đoàn kết, tương trợ
- Cần xây dựng quỹ dự phòng lớn hơn cho các tình huống khẩn cấp
                """,
                attachments='[{"name": "danh_sach_ho_tro_covid.xlsx", "path": "/uploads/reports/danh_sach_ho_tro_covid.xlsx"}, {"name": "bien_ban_phat_qua.pdf", "path": "/uploads/reports/bien_ban_phat_qua.pdf"}]',
                status=ReportStatus.DRAFT,
                submitted_by=None,
                submitted_at=None
            ),
            ReportModel(
                title="Báo cáo hoạt động tháng 3/2024 (Dự thảo)",
                report_type=ReportType.MONTHLY,
                period="2024-03",
                content="""
### Dự thảo báo cáo hoạt động tháng 3/2024

**I. Các hoạt động chính:**
1. Tổ chức Ngày Quốc tế Phụ nữ 8/3
2. Triển khai chương trình "Mùa xuân tình nguyện"
3. Họp mặt giao lưu với các đoàn thể bạn

**II. Tình hình tài chính:**
- Thu trong tháng: 8,500,000 VNĐ
- Chi trong tháng: 7,200,000 VNĐ

**III. Kế hoạch tháng 4:**
- Chuẩn bị cho hoạt động Tháng Thanh niên
- Tổ chức khóa đào tạo kỹ năng lãnh đạo

*(Báo cáo đang được hoàn thiện)*
                """,
                attachments='[]',
                status=ReportStatus.DRAFT,
                submitted_by=None,
                submitted_at=None
            )
        ]
        
        # Thêm dữ liệu vào session
        session.add_all(sample_reports)
        session.commit()
        session.close()
        
        print(f"✅ Successfully inserted {len(sample_reports)} sample reports!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample reports: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        return False


def insert_sample_tasks():
    """Thêm dữ liệu mẫu cho bảng tasks"""
    try:
        engine = db_manager.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Kiểm tra xem đã có dữ liệu chưa
        existing_count = session.query(TaskModel).count()
        if existing_count > 0:
            print(f"📊 Tasks table already has {existing_count} records. Skipping sample data insertion.")
            session.close()
            return True
        
        # Lấy một số member ID để làm assigned_to và assigned_by
        member_ids = session.query(MemberModel.id).limit(4).all()
        if not member_ids:
            print("⚠️ No members found. Please insert members first.")
            session.close()
            return False
        
        member_ids = [mid[0] for mid in member_ids]
        
        # Tính toán các ngày
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)
        next_week = now + timedelta(days=7)
        next_month = now + timedelta(days=30)
        last_week = now - timedelta(days=7)
        
        sample_tasks = [
            TaskModel(
                title="Chuẩn bị tài liệu cho Đại hội đoàn viên",
                description="""
Chuẩ bị đầy đủ tài liệu cần thiết cho Đại hội đoàn viên lần thứ VI:

**Cần làm:**
1. Soạn thảo báo cáo tổng kết nhiệm kỳ
2. Chuẩn bị bảng biểu thống kê
3. Thiết kế slide thuyết trình
4. In ấn tài liệu phát cho đại biểu
5. Chuẩn bị danh sách đại biểu tham dự

**Yêu cầu:**
- Tài liệu phải được hoàn thành trước 3 ngày
- Cần đảm bảo tính chính xác và đầy đủ
- Thiết kế phải chuyên nghiệp và dễ đọc
                """,
                priority=TaskPriority.HIGH,
                status=TaskStatus.IN_PROGRESS,
                assigned_to=member_ids[0],
                assigned_by=member_ids[3],
                start_date=last_week,
                due_date=next_week,
                estimated_hours=40.0,
                actual_hours=25.0,
                progress_percentage=65,
                notes="Đã hoàn thành phần báo cáo tổng kết, đang làm slide thuyết trình"
            ),
            TaskModel(
                title="Tổ chức hoạt động từ thiện tháng 4",
                description="""
Lên kế hoạch và tổ chức hoạt động từ thiện nhân dịp Tháng Thanh niên:

**Các bước thực hiện:**
1. Khảo sát và chọn đối tượng thụ hưởng
2. Lập kế hoạch chi tiết cho hoạt động
3. Vận động đóng góp từ đoàn viên
4. Chuẩn bị quà tặng và nhu yếu phẩm
5. Tổ chức thực hiện hoạt động
6. Báo cáo kết quả

**Mục tiêu:**
- Hỗ trợ ít nhất 20 gia đình khó khăn
- Tổng giá trị hỗ trợ: 50,000,000 VNĐ
- Tạo không khí đoàn kết trong tổ chức
                """,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.NOT_STARTED,
                assigned_to=member_ids[1],
                assigned_by=member_ids[3],
                start_date=tomorrow,
                due_date=next_month,
                estimated_hours=60.0,
                actual_hours=0.0,
                progress_percentage=0,
                notes="Chưa bắt đầu, cần họp bàn phương án thực hiện"
            ),
            TaskModel(
                title="Cập nhật website và fanpage tổ chức",
                description="""
Nâng cấp và cập nhật nội dung website cũng như fanpage Facebook của tổ chức:

**Website:**
1. Cập nhật thông tin về Ban chấp hành mới
2. Đăng tải các bài viết về hoạt động gần đây
3. Cập nhật thư viện ảnh hoạt động
4. Tối ưu SEO cho website
5. Kiểm tra và sửa lỗi hiển thị

**Fanpage Facebook:**
1. Thiết kế lại cover photo
2. Đăng bài thường xuyên (3 bài/tuần)
3. Tương tác với các bình luận
4. Livestream các sự kiện quan trọng
5. Quảng bá các hoạt động sắp tới

**Yêu cầu kỹ thuật:**
- Sử dụng WordPress cho website
- Tích hợp Google Analytics
- Đảm bảo responsive trên mobile
                """,
                priority=TaskPriority.LOW,
                status=TaskStatus.COMPLETED,
                assigned_to=member_ids[2],
                assigned_by=member_ids[0],
                start_date=datetime(2024, 2, 1),
                due_date=datetime(2024, 3, 15),
                completed_date=datetime(2024, 3, 10),
                estimated_hours=25.0,
                actual_hours=28.0,
                progress_percentage=100,
                notes="Đã hoàn thành toàn bộ công việc. Website mới đã được triển khai thành công."
            ),
            TaskModel(
                title="Soạn thảo quy chế hoạt động mới",
                description="""
Xây dựng quy chế hoạt động mới cho tổ chức đoàn thể, thay thế quy chế cũ đã lỗi thời:

**Nội dung chính:**
1. Cấu trúc tổ chức và chức năng nhiệm vụ
2. Quy định về thành viên và quyền lợi
3. Quy trình tổ chức các hoạt động
4. Quản lý tài chính và tài sản
5. Quy định về khen thưởng và kỷ luật
6. Các văn bản mẫu và biểu đơn

**Tiến độ:**
- Giai đoạn 1: Nghiên cứu quy chế các tổ chức khác (2 tuần)
- Giai đoạn 2: Soạn thảo dự thảo (3 tuần)
- Giai đoạn 3: Lấy ý kiến đóng góp (2 tuần)
- Giai đoạn 4: Hoàn thiện và phê duyệt (1 tuần)

**Lưu ý:**
- Cần tham khảo quy chế mẫu của cấp trên
- Đảm bảo phù hợp với pháp luật hiện hành
- Phải được thông qua tại Đại hội
                """,
                priority=TaskPriority.URGENT,
                status=TaskStatus.OVERDUE,
                assigned_to=member_ids[0],
                assigned_by=member_ids[3],
                start_date=datetime(2024, 1, 15),
                due_date=yesterday,
                estimated_hours=80.0,
                actual_hours=45.0,
                progress_percentage=60,
                notes="Công việc bị chậm tiến độ do phải tham khảo thêm nhiều tài liệu pháp lý. Cần gia hạn thêm 2 tuần."
            ),
            TaskModel(
                title="Lập kế hoạch đào tạo kỹ năng cho đoàn viên",
                description="""
Thiết kế chương trình đào tạo kỹ năng toàn diện cho đoàn viên:

**Các khóa đào tạo:**
1. Kỹ năng giao tiếp và thuyết trình
2. Kỹ năng lãnh đạo và quản lý
3. Kỹ năng làm việc nhóm
4. Tin học văn phòng nâng cao
5. Tiếng Anh giao tiếp cơ bản

**Yêu cầu:**
- Mỗi khóa học 16 giờ (2 ngày)
- Tối đa 25 học viên/khóa
- Có chứng chỉ hoàn thành
- Giảng viên có kinh nghiệm

**Kế hoạch triển khai:**
- Tháng 5: Khóa giao tiếp và thuyết trình
- Tháng 6: Khóa lãnh đạo và quản lý
- Tháng 7: Khóa làm việc nhóm
- Tháng 8: Khóa tin học văn phòng
- Tháng 9: Khóa tiếng Anh

**Ngân sách dự kiến:** 100,000,000 VNĐ
                """,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.NOT_STARTED,
                assigned_to=member_ids[1],
                assigned_by=member_ids[0],
                start_date=next_week,
                due_date=datetime(2024, 5, 1),
                estimated_hours=50.0,
                actual_hours=0.0,
                progress_percentage=0,
                notes="Cần liên hệ tìm giảng viên và địa điểm tổ chức trước khi bắt đầu"
            ),
            TaskModel(
                title="Kiểm tra và cập nhật danh sách đoàn viên",
                description="""
Rà soát và cập nhật toàn bộ danh sách đoàn viên, hội viên của tổ chức:

**Công việc cụ thể:**
1. Kiểm tra thông tin cá nhân của từng thành viên
2. Cập nhật địa chỉ, số điện thoại mới
3. Ghi nhận những thay đổi về công việc, chức vụ
4. Xác định trạng thái hoạt động (active/inactive)
5. Làm thẻ đoàn viên mới cho năm 2024
6. Tạo file Excel quản lý danh sách

**Phương pháp:**
- Gửi form khảo sát online cho tất cả thành viên
- Điện thoại xác nhận với những người chưa phản hồi
- Họp với các chi đoàn để cập nhật thông tin
- Sử dụng phần mềm quản lý thành viên

**Sản phẩm đầu ra:**
- File Excel danh sách cập nhật
- 150 thẻ đoàn viên năm 2024
- Báo cáo thống kê thành viên
                """,
                priority=TaskPriority.HIGH,
                status=TaskStatus.IN_PROGRESS,
                assigned_to=member_ids[2],
                assigned_by=member_ids[3],
                start_date=datetime(2024, 3, 1),
                due_date=datetime(2024, 4, 15),
                estimated_hours=35.0,
                actual_hours=20.0,
                progress_percentage=30,
                notes="Đã gửi form khảo sát, thu về được 60% phản hồi. Đang tiếp tục liên hệ những người chưa trả lời."
            ),
            TaskModel(
                title="Tổ chức tour du lịch hè cho đoàn viên",
                description="""
Lên kế hoạch và tổ chức chuyến du lịch hè dành cho đoàn viên và gia đình:

**Địa điểm đề xuất:**
1. Đà Lạt (3 ngày 2 đêm)
2. Phú Quốc (4 ngày 3 đêm)  
3. Hạ Long (2 ngày 1 đêm)

**Cần chuẩn bị:**
1. Khảo sát ý kiến đoàn viên về địa điểm
2. Liên hệ và đàm phán với công ty lữ hành
3. Lập ngân sách chi tiết
4. Xin phép lãnh đạo đơn vị
5. Tổ chức đăng ký tham gia
6. Chuẩn bị hành lý và giấy tờ cần thiết

**Thời gian dự kiến:** Cuối tháng 7/2024
**Số lượng:** 80-100 người
**Ngân sách:** 150,000,000 VNĐ

**Lưu ý:**
- Cần có bảo hiểm du lịch cho tất cả thành viên
- Chương trình phù hợp với mọi lứa tuổi
- Dự phòng phương án thay thế khi thời tiết xấu
                """,
                priority=TaskPriority.LOW,
                status=TaskStatus.NOT_STARTED,
                assigned_to=member_ids[1],
                assigned_by=member_ids[0],
                start_date=datetime(2024, 5, 1),
                due_date=datetime(2024, 7, 15),
                estimated_hours=45.0,
                actual_hours=0.0,
                progress_percentage=0,
                notes="Chờ phê duyệt ngân sách từ Ban chấp hành mới bắt đầu triển khai"
            ),
            TaskModel(
                title="Báo cáo tài chính quý I/2024",
                description="""
Lập báo cáo tài chính chi tiết cho quý I/2024:

**Nội dung báo cáo:**
1. Tình hình thu chi trong quý
2. Bảng cân đối tài sản - nguồn vốn
3. Phân tích các khoản thu chi bất thường
4. So sánh với cùng kỳ năm trước
5. Dự báo tình hình tài chính quý II

**Tài liệu cần thiết:**
- Sổ sách kế toán quý I
- Chứng từ thu chi gốc
- Bảng kê ngân hàng
- Hóa đơn, chứng từ liên quan

**Yêu cầu:**
- Báo cáo phải chính xác, minh bạch
- Tuân thủ chuẩn mực kế toán
- Có ý kiến của Ban kiểm soát
- Trình bày rõ ràng, dễ hiểu
                """,
                priority=TaskPriority.HIGH,
                status=TaskStatus.COMPLETED,
                assigned_to=member_ids[2],
                assigned_by=member_ids[3],
                start_date=datetime(2024, 4, 1),
                due_date=datetime(2024, 4, 10),
                completed_date=datetime(2024, 4, 8),
                estimated_hours=20.0,
                actual_hours=18.0,
                progress_percentage=100,
                notes="Báo cáo đã hoàn thành và được Ban chấp hành phê duyệt. Tình hình tài chính ổn định."
            )
        ]
        
        # Thêm dữ liệu vào session
        session.add_all(sample_tasks)
        session.commit()
        session.close()
        
        print(f"✅ Successfully inserted {len(sample_tasks)} sample tasks!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample tasks: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        return False


def insert_sample_data():
    """Thêm tất cả dữ liệu mẫu vào database"""
    print("📊 Inserting sample data...")
    
    success = True
    
    # Insert members first (vì các bảng khác có thể tham chiếu đến members)
    if not insert_sample_members():
        success = False
    
    # Insert reports
    if not insert_sample_reports():
        success = False
    
    # Insert tasks  
    if not insert_sample_tasks():
        success = False
    
    if success:
        print("🎉 All sample data inserted successfully!")
    else:
        print("❌ Some errors occurred while inserting sample data!")
    
    return success


def init_database():
    """Khởi tạo PostgreSQL database và tạo các bảng"""
    print("🔧 Initializing PostgreSQL database...")
    
    # Test kết nối
    if not db_manager.test_connection():
        print("❌ PostgreSQL database connection failed!")
        return False
    
    print("✅ PostgreSQL database connection successful!")
    
    # Tạo các bảng
    if create_tables():
        print("✅ PostgreSQL database tables created successfully!")
        
        # Thêm dữ liệu mẫu
        if insert_sample_data():
            print("🎉 PostgreSQL database initialization with sample data completed!")
            return True
        else:
            print("⚠️ Database tables created but sample data insertion failed!")
            return True  # Vẫn coi là thành công vì bảng đã tạo được
    else:
        print("❌ PostgreSQL database initialization failed!")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "sample-data":
            # Chỉ thêm dữ liệu mẫu
            print("📊 Adding sample data to existing database...")
            if insert_sample_data():
                print("🎉 Sample data added successfully!")
            else:
                print("❌ Failed to add sample data!")
        elif sys.argv[1] == "drop":
            # Xóa tất cả bảng
            print("⚠️ Dropping all tables...")
            if drop_tables():
                print("✅ All tables dropped successfully!")
        elif sys.argv[1] == "recreate":
            # Xóa và tạo lại database với dữ liệu mẫu
            print("🔄 Recreating database...")
            drop_tables()
            init_database()
        else:
            print("Usage:")
            print("  python setup.py                 # Initialize database with sample data")
            print("  python setup.py sample-data     # Add sample data only")
            print("  python setup.py drop            # Drop all tables")
            print("  python setup.py recreate        # Drop and recreate database")
    else:
        # Chạy script để khởi tạo database với dữ liệu mẫu
        init_database()