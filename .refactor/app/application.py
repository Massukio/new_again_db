"""
Main application class for the refactored implementation of New Again.
"""

import sys
import os
from PyQt5 import QtWidgets

# Import original code
from app.main_ui import UiMainWindow
from db.initialize_db import initialize_database
from db.database import add_plate_info, get_all_plate_info, update_plate_info, delete_plate_info

# Import refactored implementations
from .main_window import MainWindow
from ..utils.logger import logger
from ..utils.config_manager import ConfigManager
from ..db.database_manager import DatabaseManager


class Application:
    """
    The main application class that initializes and runs the application.
    This class serves as a facade to the original implementation with enhanced
    error handling and logging.
    """
    def __init__(self):
        """Initialize the application with proper exception handling."""
        try:
            # Initialize application
            self.app = QtWidgets.QApplication(sys.argv)

            # Set application name and organization
            self.app.setApplicationName("New Again (Refactored)")
            self.app.setOrganizationName("New Again Co.")

            # Log application startup
            logger.info("Application starting up")

            # Initialize database if needed
            self._check_database()

            # Create main window
            self.main_window = MainWindow()

            # Set up exception handling for Qt
            sys.excepthook = self._handle_exception

        except Exception as e:
            logger.error(f"Error during application initialization: {e}")
            raise

    def _check_database(self):
        """Check and initialize the database if needed."""
        try:
            if not os.path.exists("database.db"):
                logger.info("Database not found, initializing...")
                initialize_database()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        """Global exception handler for unhandled exceptions."""
        logger.error(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

        # Show error dialog to user
        error_msg = QtWidgets.QMessageBox()
        error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        error_msg.setWindowTitle("應用程式錯誤")
        error_msg.setText("發生意外錯誤，應用程式將關閉。")
        error_msg.setDetailedText(str(exc_value))
        error_msg.exec_()

    def run(self):
        """Run the application main loop."""
        try:
            logger.info("Showing main window")
            self.main_window.show()

            # Run the application and capture exit code
            exit_code = self.app.exec_()

            logger.info(f"Application exiting with code {exit_code}")
            sys.exit(exit_code)

        except Exception as e:
            logger.error(f"Error during application execution: {e}")
            raise
