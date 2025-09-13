# Hệ thống Quản lý Đoàn - Hội

Hệ thống quản lý đoàn viên, hội viên và công việc được xây dựng với kiến trúc sạch (Clean Architecture) và Python.

## Tính năng chính

### 1. Quản lý thành viên
- Quản lý thông tin đoàn viên, hội viên
- Quản lý ban chấp hành
- Theo dõi trạng thái hoạt động
- Tìm kiếm và báo cáo thành viên

### 2. Quản lý báo cáo
- Tạo và quản lý báo cáo tháng, quý, năm
- Quy trình duyệt báo cáo
- Theo dõi tiến độ báo cáo
- Lưu trữ file đính kèm

### 3. Quản lý công việc
- Giao việc và theo dõi tiến độ
- Quản lý ưu tiên và deadline
- Báo cáo thống kê hiệu suất
- Cảnh báo công việc quá hạn

## Kiến trúc hệ thống

Hệ thống được xây dựng theo nguyên tắc Clean Architecture với các layer:

```
📁 union_management_system/
├── 📁 domain/           # Tầng Domain - Business logic core
│   ├── 📁 entities/     # Các entity chính
│   └── 📁 repositories/ # Interface của repositories
├── 📁 application/      # Tầng Application - Use cases
│   ├── 📁 use_cases/    # Các use case chính
│   └── 📁 services/     # Application services
├── 📁 infrastructure/   # Tầng Infrastructure - External concerns
│   ├── 📁 database/     # Database configuration và models
│   └── 📁 repositories/ # Implementation của repositories
├── 📁 presentation/     # Tầng Presentation - UI
│   ├── 📁 gui/          # Giao diện Tkinter
│   └── 📁 controllers/  # Controllers
├── 📁 config/           # Configuration files
└── 📁 tests/           # Unit tests
```

## Yêu cầu hệ thống

### Phần mềm cần thiết
- Python 3.8+
- PostgreSQL 12+
- Spyder IDE (khuyến nghị)

### Python packages
Xem file `requirements.txt` để biết danh sách đầy đủ. Các package chính:
- `sqlalchemy` - ORM cho database
- `psycopg2-binary` - PostgreSQL driver
- `tkinter` - GUI framework (có sẵn với Python)

## Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Cấu hình database
1. Tạo file `.env` từ `.env.example`:
   ```bash
   copy config\.env.example .env
   ```

2. Cập nhật thông tin database trong file `.env`:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=union_management
   DB_USERNAME=postgres
   DB_PASSWORD=your_password
   ```

### 3. Khởi tạo database
Chạy script để tạo database và tables:
```python
python infrastructure/database/setup.py
```

### 4. Chạy ứng dụng
```python
python presentation/gui/main_window.py
```

## Sử dụng trong Spyder

1. Mở Spyder IDE
2. Set working directory tới thư mục dự án
3. Chạy file `presentation/gui/main_window.py`

## Cấu trúc Database

### Bảng Members (Thành viên)
- Lưu trữ thông tin đoàn viên, hội viên, ban chấp hành
- Các trường: ID, mã thành viên, họ tên, loại, chức vụ, phòng ban, trạng thái

### Bảng Reports (Báo cáo)
- Quản lý các báo cáo định kỳ
- Quy trình: Nháp → Nộp → Duyệt/Từ chối

### Bảng Tasks (Công việc)
- Theo dõi giao việc và tiến độ
- Các trạng thái: Chưa bắt đầu → Đang thực hiện → Hoàn thành

## Tính năng nổi bật

### Clean Architecture
- Tách biệt rõ ràng giữa business logic và technical concerns
- Dễ dàng test và maintain
- Có thể thay đổi UI hoặc database mà không ảnh hưởng core logic

### Repository Pattern
- Abstraction layer cho data access
- Dễ dàng mock để unit test
- Có thể switch giữa các loại database

### Use Case Driven Design
- Mỗi use case đại diện cho một business requirement
- Code dễ hiểu và maintain
- Tuân thủ Single Responsibility Principle

## Development

### Chạy tests
```bash
pytest tests/
```

### Code formatting
```bash
black .
flake8 .
```

### Thêm tính năng mới
1. Tạo entity trong `domain/entities/`
2. Định nghĩa repository interface trong `domain/repositories/`
3. Implement repository trong `infrastructure/repositories/`
4. Tạo use case trong `application/use_cases/`
5. Cập nhật GUI trong `presentation/gui/`

## Troubleshooting

### Lỗi kết nối database
1. Kiểm tra SQL Server đã chạy
2. Verify connection string trong file `.env`
3. Đảm bảo ODBC Driver đã được cài đặt

### Lỗi import modules
1. Kiểm tra PYTHONPATH
2. Đảm bảo đang chạy từ thư mục gốc của project

## Roadmap

### Version 1.1
- [ ] Thêm tính năng xuất Excel
- [ ] Email notifications
- [ ] Advanced search và filters
- [ ] Dashboard với charts

### Version 1.2
- [ ] Web interface (FastAPI)
- [ ] Mobile app integration
- [ ] Document management
- [ ] Workflow automation

## Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Create Pull Request

## License

[MIT License](LICENSE)

## Liên hệ

Để được hỗ trợ hoặc báo cáo lỗi, vui lòng tạo issue trên GitHub repository.