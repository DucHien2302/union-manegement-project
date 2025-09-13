import os
from typing import Optional


class AppConfig:
    """Cấu hình ứng dụng - chỉ sử dụng PostgreSQL"""
    
    # PostgreSQL settings (duy nhất database được hỗ trợ)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "union_management")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Union Management System")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # File upload settings
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: set = set(os.getenv("ALLOWED_EXTENSIONS", "pdf,doc,docx,xls,xlsx,png,jpg,jpeg").split(","))
    
    @classmethod
    def load_from_env_file(cls, env_file: str = ".env") -> None:
        """Load configuration from .env file"""
        if os.path.exists(env_file):
            from dotenv import load_dotenv
            load_dotenv(env_file)
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get complete database connection URL for PostgreSQL"""
        return (
            f"postgresql+psycopg2://{cls.DB_USERNAME}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )
    
    @classmethod
    def get_database_url_without_db(cls) -> str:
        """Get connection URL to PostgreSQL server without database (for creating database)"""
        return (
            f"postgresql+psycopg2://{cls.DB_USERNAME}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/postgres"
        )
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        required_settings = [
            cls.DB_HOST,
            cls.DB_PORT,
            cls.DB_NAME,
            cls.DB_USERNAME,
            cls.DB_PASSWORD
        ]
        
        return all(setting for setting in required_settings)


# Global config instance
config = AppConfig()