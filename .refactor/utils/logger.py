"""
Enhanced logging module for the refactored implementation.
This module extends the original logger with additional features.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Import original logger
from app.logger import logger as original_logger


class EnhancedLogger:
    """
    Enhanced logging functionality that extends the original logger.
    Adds features like application event tracking and error aggregation.
    """

    LOG_DIR = "logs"

    @staticmethod
    def setup():
        """Set up the enhanced logger."""
        # Create logs directory if it doesn't exist
        os.makedirs(EnhancedLogger.LOG_DIR, exist_ok=True)

        # Create application event log
        app_handler = RotatingFileHandler(
            os.path.join(EnhancedLogger.LOG_DIR, "application.log"),
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        app_handler.setLevel(logging.INFO)
        app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        app_handler.setFormatter(app_formatter)

        # Add the handler to the original logger
        original_logger.addHandler(app_handler)

        return original_logger

    @staticmethod
    def get_logger():
        """Get the enhanced logger instance."""
        return original_logger


# Set up and export the logger
logger = EnhancedLogger.setup()
