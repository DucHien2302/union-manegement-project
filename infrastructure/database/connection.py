import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional


class DatabaseConfig:
    """Cấu hình kết nối database"""
    
    def __init__(self):
        # Sử dụng SQLite làm database mặc định để đơn giản
        self.db_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'data', 'union_management.db'
        )
        
    def get_connection_string(self) -> str:
        """Tạo connection string cho SQLite"""
        return f"sqlite:///{self.db_path}"


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
    
    def get_engine(self):
        """Lấy SQLAlchemy engine"""
        if self._engine is None:
            connection_string = self.config.get_connection_string()
            self._engine = create_engine(
                connection_string,
                echo=False,  # Set True để debug SQL queries
                pool_pre_ping=True,
                pool_recycle=300
                # SQLite uses different isolation levels, removing unsupported READ_COMMITTED
            )
        return self._engine
    
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
            engine = self.get_engine()
            connection = engine.connect()
            connection.close()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False


# Base class cho các SQLAlchemy models
Base = declarative_base()
metadata = MetaData()

# Global database manager instance
db_manager = DatabaseManager()