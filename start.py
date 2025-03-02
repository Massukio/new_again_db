import os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from app.main_ui import UiMainWindow
from app.add_plate_dialog import AddPlateDialog
from app.table_view_handler import TableViewHandler
from app.logger import logger
from db.database import add_plate_info, get_all_plate_info, update_plate_info, delete_plate_info
from db.initialize_db import initialize_database
import sqlite3
import shutil

DATABASE_FILE = "database.db"

class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui(self)
        self.adjust_window_size()
        self.add_button.clicked.connect(self.show_add_plate_dialog)
        self.modify_button.clicked.connect(self.modify_selected_row)
        self.connect_button.clicked.connect(self.check_database_location)
        self.delete_button.clicked.connect(self.confirm_delete_selected_row)
        self.backup_button.clicked.connect(self.backup_database)
        self.pre_check_database()
        self.initialize_table_handler()

    def pre_check_database(self):
        if not os.path.exists(DATABASE_FILE):
            initialize_database()
            QtWidgets.QMessageBox.information(
                self, '資料庫初始化', f'資料庫已創建於: {os.path.abspath(DATABASE_FILE)}',
                QtWidgets.QMessageBox.Ok
            )
        else:
            try:
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plate_info'")
                if cursor.fetchone() is None:
                    raise sqlite3.OperationalError("Table 'plate_info' does not exist.")
                conn.close()
            except sqlite3.OperationalError as e:
                logger.error(f"Database error: {e}")
                os.remove(DATABASE_FILE)
                initialize_database()
                QtWidgets.QMessageBox.information(
                    self, '資料庫初始化', f'資料庫已創建於: {os.path.abspath(DATABASE_FILE)}',
                    QtWidgets.QMessageBox.Ok
                )

    def initialize_table_handler(self):
        try:
            self.table_handler = TableViewHandler(
                self.table_view, self.plate_line_edit, self.plate_line_edit2, self.search_combo_box)
        except sqlite3.OperationalError as e:
            logger.error(f"Database error: {e}")
            QtWidgets.QMessageBox.critical(
                self, '資料庫錯誤', '資料庫不存在或無法訪問。請點擊連接按鈕初始化資料庫。',
                QtWidgets.QMessageBox.Ok
            )

    def adjust_window_size(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, int(screen.width() * 0.8), int(screen.height() * 0.8))
        self.setMinimumSize(int(screen.width() * 0.6), int(screen.height() * 0.6))

    def resizeEvent(self, event):
        self.grid_layout_widget.setGeometry(0, 0, int(self.width() * 0.8), int(self.height() * 0.8))
        self.grid_layout_widget_2.setGeometry(int(self.width() * 0.8), 0, int(self.width() * 0.2), int(self.height() * 0.8))
        self.grid_layout_widget_3.setGeometry(0, int(self.height() * 0.8), int(self.width() * 0.8), int(self.height() * 0.2))
        self.grid_layout_widget_6.setGeometry(int(self.width() * 0.8), int(self.height() * 0.8), int(self.width() * 0.2), int(self.height() * 0.2))
        super(MainWindow, self).resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.reset_table_view()
        else:
            super(MainWindow, self).keyPressEvent(event)

    def show_add_plate_dialog(self):
        dialog = AddPlateDialog(self)
        while dialog.exec_() == QtWidgets.QDialog.Accepted:
            plate_info = dialog.get_plate_info()
            logger.debug(f"Adding plate info: {plate_info}")
            add_plate_info(
                part1=plate_info[0],
                part2=plate_info[1],
                phone_number=plate_info[2],
                note=plate_info[3]
            )
            logger.info(f"新增車牌號碼: {plate_info}")
            self.table_handler.load_data()
            dialog = AddPlateDialog(self)

    def confirm_delete_selected_row(self):
        selected_row = self.table_view.currentRow()
        if selected_row >= 0:
            plate_info = self.table_view.item(selected_row, 0).text()
            reply = QtWidgets.QMessageBox.question(
                None, '確認刪除', f"確定要刪除車牌號碼 {plate_info} 嗎？",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.table_handler.delete_selected_row()

    def update_line_edits(self):
        self.plate_line_edit.clear()
        self.plate_line_edit2.clear()
        self.plate_line_edit.setFocus()

        if self.search_combo_box.currentText() == "電話查詢":
            self.plate_line_edit2.hide()
            self.grid_layout_5.addWidget(self.plate_line_edit, 0, 1, 1, 2)
            self.plate_line_edit.setMaxLength(10)
            self.plate_line_edit.setValidator(QtGui.QIntValidator())
        else:
            self.plate_line_edit2.show()
            self.grid_layout_5.addWidget(self.plate_line_edit, 0, 1, 1, 1)
            self.grid_layout_5.addWidget(self.plate_line_edit2, 0, 2, 1, 1)
            self.plate_line_edit.setMaxLength(4)
            self.plate_line_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]{0,4}")))
            self.plate_line_edit2.setMaxLength(4)
            self.plate_line_edit2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]{0,4}")))

    def check_database_location(self):
        QtWidgets.QMessageBox.information(
            self, '資料庫位置', f'資料庫位置: {os.path.abspath(DATABASE_FILE)}',
            QtWidgets.QMessageBox.Ok
        )

    def modify_selected_row(self):
        selected_row = self.table_view.currentRow()
        if selected_row >= 0:
            plate_info = self.table_view.item(selected_row, 0).text()
            phone_number = self.table_view.item(selected_row, 1).text()
            note = self.table_view.item(selected_row, 2).text()
            part1, part2 = plate_info.split('-')

            dialog = AddPlateDialog(self)
            dialog.plate_part1_line_edit.setText(part1)
            dialog.plate_part2_line_edit.setText(part2)
            dialog.phone_number_line_edit.setText(phone_number)
            dialog.note_line_edit.setText(note)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                new_part1, new_part2, new_phone_number, new_note = dialog.get_plate_info()
                update_plate_info(new_part1, new_part2, new_phone_number, new_note)
                self.table_view.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(f"{new_part1}-{new_part2}"))
                self.table_view.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(new_phone_number))
                self.table_view.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(new_note))

    def backup_database(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        current_date = datetime.now().strftime("%Y%m%d")
        default_filename = f"{current_date}_backup_database.db"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Backup Database", default_filename, "SQLite Database Files (*.db);;All Files (*)", options=options)
        if file_path:
            try:
                shutil.copyfile(DATABASE_FILE, file_path)
                QtWidgets.QMessageBox.information(None, '成功', '資料庫備份成功。', QtWidgets.QMessageBox.Ok)
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, '錯誤', f'資料庫備份失敗: {e}', QtWidgets.QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
