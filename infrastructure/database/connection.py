import os
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from config.settings import AppConfig


class DatabaseConfig:
    """Cấu hình kết nối database PostgreSQL"""
    
    def __init__(self):
        self.config = AppConfig()
        
    def get_connection_string(self, include_db: bool = True) -> str:
        """Tạo connection string cho PostgreSQL"""
        if include_db:
            return self.config.get_database_url()
        else:
            return self.config.get_database_url_without_db()
    
    def get_database_name(self) -> str:
        """Lấy tên database"""
        return self.config.DB_NAME


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
        try:
            # Kết nối đến master database để kiểm tra
            engine = self.get_engine(include_db=False)
            with engine.connect() as conn:
                result = conn.execute(
                    text(f"SELECT 1 FROM pg_database WHERE datname = '{self.config.get_database_name()}'")
                )
                return result.fetchone() is not None
        except Exception as e:
            print(f"❌ Error checking database existence: {e}")
            return False
    
    def create_database(self) -> bool:
        """Tạo database nếu chưa tồn tại"""
        try:
            if self.check_database_exists():
                print(f"✅ Database '{self.config.get_database_name()}' already exists")
                return True
            
            print(f"🔧 Creating database '{self.config.get_database_name()}'...")
            
            # Sử dụng SQLAlchemy để tạo database
            from sqlalchemy import create_engine
            engine = create_engine(self.config.get_connection_string(include_db=False))
            with engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE {self.config.get_database_name()}"))
            
            print(f"✅ Database '{self.config.get_database_name()}' created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    
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
                print("✅ PostgreSQL connection successful!")
                return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


# Base class cho các SQLAlchemy models
Base = declarative_base()
metadata = MetaData()

# Global database manager instance
db_manager = DatabaseManager()