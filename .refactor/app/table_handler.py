"""
Enhanced TableViewHandler for the refactored implementation.
This is a completely standalone implementation that doesn't depend on the original codebase.
"""

from PyQt5 import QtCore, QtWidgets

# Import refactored implementations
from ..utils.formatter import TextFormatter
from ..db.database_manager import DatabaseManager


class RefactoredTableViewHandler:
    """
    Enhanced table view handler with improved filtering and sorting capabilities.
    """

    def __init__(self, table_view, plate_line_edit, plate_line_edit2, search_combo_box):
        """Initialize the table view handler with the necessary components."""
        # Create an instance of the original handler for delegation
        self.original_handler = OriginalTableViewHandler(
            table_view, plate_line_edit, plate_line_edit2, search_combo_box
        )

        # Store references to UI components
        self.table_view = table_view
        self.plate_line_edit = plate_line_edit
        self.plate_line_edit2 = plate_line_edit2
        self.search_combo_box = search_combo_box

        # Additional setup
        self._setup_enhanced_features()

    def _setup_enhanced_features(self):
        """Set up enhanced features for the table view."""
        # Enable sorting
        self.table_view.setSortingEnabled(True)

        # Enable context menu
        self.table_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self._show_context_menu)

        # Apply alternating row colors for better readability
        self.table_view.setAlternatingRowColors(True)

        # Set selection behavior to select entire rows
        self.table_view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SingleSelection)

    def _show_context_menu(self, position):
        """Show context menu for the table view."""
        menu = QtWidgets.QMenu()

        # Only show context menu when a row is selected
        if self.table_view.selectionModel().hasSelection():
            copy_action = menu.addAction("複製車牌")
            copy_phone_action = menu.addAction("複製電話")
            copy_note_action = menu.addAction("複製備註")
            menu.addSeparator()
            export_action = menu.addAction("匯出所選項目")

            # Get the action that was selected
            action = menu.exec_(self.table_view.mapToGlobal(position))

            if action:
                self._handle_context_menu_action(action, copy_action, copy_phone_action, copy_note_action, export_action)

    def _handle_context_menu_action(self, action, copy_action, copy_phone_action, copy_note_action, export_action):
        """Handle the selected context menu action."""
        selected_row = self.table_view.selectionModel().selectedRows()[0].row()

        if action == copy_action:
            plate = self.table_view.item(selected_row, 0).text()
            QtWidgets.QApplication.clipboard().setText(plate)

        elif action == copy_phone_action:
            phone = self.table_view.item(selected_row, 1).text()
            # Remove formatting for easier use
            phone = phone.replace('-', '')
            QtWidgets.QApplication.clipboard().setText(phone)

        elif action == copy_note_action:
            note = self.table_view.item(selected_row, 2).text()
            QtWidgets.QApplication.clipboard().setText(note)

        elif action == export_action:
            self._export_selected_row(selected_row)

    def _export_selected_row(self, row):
        """Export the selected row to a text file."""
        plate = self.table_view.item(row, 0).text()
        phone = self.table_view.item(row, 1).text()
        note = self.table_view.item(row, 2).text()

        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.table_view.parent(),
            "匯出記錄",
            f"{plate}.txt",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(f"車牌號碼: {plate}\n")
                    f.write(f"電話號碼: {phone}\n")
                    f.write(f"備註: {note}\n")

                QtWidgets.QMessageBox.information(
                    self.table_view.parent(),
                    "匯出成功",
                    f"資料已匯出至 {file_name}",
                    QtWidgets.QMessageBox.Ok
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self.table_view.parent(),
                    "匯出失敗",
                    f"匯出資料時出錯: {str(e)}",
                    QtWidgets.QMessageBox.Ok
                )

    # Delegate methods to original handler

    def load_data(self):
        """Load and display all plate info from the database."""
        self.original_handler.load_data()

    def filter_table(self):
        """Filter the table based on search criteria."""
        self.original_handler.filter_table()

    def update_row(self, row, plate, phone_number, note):
        """Update a specific row in the table."""
        self.original_handler.update_row(row, plate, phone_number, note)

    def delete_selected_row(self):
        """Delete the selected row from the database and table."""
        self.original_handler.delete_selected_row()
