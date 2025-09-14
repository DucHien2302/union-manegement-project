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
            ),
            # Thêm nhiều members mới cho demo
            MemberModel(
                member_code="DV005",
                full_name="Nguyễn Thị Giang",
                date_of_birth=datetime(1992, 9, 8),
                gender="Nữ",
                phone="0966555444",
                email="giang.nguyen@company.com",
                address="258 Đường Hai Bà Trưng, Quận 1, TP.HCM",
                position="Chuyên viên Marketing",
                department="Phòng Marketing",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2023, 1, 5),
                notes="Sáng tạo trong công việc, tích cực tham gia hoạt động"
            ),
            MemberModel(
                member_code="DV006",
                full_name="Đặng Văn Hưng",
                date_of_birth=datetime(1987, 6, 30),
                gender="Nam",
                phone="0933222111",
                email="hung.dang@company.com",
                address="369 Đường Lý Tự Trọng, Quận 3, TP.HCM",
                position="Trưởng phòng Kinh doanh",
                department="Phòng Kinh doanh",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2019, 11, 20),
                notes="Có nhiều kinh nghiệm trong lĩnh vực kinh doanh"
            ),
            MemberModel(
                member_code="HV002",
                full_name="Phan Thị Lan",
                date_of_birth=datetime(1975, 1, 18),
                gender="Nữ",
                phone="0922111333",
                email="lan.phan@company.com",
                address="741 Đường Nguyễn Thị Minh Khai, Quận 3, TP.HCM",
                position="Giám đốc Tài chính",
                department="Ban Giám đốc",
                member_type=MemberType.ASSOCIATION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2017, 4, 12),
                notes="Chuyên gia tài chính với hơn 15 năm kinh nghiệm"
            ),
            MemberModel(
                member_code="DV007",
                full_name="Vũ Văn Khang",
                date_of_birth=datetime(1993, 10, 5),
                gender="Nam",
                phone="0944666888",
                email="khang.vu@company.com",
                address="852 Đường Sư Vạn Hạnh, Quận 10, TP.HCM",
                position="Thiết kế đồ họa",
                department="Phòng Marketing",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2023, 6, 15),
                notes="Tài năng trẻ trong lĩnh vực thiết kế"
            ),
            MemberModel(
                member_code="DV008",
                full_name="Lý Thị Mai",
                date_of_birth=datetime(1991, 4, 25),
                gender="Nữ",
                phone="0955777999",
                email="mai.ly@company.com",
                address="159 Đường Cộng Hòa, Quận Tân Bình, TP.HCM",
                position="Chuyên viên Pháp chế",
                department="Phòng Pháp chế",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.SUSPENDED,
                join_date=datetime(2020, 8, 30),
                notes="Tạm đình chỉ do vi phạm nội quy công ty"
            ),
            MemberModel(
                member_code="BCH002",
                full_name="Tô Văn Nam",
                date_of_birth=datetime(1980, 12, 3),
                gender="Nam",
                phone="0911444555",
                email="nam.to@company.com",
                address="753 Đường Nguyễn Văn Cừ, Quận 5, TP.HCM",
                position="Phó Bí thư Đoàn",
                department="Đoàn thanh niên",
                member_type=MemberType.EXECUTIVE,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2016, 2, 28),
                notes="Hỗ trợ tích cực cho các hoạt động đoàn thể"
            ),
            MemberModel(
                member_code="DV009",
                full_name="Ngô Thị Oanh",
                date_of_birth=datetime(1994, 8, 14),
                gender="Nữ",
                phone="0977123789",
                email="oanh.ngo@company.com",
                address="456 Đường Lê Văn Sỹ, Quận Phú Nhuận, TP.HCM",
                position="Chuyên viên Quan hệ khách hàng",
                department="Phòng Kinh doanh",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2022, 12, 1),
                notes="Có khả năng giao tiếp tốt với khách hàng"
            ),
            MemberModel(
                member_code="DV010",
                full_name="Bùi Văn Phúc",
                date_of_birth=datetime(1989, 5, 22),
                gender="Nam",
                phone="0988456123",
                email="phuc.bui@company.com",
                address="987 Đường Hoàng Văn Thụ, Quận Tân Bình, TP.HCM",
                position="Chuyên viên Kỹ thuật",
                department="Phòng Kỹ thuật",
                member_type=MemberType.UNION_MEMBER,
                status=MemberStatus.INACTIVE,
                join_date=datetime(2018, 7, 15),
                notes="Nghỉ phép dài hạn do chấn thương"
            ),
            MemberModel(
                member_code="HV003",
                full_name="Đỗ Thị Quỳnh",
                date_of_birth=datetime(1983, 11, 10),
                gender="Nữ",
                phone="0933789456",
                email="quynh.do@company.com",
                address="321 Đường Trần Hưng Đạo, Quận 1, TP.HCM",
                position="Trưởng phòng Nhân sự",
                department="Phòng Nhân sự",
                member_type=MemberType.ASSOCIATION_MEMBER,
                status=MemberStatus.ACTIVE,
                join_date=datetime(2019, 3, 18),
                notes="Có chuyên môn cao trong quản lý nhân sự"
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
            ),
            # Thêm nhiều reports mới cho demo bulk actions
            ReportModel(
                title="Báo cáo hoạt động tháng 2/2024",
                report_type=ReportType.MONTHLY,
                period="2024-02",
                content="""
### Báo cáo hoạt động tháng 2/2024

**I. Hoạt động nổi bật:**
1. Tổ chức Tết truyền thống cho đoàn viên
2. Chương trình thăm hỏi Tết cho gia đình khó khăn  
3. Hội nghị triển khai nhiệm vụ năm 2024

**II. Kết quả đạt được:**
- Tổ chức thành công 5 hoạt động lớn
- Hỗ trợ 30 gia đình có hoàn cảnh khó khăn
- Tỷ lệ tham gia hoạt động: 92%

**III. Tài chính tháng 2:**
- Thu: 18,000,000 VNĐ
- Chi: 15,500,000 VNĐ  
- Dư: 2,500,000 VNĐ
                """,
                attachments='[{"name": "hinh_anh_tet_2024.zip", "path": "/uploads/reports/hinh_anh_tet_2024.zip"}]',
                status=ReportStatus.SUBMITTED,
                submitted_by=member_ids[0],
                submitted_at=datetime(2024, 3, 2, 8, 30)
            ),
            ReportModel(
                title="Báo cáo hoạt động tháng 4/2024",
                report_type=ReportType.MONTHLY,
                period="2024-04",
                content="""
### Báo cáo hoạt động tháng 4/2024

**I. Tháng thanh niên 2024:**
1. Hội trại thanh niên "Tuổi trẻ năng động"
2. Chương trình tình nguyện vệ sinh môi trường
3. Thi tìm hiểu lịch sử Đoàn TNCS Hồ Chí Minh

**II. Các chỉ số đạt được:**
- Số đoàn viên tham gia: 140/150 (93.3%)
- Số hoạt động tổ chức: 8 hoạt động
- Điểm đánh giá hoạt động: 9.2/10

**III. Những điểm nổi bật:**
- Tăng cường tinh thần đoàn kết
- Nâng cao ý thức trách nhiệm xã hội
- Phát huy sáng kiến của thanh niên
                """,
                attachments='[{"name": "bang_diem_thi_tim_hieu.xlsx", "path": "/uploads/reports/bang_diem_thi_tim_hieu.xlsx"}]',
                status=ReportStatus.SUBMITTED,
                submitted_by=member_ids[1],
                submitted_at=datetime(2024, 5, 3, 14, 20)
            ),
            ReportModel(
                title="Báo cáo tình hình tài chính 6 tháng đầu năm 2024",
                report_type=ReportType.SPECIAL,
                period="2024-H1",
                content="""
### Báo cáo tài chính 6 tháng đầu năm 2024

**I. Tổng quan:**
6 tháng đầu năm 2024 tổ chức duy trì hoạt động ổn định về tài chính.

**II. Thu nhập:**
- Phí đoàn viên: 90,000,000 VNĐ
- Tài trợ từ đơn vị: 50,000,000 VNĐ
- Các khoản thu khác: 10,000,000 VNĐ
- **Tổng thu: 150,000,000 VNĐ**

**III. Chi phí:**
- Hoạt động đoàn thể: 85,000,000 VNĐ
- Hỗ trợ đoàn viên: 35,000,000 VNĐ
- Chi phí quản lý: 15,000,000 VNĐ
- **Tổng chi: 135,000,000 VNĐ**

**IV. Kết quả:**
- **Dư thu: 15,000,000 VNĐ**
- Tình hình tài chính lành mạnh
- Đảm bảo hoạt động 6 tháng cuối năm
                """,
                attachments='[{"name": "bang_can_doi_tai_chinh_h1_2024.xlsx", "path": "/uploads/reports/bang_can_doi_tai_chinh_h1_2024.xlsx"}]',
                status=ReportStatus.DRAFT,
                submitted_by=None,
                submitted_at=None
            ),
            ReportModel(
                title="Báo cáo hoạt động tháng 5/2024",
                report_type=ReportType.MONTHLY,
                period="2024-05",
                content="""
### Báo cáo hoạt động tháng 5/2024

**I. Các hoạt động chính:**
1. Tổ chức lễ kỷ niệm ngày thành lập Đoàn TNCS HCM
2. Chương trình trao tặng học bổng cho con em đoàn viên
3. Hội thi tài năng của đoàn viên trẻ

**II. Kết quả đạt được:**
- Trao 15 suất học bổng, tổng giá trị 45,000,000 VNĐ
- 25 tiết mục tham gia hội thi tài năng
- Tỷ lệ tham gia hoạt động: 88%

**III. Đánh giá:**
- Hoạt động đạt hiệu quả cao
- Đoàn viên hưởng ứng tích cực
- Tạo sân chơi bổ ích cho thanh niên
                """,
                attachments='[]',
                status=ReportStatus.SUBMITTED,
                submitted_by=member_ids[2],
                submitted_at=datetime(2024, 6, 1, 16, 45)
            ),
            ReportModel(
                title="Báo cáo quý II/2024",
                report_type=ReportType.QUARTERLY,
                period="Q2-2024",
                content="""
### Báo cáo quý II/2024

**I. Tổng quan quý II:**
Quý II đã triển khai nhiều hoạt động ý nghĩa, đặc biệt là Tháng Thanh niên.

**II. Các chỉ tiêu hoàn thành:**
- Số hoạt động: 18 hoạt động (vượt kế hoạch 20%)
- Tỷ lệ tham gia: 89% (đạt chỉ tiêu 85%)
- Số đoàn viên mới: 5 người

**III. Hoạt động nổi bật:**
1. Tháng Thanh niên với 8 hoạt động đa dạng
2. Chương trình học bổng ý nghĩa
3. Các hoạt động giao lưu văn hóa - thể thao

**IV. Khó khăn:**
- Thời tiết mưa nhiều ảnh hưởng một số hoạt động ngoài trời
- Một số đoàn viên bận công việc chưa tham gia đầy đủ
                """,
                attachments='[{"name": "bao_cao_quy_2_2024.pdf", "path": "/uploads/reports/bao_cao_quy_2_2024.pdf"}]',
                status=ReportStatus.DRAFT,
                submitted_by=None,
                submitted_at=None
            ),
            ReportModel(
                title="Báo cáo đặc biệt: Hoạt động hè 2024",
                report_type=ReportType.SPECIAL,
                period="2024-Summer",
                content="""
### Báo cáo hoạt động hè 2024

**I. Tổng quan:**
Mùa hè 2024 với nhiều hoạt động bổ ích cho đoàn viên và thanh thiếu nhi.

**II. Các chương trình đã triển khai:**
1. **Trại hè thanh niên 2024:**
   - 60 đoàn viên tham gia
   - Thời gian: 3 ngày 2 đêm tại Đà Lạt
   - Ngân sách: 120,000,000 VNĐ

2. **Lớp học hè cho con em đoàn viên:**
   - 40 em tham gia
   - Các môn: Toán, Văn, Tiếng Anh, Tin học
   - Miễn phí 100%

3. **Chương trình tình nguyện mùa hè:**
   - Dạy học cho trẻ em vùng khó khăn
   - 20 tình nguyện viên tham gia
   - Thời gian: 2 tuần

**III. Kết quả đạt được:**
- Tăng cường kỹ năng sống cho đoàn viên
- Nâng cao tinh thần tình nguyện
- Hỗ trợ giáo dục cho con em đoàn viên
                """,
                attachments='[{"name": "album_anh_he_2024.zip", "path": "/uploads/reports/album_anh_he_2024.zip"}]',
                status=ReportStatus.SUBMITTED,
                submitted_by=member_ids[0],
                submitted_at=datetime(2024, 8, 15, 10, 30)
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
            ),
            # Thêm nhiều tasks mới cho demo
            TaskModel(
                title="Thiết kế poster tuyên truyền",
                description="""
Thiết kế các poster tuyên truyền cho các hoạt động sắp tới:

**Yêu cầu thiết kế:**
1. Poster cho Ngày hội thể thao
2. Poster cho chương trình từ thiện
3. Poster tuyển đoàn viên mới
4. Banner cho website

**Thông số kỹ thuật:**
- Kích thước: A3 cho poster, 1200x400px cho banner
- Định dạng: AI, PSD, PNG, JPG
- Màu sắc: Theo bộ nhận diện tổ chức
- Font chữ: Roboto, Arial

**Deadline:**
- Draft 1: 3 ngày
- Final: 1 tuần
                """,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.IN_PROGRESS,
                assigned_to=member_ids[1],
                assigned_by=member_ids[0],
                start_date=now - timedelta(days=2),
                due_date=now + timedelta(days=5),
                estimated_hours=16.0,
                actual_hours=8.0,
                progress_percentage=50,
                notes="Đã hoàn thành 2/4 poster, đang làm poster tuyển đoàn viên mới"
            ),
            TaskModel(
                title="Chuẩn bị văn phòng phẩm cho năm học mới",
                description="""
Mua sắm và chuẩn bị văn phòng phẩm cho hoạt động năm học 2024-2025:

**Danh sách cần mua:**
1. Giấy A4: 20 ream
2. Bút bi: 100 cái
3. Bút chì: 50 cái  
4. Tẩy: 30 cái
5. Kẹp giấy: 10 hộp
6. Ghim đóng: 5 hộp
7. Băng keo: 20 cuộn
8. Thư mục: 50 cái

**Ngân sách:** 5,000,000 VNĐ
**Nhà cung cấp:** Công ty Thiên Long, Bình Minh
**Giao hàng:** Trước 15/9/2024
                """,
                priority=TaskPriority.LOW,
                status=TaskStatus.NOT_STARTED,
                assigned_to=member_ids[2],
                assigned_by=member_ids[3],
                start_date=now + timedelta(days=1),
                due_date=now + timedelta(days=10),
                estimated_hours=8.0,
                actual_hours=0.0,
                progress_percentage=0,
                notes="Chờ phê duyệt ngân sách từ phòng tài chính"
            ),
            TaskModel(
                title="Tổ chức khóa đào tạo kỹ năng mềm",
                description="""
Tổ chức khóa đào tạo kỹ năng mềm cho đoàn viên:

**Nội dung đào tạo:**
1. Kỹ năng giao tiếp hiệu quả
2. Kỹ năng thuyết trình
3. Kỹ năng làm việc nhóm
4. Quản lý thời gian
5. Tư duy sáng tạo

**Logistics:**
- Thời gian: 2 ngày (thứ 7-chủ nhật)
- Địa điểm: Hội trường công ty
- Số lượng: 50 học viên
- Giảng viên: Mời từ bên ngoài

**Chuẩn bị:**
- Liên hệ giảng viên
- Đặt suất ăn
- In tài liệu
- Chuẩn bị thiết bị
                """,
                priority=TaskPriority.HIGH,
                status=TaskStatus.NOT_STARTED,
                assigned_to=member_ids[0],
                assigned_by=member_ids[3],
                start_date=now + timedelta(days=3),
                due_date=now + timedelta(days=21),
                estimated_hours=40.0,
                actual_hours=0.0,
                progress_percentage=0,
                notes="Cần xác định ngân sách và phê duyệt kế hoạch trước khi triển khai"
            ),
            TaskModel(
                title="Sửa chữa âm thanh phòng hội thảo",
                description="""
Sửa chữa hệ thống âm thanh phòng hội thảo bị hỏng:

**Vấn đề hiện tại:**
- Micro không bắt âm
- Loa bị rè, kêu to
- Mixer có tiếng ồn
- Dây cáp bị đứt một số đoạn

**Cần làm:**
1. Kiểm tra toàn bộ hệ thống
2. Thay thế linh kiện hỏng
3. Căng lại dây cáp
4. Test thử toàn hệ thống
5. Bảo dưỡng định kỳ

**Dự kiến chi phí:** 3,000,000 VNĐ
**Thời gian sửa:** 2 ngày
                """,
                priority=TaskPriority.URGENT,
                status=TaskStatus.IN_PROGRESS,
                assigned_to=member_ids[3],
                assigned_by=member_ids[0],
                start_date=yesterday,
                due_date=tomorrow,
                estimated_hours=16.0,
                actual_hours=10.0,
                progress_percentage=70,
                notes="Đã xác định được nguyên nhân, đang chờ linh kiện thay thế từ nhà cung cấp"
            ),
            TaskModel(
                title="Cập nhật hồ sơ thành viên cho năm 2024",
                description="""
Cập nhật và rà soát hồ sơ thành viên theo quy định mới:

**Công việc cần làm:**
1. Thu thập thông tin cập nhật từ thành viên
2. Scan và lưu trữ giấy tờ mới
3. Cập nhật vào hệ thống quản lý
4. In thẻ thành viên mới
5. Lưu trữ hồ sơ theo quy định

**Giấy tờ cần cập nhật:**
- CMND/CCCD mới
- Bằng cấp mới (nếu có)
- Thông tin liên hệ
- Nơi làm việc hiện tại

**Số lượng:** 150 hồ sơ
**Thời hạn:** 1 tháng
                """,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.ON_HOLD,
                assigned_to=member_ids[1],
                assigned_by=member_ids[2],
                start_date=last_week,
                due_date=next_month,
                estimated_hours=60.0,
                actual_hours=15.0,
                progress_percentage=25,
                notes="Tạm dừng do đang chờ hướng dẫn mới từ cấp trên về mẫu hồ sơ"
            ),
            TaskModel(
                title="Lên kế hoạch hoạt động cuối năm 2024",
                description="""
Xây dựng kế hoạch tổng thể cho các hoạt động cuối năm:

**Các hoạt động chính:**
1. **Tháng 10:** Kỷ niệm ngày Phụ nữ Việt Nam
2. **Tháng 11:** Hội nghị tổng kết năm
3. **Tháng 12:** 
   - Gala dinner cuối năm
   - Trao giải thưởng xuất sắc
   - Tiệc tất niên

**Cần chuẩn bị:**
- Ngân sách chi tiết
- Địa điểm tổ chức
- Chương trình nghệ thuật
- Danh sách khách mời
- Quà tặng và phần thưởng

**Ngân sách dự kiến:** 200,000,000 VNĐ
**Timeline:** Bắt đầu chuẩn bị từ tháng 9
                """,
                priority=TaskPriority.HIGH,
                status=TaskStatus.NOT_STARTED,
                assigned_to=member_ids[0],
                assigned_by=member_ids[3],
                start_date=next_week,
                due_date=datetime(2024, 12, 31),
                estimated_hours=80.0,
                actual_hours=0.0,
                progress_percentage=0,
                notes="Cần họp Ban chấp hành để thống nhất phương án trước khi triển khai"
            ),
            TaskModel(
                title="Backup và bảo mật dữ liệu hệ thống",
                description="""
Thực hiện backup và tăng cường bảo mật cho hệ thống IT:

**Công việc backup:**
1. Backup database hàng tuần
2. Backup files quan trọng
3. Test phục hồi dữ liệu
4. Lưu trữ backup ngoài site

**Tăng cường bảo mật:**
1. Cập nhật antivirus
2. Cập nhật Windows Update
3. Thay đổi password định kỳ
4. Kiểm tra firewall
5. Quét malware toàn hệ thống

**Lịch thực hiện:**
- Backup: Mỗi chủ nhật
- Bảo mật: Mỗi tháng
- Kiểm tra: Mỗi quý
                """,
                priority=TaskPriority.HIGH,
                status=TaskStatus.IN_PROGRESS,
                assigned_to=member_ids[2],
                assigned_by=member_ids[0],
                start_date=now - timedelta(days=5),
                due_date=now + timedelta(days=2),
                estimated_hours=12.0,
                actual_hours=8.0,
                progress_percentage=65,
                notes="Đã hoàn thành backup, đang thực hiện cập nhật bảo mật"
            ),
            TaskModel(
                title="Khảo sát ý kiến đoàn viên về hoạt động 2024",
                description="""
Tiến hành khảo sát ý kiến đoàn viên về chất lượng hoạt động năm 2024:

**Nội dung khảo sát:**
1. Đánh giá các hoạt động đã tham gia
2. Ý kiến về chương trình đào tạo
3. Góp ý về hoạt động tài chính
4. Đề xuất hoạt động năm 2025
5. Đánh giá Ban chấp hành

**Phương pháp:**
- Khảo sát online qua Google Form
- Phỏng vấn trực tiếp một số đoàn viên
- Họp nhóm tập trung (Focus Group)

**Mục tiêu:** 90% đoàn viên tham gia khảo sát
**Thời gian:** 2 tuần
**Sản phẩm:** Báo cáo khảo sát 50 trang
                """,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.CANCELLED,
                assigned_to=member_ids[1],
                assigned_by=member_ids[3],
                start_date=datetime(2024, 6, 1),
                due_date=datetime(2024, 6, 15),
                estimated_hours=24.0,
                actual_hours=4.0,
                progress_percentage=15,
                notes="Hủy do trùng thời gian với khảo sát của cấp trên, sẽ tổ chức lại vào tháng 10"
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