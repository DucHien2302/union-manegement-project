"""
Base Controller
Base class for all controllers with common functionality
"""

import logging
from config.logging_config import setup_logging


class BaseController:
    """Base controller class with common functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        setup_logging()