#!/usr/bin/env python3
"""
Test PostgreSQL database connection và truy vấn dữ liệu
Chỉ hỗ trợ PostgreSQL - SQLite đã được loại bỏ
"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from infrastructure.database.connection import db_manager

def test_database():
    """Test kết nối và truy vấn PostgreSQL database"""
    
    try:
        # Test kết nối PostgreSQL
        if not db_manager.test_connection():
            print("❌ Không thể kết nối PostgreSQL database")
            return False
        
        session = db_manager.get_session()
        print("🔗 Kết nối PostgreSQL database thành công!")
        
        # Test query members với schema mới
        print("\n👥 Danh sách thành viên:")
        try:
            result = session.execute(text("SELECT id, member_code, full_name, email, member_type, status FROM members LIMIT 5"))
            for row in result:
                print(f"  - {row.id}: {row.member_code} - {row.full_name} ({row.email}) - {row.member_type} - {row.status}")
        except Exception as e:
            print(f"  Chưa có thành viên nào: {e}")
        
        # Test query tasks với schema mới
        print("\n📋 Danh sách công việc:")
        try:
            result = session.execute(text("SELECT id, title, priority, status, assigned_to FROM tasks LIMIT 5"))
            for row in result:
                print(f"  - {row.id}: {row.title} - {row.priority} - {row.status} - Assigned: {row.assigned_to}")
        except Exception as e:
            print(f"  Chưa có công việc nào: {e}")
        
        # Test query reports với schema mới
        print("\n📊 Danh sách báo cáo:")
        try:
            result = session.execute(text("SELECT id, title, report_type, status FROM reports LIMIT 5"))
            for row in result:
                print(f"  - {row.id}: {row.title} - {row.report_type} - {row.status}")
        except Exception as e:
            print(f"  Chưa có báo cáo nào: {e}")
        
        session.close()
        print("\n✅ Test PostgreSQL database thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test PostgreSQL database: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Test PostgreSQL Database Connection")
    print("=" * 35)
    test_database()