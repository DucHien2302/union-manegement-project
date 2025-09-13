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
from infrastructure.database.connection import Base, db_manager
from infrastructure.database.models import MemberModel, ReportModel, TaskModel


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
        print("🎉 PostgreSQL database initialization completed!")
        return True
    else:
        print("❌ PostgreSQL database initialization failed!")
        return False


if __name__ == "__main__":
    # Chạy script này để khởi tạo database
    init_database()