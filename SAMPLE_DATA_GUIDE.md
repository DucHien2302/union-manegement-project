# 🚀 Hướng dẫn sử dụng Union Management System

## 📋 Dữ liệu mẫu có sẵn

Hệ thống đã được cài đặt sẵn dữ liệu mẫu để người dùng mới có thể trải nghiệm đầy đủ các tính năng:

### 👥 **15 Members (Thành viên)**
- **10 Đoàn viên hoạt động** (Active)
- **2 Đoàn viên tạm nghỉ** (Inactive) 
- **1 Đoàn viên bị đình chỉ** (Suspended)
- **3 Hội viên** (Association Members)
- **2 Ban chấp hành** (Executive)

### 📊 **11 Reports (Báo cáo)**
- **3 Báo cáo đã duyệt** (Approved) - để test xuất Excel
- **4 Báo cáo chờ duyệt** (Submitted) - để test bulk actions
- **4 Báo cáo nháp** (Draft) - để test chỉnh sửa

### ✅ **16 Tasks (Công việc)** 
- **3 Hoàn thành** (Completed)
- **4 Đang thực hiện** (In Progress) 
- **5 Chưa bắt đầu** (Not Started)
- **2 Tạm dừng** (On Hold) - để test bulk actions
- **1 Quá hạn** (Overdue)
- **1 Đã hủy** (Cancelled)

## 🎯 **Các tính năng chính để test**

### 1. **📑 Quản lý thành viên**
- ✅ Xem danh sách 15 thành viên đa dạng
- ✅ **Xuất Excel** toàn bộ danh sách thành viên
- ✅ Tìm kiếm và lọc theo trạng thái
- ✅ Thêm/sửa/xóa thành viên

### 2. **📈 Quản lý báo cáo**
- ✅ **Bulk Actions**: Chọn nhiều báo cáo và thực hiện hàng loạt:
  - Duyệt nhiều báo cáo cùng lúc
  - Từ chối nhiều báo cáo cùng lúc  
  - Xóa nhiều báo cáo được chọn
- ✅ **Xuất Excel** báo cáo với định dạng chuyên nghiệp
- ✅ Lọc theo loại báo cáo và trạng thái
- ✅ Xem chi tiết nội dung báo cáo

### 3. **📋 Quản lý công việc**
- ✅ **Bulk Actions**: Thao tác hàng loạt với checkbox:
  - Hoàn thành nhiều công việc cùng lúc
  - Tạm dừng nhiều công việc
  - Xóa nhiều công việc được chọn
- ✅ **Xuất Excel** danh sách công việc với màu theo trạng thái
- ✅ Lọc theo độ ưu tiên và trạng thái
- ✅ Theo dõi tiến độ hoàn thành

## 🔧 **Cách sử dụng Bulk Actions**

1. **Chọn items**: Click vào checkbox ☐ ở cột đầu tiên
2. **Chọn tất cả**: Có thể chọn nhiều items bằng cách click từng checkbox
3. **Thực hiện thao tác**: Click vào các nút bulk action:
   - **Reports**: "Duyệt", "Từ chối", "Xóa được chọn"  
   - **Tasks**: "Hoàn thành", "Tạm dừng", "Xóa được chọn"

## 📊 **Xuất Excel**

Tất cả 3 module đều hỗ trợ xuất Excel với:
- 🎨 **Định dạng chuyên nghiệp**: Headers màu xanh, borders đẹp
- 🌈 **Màu sắc theo trạng thái**: Mỗi trạng thái có màu riêng
- 📅 **Định dạng ngày tháng**: DD/MM/YYYY chuẩn Việt Nam
- 💾 **Tự động đặt tên file**: Với timestamp và tổng số records

## 🎮 **Gợi ý trải nghiệm cho người mới**

### **Bước 1**: Khám phá dữ liệu
- Xem danh sách Members, Reports, Tasks
- Thử các bộ lọc khác nhau
- Tìm kiếm theo từ khóa

### **Bước 2**: Test Bulk Actions  
- Chọn 2-3 reports có trạng thái "Submitted"
- Click "Duyệt" để duyệt hàng loạt
- Chọn một số tasks và thử "Hoàn thành"

### **Bước 3**: Xuất Excel
- Xuất danh sách Members (15 records)
- Xuất Reports với định dạng đẹp
- Xuất Tasks với màu sắc theo trạng thái

### **Bước 4**: Thêm dữ liệu mới
- Thêm member mới để test form validation
- Tạo báo cáo mới và thử workflow approve
- Tạo task mới với priority và due date

## 🔄 **Reset dữ liệu mẫu**

Nếu muốn reset về dữ liệu mẫu ban đầu:

```bash
python infrastructure/database/setup.py recreate
```

## 🎉 **Kết quả mong đợi**

Sau khi trải nghiệm, bạn sẽ thấy:
- ✅ Giao diện hiện đại, dễ sử dụng
- ✅ Bulk actions hoạt động mượt mà
- ✅ Excel export chuyên nghiệp  
- ✅ Tìm kiếm và lọc linh hoạt
- ✅ Workflow quản lý hoàn chỉnh

---

**💡 Tip**: Dữ liệu mẫu được thiết kế để demo tất cả các tình huống sử dụng thực tế, từ thành viên active/inactive đến các trạng thái báo cáo và task đa dạng.