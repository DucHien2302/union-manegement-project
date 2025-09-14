"""
Migration script để thêm trường created_by vào bảng reports
"""

import sys
import os
from sqlalchemy import text

# Thêm project root vào Python path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)

from infrastructure.database.connection import db_manager

def migrate_add_created_by_column():
    """Thêm cột created_by vào bảng reports"""
    try:
        session = db_manager.get_session()
        
        # Kiểm tra xem cột đã tồn tại chưa
        check_column_query = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='reports' AND column_name='created_by';
        """
        
        result = session.execute(text(check_column_query)).fetchone()
        
        if not result:
            # Thêm cột created_by
            add_column_query = """
                ALTER TABLE reports 
                ADD COLUMN created_by INTEGER;
            """
            session.execute(text(add_column_query))
            
            # Cập nhật giá trị mặc định cho các bản ghi hiện tại
            update_existing_query = """
                UPDATE reports 
                SET created_by = 1 
                WHERE created_by IS NULL;
            """
            session.execute(text(update_existing_query))
            
            session.commit()
            print("✅ Đã thêm cột 'created_by' vào bảng 'reports' thành công!")
        else:
            print("ℹ️ Cột 'created_by' đã tồn tại trong bảng 'reports'")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Lỗi khi thêm cột 'created_by': {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    migrate_add_created_by_column()