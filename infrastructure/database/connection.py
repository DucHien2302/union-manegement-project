import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional


import os
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from config.settings import AppConfig


import os
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from config.settings import AppConfig


class DatabaseConfig:
    """Cấu hình kết nối database"""
    
    def __init__(self):
        self.config = AppConfig()
        self.use_sqlite_fallback = False
        
    def get_connection_string(self, include_db: bool = True) -> str:
        """Tạo connection string cho SQL Server hoặc SQLite fallback"""
        if self.use_sqlite_fallback:
            # SQLite fallback
            db_path = os.path.join(
                os.path.dirname(__file__), '..', '..', 'data', 'union_management.db'
            )
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return f"sqlite:///{db_path}"
        else:
            # SQL Server - sử dụng method từ AppConfig
            if include_db:
                return self.config.get_database_url()
            else:
                return self.config.get_database_url_without_db()
    
    def get_database_name(self) -> str:
        """Lấy tên database"""
        return self.config.DB_NAME
    
    def enable_sqlite_fallback(self):
        """Bật chế độ SQLite fallback"""
        self.use_sqlite_fallback = True
        print("⚠️ Switching to SQLite fallback mode")


class DatabaseManager:
    """Quản lý kết nối database"""
    
    _instance: Optional['DatabaseManager'] = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.config = DatabaseConfig()
            self.initialized = True
    
    def get_engine(self, include_db: bool = True):
        """Lấy SQLAlchemy engine"""
        if self._engine is None or not include_db:
            connection_string = self.config.get_connection_string(include_db)
            engine = create_engine(
                connection_string,
                echo=False,  # Set True để debug SQL queries
                pool_pre_ping=True,
                pool_recycle=300
            )
            if include_db:
                self._engine = engine
            return engine
        return self._engine
    
    def check_database_exists(self) -> bool:
        """Kiểm tra database có tồn tại không"""
        if self.config.use_sqlite_fallback:
            # SQLite: database file tồn tại = database tồn tại
            return True
            
        try:
            # Kết nối đến master database để kiểm tra
            engine = self.get_engine(include_db=False)
            with engine.connect() as conn:
                result = conn.execute(
                    text(f"SELECT database_id FROM sys.databases WHERE name = '{self.config.get_database_name()}'")
                )
                return result.fetchone() is not None
        except Exception as e:
            print(f"❌ Error checking database existence: {e}")
            return False
    
    def create_database(self) -> bool:
        """Tạo database nếu chưa tồn tại"""
        if self.config.use_sqlite_fallback:
            # SQLite: không cần tạo database riêng
            print("✅ Using SQLite database")
            return True
            
        try:
            if self.check_database_exists():
                print(f"✅ Database '{self.config.get_database_name()}' already exists")
                return True
            
            print(f"🔧 Creating database '{self.config.get_database_name()}'...")
            
            # Sử dụng pyodbc trực tiếp để tạo database
            import pyodbc
            
            # Tạo connection string cho pyodbc
            if not self.config.config.DB_USERNAME:
                # Windows Authentication
                conn_str = (
                    f"DRIVER={{{self.config.config.DB_DRIVER}}};"
                    f"SERVER={self.config.config.DB_SERVER};"
                    f"DATABASE=master;"
                    f"Trusted_Connection=yes;"
                )
            else:
                # SQL Authentication
                conn_str = (
                    f"DRIVER={{{self.config.config.DB_DRIVER}}};"
                    f"SERVER={self.config.config.DB_SERVER};"
                    f"DATABASE=master;"
                    f"UID={self.config.config.DB_USERNAME};"
                    f"PWD={self.config.config.DB_PASSWORD};"
                )
            
            # Tạo database với pyodbc
            with pyodbc.connect(conn_str, autocommit=True) as conn:
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE [{self.config.get_database_name()}]")
                
            print(f"✅ Database '{self.config.get_database_name()}' created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            # Try to fallback to SQLite
            print("🔄 Attempting to use SQLite as fallback...")
            self.config.enable_sqlite_fallback()
            self._engine = None  # Reset engine to use new connection string
            return True
    
    def get_session_factory(self):
        """Lấy session factory"""
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = sessionmaker(bind=engine)
        return self._session_factory
    
    def get_session(self):
        """Tạo database session mới"""
        session_factory = self.get_session_factory()
        return session_factory()
    
    def test_connection(self) -> bool:
        """Test kết nối database"""
        try:
            # Tạo database nếu chưa có
            if not self.create_database():
                return False
                
            # Test kết nối đến database
            engine = self.get_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            # Try SQLite fallback if SQL Server fails
            if not self.config.use_sqlite_fallback:
                print("🔄 Trying SQLite fallback...")
                self.config.enable_sqlite_fallback()
                self._engine = None  # Reset engine
                return self.test_connection()  # Recursive call with SQLite
            return False


# Base class cho các SQLAlchemy models
Base = declarative_base()
metadata = MetaData()

# Global database manager instance
db_manager = DatabaseManager()