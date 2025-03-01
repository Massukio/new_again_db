import os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from app.main_ui import UiMainWindow
from app.add_plate_dialog import AddPlateDialog
from app.table_view_handler import TableViewHandler
from app.logger import logger
from db.database import add_plate_info, get_all_plate_info, update_plate_info, delete_plate_info
from db.initialize_db import initialize_database

class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui(self)
        self.add_button.clicked.connect(self.show_add_plate_dialog)
        self.modify_button.clicked.connect(self.modify_selected_row)
        self.connect_button.clicked.connect(self.check_database_exists)
        self.delete_button.clicked.connect(self.confirm_delete_selected_row)
        self.backup_button.clicked.connect(self.backup_database)
        self.table_handler = TableViewHandler(
            self.table_view, self.plate_line_edit, self.plate_line_edit2, self.search_combo_box)

    def show_add_plate_dialog(self):
        dialog = AddPlateDialog(self)
        while dialog.exec_() == QtWidgets.QDialog.Accepted:
            plate_info = dialog.get_plate_info()
            logger.debug(f"Adding plate info: {plate_info}")
            add_plate_info(
                part1=plate_info[0],
                part2=plate_info[1],
                phone_number=plate_info[2]
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

    def check_database_exists(self):
        if not os.path.exists("database.db"):
            reply = QtWidgets.QMessageBox.question(
                None, '資料庫不存在', '資料庫不存在，是否要初始化資料庫？',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                initialize_database()
                QtWidgets.QMessageBox.information(
                    None, '成功', '資料庫已初始化。',
                    QtWidgets.QMessageBox.Ok
                )
            else:
                QtWidgets.QMessageBox.critical(
                    None, '錯誤', '資料庫不存在，請先新增資料。',
                    QtWidgets.QMessageBox.Ok
                )
        else:
            QtWidgets.QMessageBox.information(
                None, '成功', '資料庫已連接。',
                QtWidgets.QMessageBox.Ok
            )

    def modify_selected_row(self):
        selected_row = self.table_view.currentRow()
        if selected_row >= 0:
            plate_info = self.table_view.item(selected_row, 0).text()
            phone_number = self.table_view.item(selected_row, 1).text()
            part1, part2 = plate_info.split('-')

            dialog = AddPlateDialog(self)
            dialog.plate_part1_line_edit.setText(part1)
            dialog.plate_part2_line_edit.setText(part2)
            dialog.phone_number_line_edit.setText(phone_number)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                new_part1, new_part2, new_phone_number = dialog.get_plate_info()
                update_plate_info(new_part1, new_part2, new_phone_number)
                self.table_view.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(f"{new_part1}-{new_part2}"))
                self.table_view.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(new_phone_number))

    def backup_database(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        current_date = datetime.now().strftime("%Y%m%d")
        default_filename = f"{current_date}_backup_database.json"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Backup Database", default_filename, "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            try:
                with open("database.json", "r", encoding="utf-8") as src:
                    with open(file_path, "w", encoding="utf-8") as dst:
                        dst.write(src.read())
                QtWidgets.QMessageBox.information(None, '成功', '資料庫備份成功。', QtWidgets.QMessageBox.Ok)
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, '錯誤', f'資料庫備份失敗: {e}', QtWidgets.QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
