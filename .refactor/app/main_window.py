"""
Main window implementation for the refactored New Again application.
This is a standalone implementation that doesn't depend on the original codebase.
"""

import os
import json
import sqlite3
import shutil
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

# Import refactored standalone modules
from .ui_main_window import UiMainWindow
from ..utils.logger import logger

# Import refactored implementations
from .dialogs.font_size_dialog import FontSizeDialog
from .dialogs.add_plate_dialog import RefactoredAddPlateDialog
from .table_handler import RefactoredTableViewHandler
from ..utils.config_manager import ConfigManager
from ..utils.formatter import TextFormatter
from ..db.database_manager import DatabaseManager


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    """
    Main window implementation that extends the original UiMainWindow.
    This class preserves all functionality while improving code organization.
    """

    DATABASE_FILE = "database.db"
    CONFIG_FILE = "config.json"

    def __init__(self, parent=None):
        """Initialize the main window with all required components."""
        super(MainWindow, self).__init__(parent)

        # Initialize database manager
        self.db_manager = DatabaseManager()

        # Initialize configuration
        config = ConfigManager.load_config()
        self.button_font_size = config.get('button_font_size', 20)
        self.table_font_size = config.get('table_font_size', 25)
        self.input_font_size = config.get('input_font_size', 30)

        # Setup UI
        self.setup_ui(self)
        self.adjust_window_size()
        self.apply_modern_style()

        # Connect event handlers
        self.connect_signals()

        # Initialize the application state
        self.pre_check_database()
        self.initialize_table_handler()
        self.set_background_color()

    def connect_signals(self):
        """Connect all signal handlers to their respective slots."""
        self.add_button.clicked.connect(self.show_add_plate_dialog)
        self.modify_button.clicked.connect(self.modify_selected_row)
        self.connect_button.clicked.connect(self.check_database_location)
        self.delete_button.clicked.connect(self.confirm_delete_selected_row)
        self.backup_button.clicked.connect(self.backup_database)
        self.action_adjust_font_size.triggered.connect(self.show_font_size_dialog)

    def pre_check_database(self):
        """Check if the database exists and create it if necessary."""
        from ..db.init import initialize_database

        if not os.path.exists(self.DATABASE_FILE):
            initialize_database()
            QtWidgets.QMessageBox.information(
                self, '資料庫初始化', f'資料庫已創建於: {os.path.abspath(self.DATABASE_FILE)}',
                QtWidgets.QMessageBox.Ok
            )
        else:
            try:
                conn = sqlite3.connect(self.DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plate_info'")
                if cursor.fetchone() is None:
                    raise sqlite3.OperationalError("Table 'plate_info' does not exist.")
                conn.close()
            except sqlite3.Error as e:
                QtWidgets.QMessageBox.critical(
                    self, '資料庫錯誤', f'資料庫結構錯誤: {str(e)}',
                    QtWidgets.QMessageBox.Ok
                )
                initialize_database()

    def initialize_table_handler(self):
        """Initialize the table view handler with the refactored implementation."""
        self.table_handler = RefactoredTableViewHandler(
            self.table_view,
            self.table_font_size
        )

    def load_font_size_config(self):
        """Load font size configuration from the config file."""
        try:
            config = ConfigManager.load_config()
            self.button_font_size = config.get('button_font_size', 20)
            self.table_font_size = config.get('table_font_size', 25)
            self.input_font_size = config.get('input_font_size', 30)
        except Exception as e:
            logger.error(f"Failed to load font size config: {e}")

    def save_font_size_config(self):
        """Save font size configuration to the config file."""
        config = {
            'button_font_size': self.button_font_size,
            'table_font_size': self.table_font_size,
            'input_font_size': self.input_font_size
        }
        try:
            ConfigManager.save_config(config)
        except Exception as e:
            logger.error(f"Failed to save font size config: {e}")

    def show_font_size_dialog(self):
        """Show dialog to adjust font sizes."""
        dialog = FontSizeDialog(
            self,
            self.button_font_size,
            self.table_font_size,
            self.input_font_size
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.button_font_size = dialog.get_button_font_size()
            self.table_font_size = dialog.get_table_font_size()
            self.input_font_size = dialog.get_input_font_size()
            self.save_font_size_config()
            self.apply_modern_style()
            self.table_handler.load_data()  # Refresh table with new font size
            QtWidgets.QMessageBox.information(
                self, '字體大小調整', '字體大小已調整，設定已保存',
                QtWidgets.QMessageBox.Ok
            )

    def adjust_window_size(self):
        """Adjust the window size based on screen resolution."""
        screen_size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        window_width = min(1200, int(screen_size.width() * 0.8))
        window_height = min(800, int(screen_size.height() * 0.8))
        self.resize(window_width, window_height)
        self.setMinimumSize(800, 600)

        # Set window title to indicate refactored version
        self.setWindowTitle("車牌管理系統 (Refactored)")

    def apply_modern_style(self):
        """Apply modern styling to the application UI."""
        # Apply button font size
        button_style = f"""
            QPushButton {{
                font-size: {self.button_font_size}px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: 1px solid #2E7D32;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #3e8e41;
            }}
            QPushButton:pressed {{
                background-color: #1B5E20;
            }}
        """
        self.add_button.setStyleSheet(button_style)
        self.modify_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.connect_button.setStyleSheet(button_style)
        self.backup_button.setStyleSheet(button_style)

        # Apply table font size
        table_style = f"""
            QTableWidget {{
                font-size: {self.table_font_size}px;
                border: 1px solid #ccc;
                gridline-color: #ddd;
                alternate-background-color: #f5f5f5;
            }}
            QHeaderView::section {{
                background-color: #f0f0f0;
                font-weight: bold;
                font-size: {self.table_font_size - 2}px;
                padding: 4px;
                border: 1px solid #ccc;
            }}
        """
        self.table_view.setStyleSheet(table_style)

        # Apply input field font size
        input_style = f"""
            QLineEdit, QComboBox {{
                font-size: {self.input_font_size}px;
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 3px;
            }}
        """
        self.plate_filter_line_edit.setStyleSheet(input_style)
        self.plate_filter_line_edit2.setStyleSheet(input_style)
        self.search_combo_box.setStyleSheet(input_style)

    def set_background_color(self):
        """Set the background color for the main window."""
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
        self.setPalette(palette)

    def show_add_plate_dialog(self):
        """Show dialog to add a new plate entry using refactored dialog."""
        dialog = RefactoredAddPlateDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.table_handler.load_data()

    def modify_selected_row(self):
        """Modify the currently selected row using refactored components."""
        selected_rows = self.table_view.selectionModel().selectedRows()

        if not selected_rows:
            QtWidgets.QMessageBox.warning(
                self, '警告', '請先選擇一行資料進行修改',
                QtWidgets.QMessageBox.Ok
            )
            return

        row = selected_rows[0].row()
        plate = self.table_view.item(row, 0).text()
        phone = self.table_view.item(row, 1).text().replace('-', '')  # Remove formatting
        note = self.table_view.item(row, 2).text()

        # Parse plate using TextFormatter
        part1, part2 = TextFormatter.parse_plate_number(plate)

        dialog = RefactoredAddPlateDialog(self, plate_type='modify')
        dialog.plate_part1_line_edit.setText(part1)
        dialog.plate_part2_line_edit.setText(part2)
        dialog.phone_line_edit.setText(phone)
        dialog.note_text_edit.setText(note)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.table_handler.load_data()

    def confirm_delete_selected_row(self):
        """Confirm and delete the selected row."""
        selected_rows = self.table_view.selectionModel().selectedRows()

        if not selected_rows:
            QtWidgets.QMessageBox.warning(
                self, '警告', '請先選擇一行資料進行刪除',
                QtWidgets.QMessageBox.Ok
            )
            return

        row = selected_rows[0].row()
        plate = self.table_view.item(row, 0).text()

        reply = QtWidgets.QMessageBox.question(
            self, '確認刪除',
            f'確定要刪除車牌號碼為 {plate} 的資料嗎？',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.delete_selected_row(row, plate)

    def delete_selected_row(self, row, plate):
        """Delete the selected row from the database using DatabaseManager."""
        try:
            # Parse plate using TextFormatter
            part1, part2 = TextFormatter.parse_plate_number(plate)

            if part1 and part2:
                if self.db_manager.delete_plate_info(part1, part2):
                    self.table_handler.load_data()
                    logger.info(f"Deleted plate info: {plate}")
                else:
                    logger.error(f"Failed to delete plate info: {plate}")
                    QtWidgets.QMessageBox.warning(
                        self, '刪除失敗', f'無法刪除車牌資料: {plate}',
                        QtWidgets.QMessageBox.Ok
                    )
            else:
                logger.error(f"Invalid plate format for deletion: {plate}")
                QtWidgets.QMessageBox.warning(
                    self, '刪除失敗', f'車牌格式錯誤: {plate}',
                    QtWidgets.QMessageBox.Ok
                )
        except Exception as e:
            logger.error(f"Failed to delete plate info: {e}")
            QtWidgets.QMessageBox.critical(
                self, '刪除失敗', f'刪除時出現錯誤: {str(e)}',
                QtWidgets.QMessageBox.Ok
            )

    def backup_database(self):
        """Create a backup of the database."""
        try:
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"database_backup_{timestamp}.db")

            # Copy database file to backup location
            shutil.copy2(self.DATABASE_FILE, backup_file)

            QtWidgets.QMessageBox.information(
                self, '備份成功', f'資料庫已備份至: {os.path.abspath(backup_file)}',
                QtWidgets.QMessageBox.Ok
            )
            logger.info(f"Database backed up to: {backup_file}")
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            QtWidgets.QMessageBox.critical(
                self, '備份失敗', f'備份資料庫時出現錯誤: {str(e)}',
                QtWidgets.QMessageBox.Ok
            )

    def check_database_location(self):
        """Show the current database location."""
        QtWidgets.QMessageBox.information(
            self, '資料庫位置', f'目前資料庫位置:\n{os.path.abspath(self.DATABASE_FILE)}',
            QtWidgets.QMessageBox.Ok
        )
