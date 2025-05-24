"""
Add/Modify plate dialog for the refactored implementation.
This module extends the original AddPlateDialog with improvements.
"""

from PyQt5 import QtWidgets

# Import original code
from app.add_plate_dialog import AddPlateDialog as OriginalAddPlateDialog
from app.logger import logger
from db.database import plate_exists, plate_and_phone_exists, add_plate_info, plate_and_phone_note_exists

# Import refactored implementations
from ..utils.formatter import TextFormatter
from ..db.database_manager import DatabaseManager


class RefactoredAddPlateDialog(OriginalAddPlateDialog):
    """
    Enhanced dialog for adding or modifying plate information.
    Extends the original dialog with improved validation and user feedback.
    """

    def __init__(self, parent=None, plate_type='add'):
        """Initialize the dialog with the specified plate type."""
        super(RefactoredAddPlateDialog, self).__init__(parent, plate_type)

        # Update window title based on operation
        if plate_type == 'add':
            self.setWindowTitle("新增車牌資料")
        else:
            self.setWindowTitle("修改車牌資料")

        # Additional setup specific to refactored implementation
        self._setup_additional_validation()

    def _setup_additional_validation(self):
        """Set up additional validation for input fields."""
        # Validate plate part 1 (letters)
        self.plate_part1_line_edit.textChanged.connect(self._validate_plate_part1)

        # Validate plate part 2 (numbers)
        self.plate_part2_line_edit.textChanged.connect(self._validate_plate_part2)

        # Validate phone number
        self.phone_line_edit.textChanged.connect(self._validate_phone_number)

    def _validate_plate_part1(self):
        """Validate the first part of the plate number (typically letters)."""
        text = self.plate_part1_line_edit.text().upper()
        self.plate_part1_line_edit.setText(text)

        # Set stylesheet based on validity
        if text and not any(char.isalnum() for char in text):
            self.plate_part1_line_edit.setStyleSheet("background-color: #ffcccc;")
        else:
            self.plate_part1_line_edit.setStyleSheet("")

    def _validate_plate_part2(self):
        """Validate the second part of the plate number (typically numbers)."""
        text = self.plate_part2_line_edit.text().upper()
        self.plate_part2_line_edit.setText(text)

        # Set stylesheet based on validity
        if text and not any(char.isalnum() for char in text):
            self.plate_part2_line_edit.setStyleSheet("background-color: #ffcccc;")
        else:
            self.plate_part2_line_edit.setStyleSheet("")

    def _validate_phone_number(self):
        """Validate the phone number input."""
        text = self.phone_line_edit.text()

        # Allow only digits and hyphens
        filtered_text = ''.join(c for c in text if c.isdigit() or c == '-')
        if filtered_text != text:
            self.phone_line_edit.setText(filtered_text)

        # Set stylesheet based on validity
        if filtered_text and not any(c.isdigit() for c in filtered_text):
            self.phone_line_edit.setStyleSheet("background-color: #ffcccc;")
        else:
            self.phone_line_edit.setStyleSheet("")

    def accept(self):
        """Handle the OK button click with enhanced validation."""
        # Get input values
        part1 = self.plate_part1_line_edit.text().strip().upper()
        part2 = self.plate_part2_line_edit.text().strip().upper()
        phone_number = self.phone_line_edit.text().strip()
        note = self.note_text_edit.toPlainText().strip()

        # Validate inputs
        if not self._validate_inputs(part1, part2, phone_number):
            return

        # Check for duplicates with improved error messages
        if not self._check_for_duplicates(part1, part2, phone_number, note):
            return

        # Process the data based on operation type
        if self.plate_type == 'add':
            self._add_plate_info(part1, part2, phone_number, note)
        else:
            self._update_plate_info(part1, part2, phone_number, note)

        # Close the dialog
        super(RefactoredAddPlateDialog, self).accept()

    def _validate_inputs(self, part1, part2, phone_number):
        """Validate the input fields."""
        if not part1 or not part2:
            QtWidgets.QMessageBox.warning(
                self, '警告', '車牌號碼不可為空',
                QtWidgets.QMessageBox.Ok
            )
            return False

        if not phone_number:
            QtWidgets.QMessageBox.warning(
                self, '警告', '電話號碼不可為空',
                QtWidgets.QMessageBox.Ok
            )
            return False

        return True

    def _check_for_duplicates(self, part1, part2, phone_number, note):
        """Check for duplicate entries in the database."""
        try:
            db_manager = DatabaseManager()

            # For modification, we don't need to check for duplicates of the same entry
            if self.plate_type == 'modify':
                return True

            # Use the original implementation through our refactored DatabaseManager
            if db_manager.plate_and_phone_exists(part1, part2, phone_number):
                QtWidgets.QMessageBox.warning(
                    self, '警告', f'車牌號碼 {part1}-{part2} 與電話號碼 {phone_number} 的組合已存在',
                    QtWidgets.QMessageBox.Ok
                )
                return False

            if db_manager.plate_and_phone_note_exists(part1, part2, phone_number, note):
                QtWidgets.QMessageBox.warning(
                    self, '警告', f'車牌號碼 {part1}-{part2} 與電話號碼 {phone_number} 和備註的組合已存在',
                    QtWidgets.QMessageBox.Ok
                )
                return False

            return True
        except Exception as e:
            logger.error(f"Error checking for duplicates: {e}")
            QtWidgets.QMessageBox.critical(
                self, '錯誤', f'檢查資料時發生錯誤: {str(e)}',
                QtWidgets.QMessageBox.Ok
            )
            return False

    def _add_plate_info(self, part1, part2, phone_number, note):
        """Add a new plate info to the database."""
        try:
            db_manager = DatabaseManager()
            if db_manager.add_plate_info(part1, part2, phone_number, note):
                logger.info(f"Added plate info: {part1}-{part2} with phone: {phone_number}")
            else:
                logger.error(f"Failed to add plate info: {part1}-{part2}")
        except Exception as e:
            logger.error(f"Error adding plate info: {e}")
            QtWidgets.QMessageBox.critical(
                self, '錯誤', f'新增資料時發生錯誤: {str(e)}',
                QtWidgets.QMessageBox.Ok
            )

    def _update_plate_info(self, part1, part2, phone_number, note):
        """Update an existing plate info in the database."""
        try:
            db_manager = DatabaseManager()
            if db_manager.update_plate_info(part1, part2, phone_number, note):
                logger.info(f"Updated plate info: {part1}-{part2} with phone: {phone_number}")
            else:
                logger.error(f"Failed to update plate info: {part1}-{part2}")
        except Exception as e:
            logger.error(f"Error updating plate info: {e}")
            QtWidgets.QMessageBox.critical(
                self, '錯誤', f'更新資料時發生錯誤: {str(e)}',
                QtWidgets.QMessageBox.Ok
            )
