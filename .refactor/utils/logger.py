"""
Enhanced logging module for the refactored implementation.
This is a standalone implementation that doesn't depend on the original codebase.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    """
    Standalone logging functionality for the refactored application.
    Includes features like application event tracking and error aggregation.
    """

    LOG_DIR = "logs"

    @staticmethod
    def setup():
        """Set up the logger."""
        # Create logs directory if it doesn't exist
        os.makedirs(Logger.LOG_DIR, exist_ok=True)

        # Create the logger
        logger = logging.getLogger('new_again')
        logger.setLevel(logging.DEBUG)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Create debug file handler
        debug_handler = RotatingFileHandler(
            os.path.join(Logger.LOG_DIR, "debug.log"),
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        debug_handler.setFormatter(debug_formatter)
        logger.addHandler(debug_handler)

        # Create error file handler
        error_handler = RotatingFileHandler(
            os.path.join(Logger.LOG_DIR, "error.log"),
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(debug_formatter)
        logger.addHandler(error_handler)

        # Create application event log
        app_handler = RotatingFileHandler(
            os.path.join(Logger.LOG_DIR, "application.log"),
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        app_handler.setLevel(logging.INFO)
        app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        app_handler.setFormatter(app_formatter)
        logger.addHandler(app_handler)

        return logger

    @staticmethod
    def get_logger():
        """Get the logger instance."""
        return logger


# Set up and export the logger
logger = Logger.setup()
