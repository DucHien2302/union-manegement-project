#!/usr/bin/env python3
"""
Test database connection và truy vấn dữ liệu
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def test_database():
    """Test kết nối và truy vấn database"""
    
    try:
        # Kết nối đến database
        db_path = os.path.join(os.path.dirname(__file__), 'data', 'union_management.db')
        database_url = f"sqlite:///{db_path}"
        
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🔗 Kết nối database thành công!")
        
        # Test query members
        print("\n👥 Danh sách thành viên:")
        result = session.execute(text("SELECT member_id, name, email, member_type, status FROM members"))
        for row in result:
            print(f"  - {row.member_id}: {row.name} ({row.email}) - {row.member_type} - {row.status}")
        
        # Test query tasks
        print("\n📋 Danh sách công việc:")
        result = session.execute(text("SELECT task_id, title, priority, status, assigned_to FROM tasks"))
        for row in result:
            print(f"  - {row.task_id}: {row.title} - {row.priority} - {row.status} - Assigned: {row.assigned_to}")
        
        # Test query reports
        print("\n📊 Danh sách báo cáo:")
        result = session.execute(text("SELECT report_id, title, report_type, status, author_id FROM reports"))
        for row in result:
            print(f"  - {row.report_id}: {row.title} - {row.report_type} - {row.status} - Author: {row.author_id}")
        
        session.close()
        print("\n✅ Test database thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test database: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Test Database Connection")
    print("=" * 30)
    test_database()