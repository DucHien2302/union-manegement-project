import logging
import os
from datetime import datetime
from .settings import config


def setup_logging():
    """Thiết lập logging cho ứng dụng"""
    
    # Tạo thư mục logs nếu chưa tồn tại
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Cấu hình logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()  # Console output
        ]
    )
    
    # Logger cho ứng dụng
    logger = logging.getLogger('union_management')
    logger.info(f"Application started - {config.APP_NAME} v{config.APP_VERSION}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Lấy logger với tên cụ thể"""
    return logging.getLogger(f'union_management.{name}')