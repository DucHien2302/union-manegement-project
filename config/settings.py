import os
from typing import Optional


class AppConfig:
    """Cấu hình ứng dụng"""
    
    # Database settings
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "UnionManagementDB")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "sa")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "P@ssw0rd")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    
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
        """Get complete database connection URL for SQL Server"""
        from urllib.parse import quote_plus
        
        # Kiểm tra nếu sử dụng Windows Authentication
        if not cls.DB_USERNAME or not cls.DB_PASSWORD:
            # Windows Authentication
            driver_encoded = quote_plus(cls.DB_DRIVER)
            return (
                f"mssql+pyodbc://@{cls.DB_SERVER}/{cls.DB_NAME}?"
                f"driver={driver_encoded}&"
                f"Trusted_Connection=yes&"
                f"TrustServerCertificate=yes"
            )
        else:
            # SQL Server Authentication
            password_encoded = quote_plus(cls.DB_PASSWORD)
            driver_encoded = quote_plus(cls.DB_DRIVER)
            
            return (
                f"mssql+pyodbc://{cls.DB_USERNAME}:{password_encoded}@"
                f"{cls.DB_SERVER}/{cls.DB_NAME}?"
                f"driver={driver_encoded}&"
                f"TrustServerCertificate=yes&"
                f"Encrypt=no"
            )
    
    @classmethod
    def get_database_url_without_db(cls) -> str:
        """Get connection URL to master database (for creating database)"""
        from urllib.parse import quote_plus
        
        # Kiểm tra nếu sử dụng Windows Authentication
        if not cls.DB_USERNAME or not cls.DB_PASSWORD:
            # Windows Authentication
            driver_encoded = quote_plus(cls.DB_DRIVER)
            return (
                f"mssql+pyodbc://@{cls.DB_SERVER}/master?"
                f"driver={driver_encoded}&"
                f"Trusted_Connection=yes&"
                f"TrustServerCertificate=yes"
            )
        else:
            # SQL Server Authentication
            password_encoded = quote_plus(cls.DB_PASSWORD)
            driver_encoded = quote_plus(cls.DB_DRIVER)
            
            return (
                f"mssql+pyodbc://{cls.DB_USERNAME}:{password_encoded}@"
                f"{cls.DB_SERVER}/master?"
                f"driver={driver_encoded}&"
                f"TrustServerCertificate=yes&"
                f"Encrypt=no"
            )
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        required_settings = [
            cls.DB_SERVER,
            cls.DB_NAME,
            cls.DB_USERNAME,
            cls.DB_PASSWORD
        ]
        
        return all(setting for setting in required_settings)


# Global config instance
config = AppConfig()