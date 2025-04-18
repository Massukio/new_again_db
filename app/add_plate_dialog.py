from PyQt5 import QtWidgets, QtCore, QtGui
from app.logger import logger
from db.database import plate_exists, plate_and_phone_exists, add_plate_info, plate_and_phone_note_exists
import sqlite3

class AddPlateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, plate_type='add'):
        super(AddPlateDialog, self).__init__(parent)
        self.plate_type = plate_type
        self.setWindowTitle("新增車牌資料")
        self.resize(801, 267)

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.grid_layout_widget = QtWidgets.QWidget(self)
        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.grid_layout_widget)

        self.plate_part1_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.plate_part1_line_edit.setFont(font)
        self.plate_part1_line_edit.setMaxLength(4)
        self.plate_part1_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.plate_part1_line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.plate_part1_line_edit.textChanged.connect(self.convert_to_upper)
        self.grid_layout.addWidget(self.plate_part1_line_edit, 1, 0, 1, 1)

        self.label = QtWidgets.QLabel(self.grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("車牌號碼")
        self.grid_layout.addWidget(self.label, 0, 0, 1, 2)

        self.plate_part2_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.plate_part2_line_edit.setFont(font)
        self.plate_part2_line_edit.setMaxLength(4)
        self.plate_part2_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.plate_part2_line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.plate_part2_line_edit.textChanged.connect(self.convert_to_upper)
        self.grid_layout.addWidget(self.plate_part2_line_edit, 1, 1, 1, 1)

        self.grid_layout_widget_2 = QtWidgets.QWidget(self)
        self.grid_layout_2 = QtWidgets.QGridLayout(self.grid_layout_widget_2)
        self.grid_layout_2.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.grid_layout_widget_2)

        self.phone_number_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.phone_number_line_edit.setFont(font)
        self.phone_number_line_edit.setMaxLength(10)
        self.phone_number_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.phone_number_line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.phone_number_line_edit.setValidator(QtGui.QIntValidator())
        self.grid_layout_2.addWidget(self.phone_number_line_edit, 1, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setText("電話號碼")
        self.grid_layout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.grid_layout_widget_3 = QtWidgets.QWidget(self)
        self.grid_layout_3 = QtWidgets.QGridLayout(self.grid_layout_widget_3)
        self.grid_layout_3.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.grid_layout_widget_3)

        self.note_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.note_line_edit.setFont(font)
        self.note_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.note_line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.grid_layout_3.addWidget(self.note_line_edit, 1, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setText("備註")
        self.grid_layout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("確定")
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("取消")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

        self.apply_modern_style()

    def resizeEvent(self, event):
        self.adjust_font_size()
        super(AddPlateDialog, self).resizeEvent(event)

    def adjust_font_size(self):
        base_font_size = 30
        font_size = max(base_font_size, int(self.height() * 0.03))
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.plate_part1_line_edit.setFont(font)
        self.plate_part2_line_edit.setFont(font)
        self.phone_number_line_edit.setFont(font)
        self.note_line_edit.setFont(font)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """Handle key press events."""
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            focus_widget = self.focusWidget()
            if focus_widget == self.phone_number_line_edit:
                self.note_line_edit.setFocus()
            elif focus_widget == self.note_line_edit:
                self.accept()
            elif isinstance(focus_widget, QtWidgets.QLineEdit):
                self.focusNextChild()
        else:
            super(AddPlateDialog, self).keyPressEvent(event)

    def accept(self) -> None:
        """Handle the accept event."""
        plate_info = self.get_plate_info()
        logger.debug(f"Plate Info: {plate_info}")

        if self.plate_type == 'add':
            if plate_and_phone_exists(plate_info[0], plate_info[1], plate_info[2]):
                error_dialog = QtWidgets.QMessageBox()
                error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
                error_dialog.setWindowTitle("錯誤")
                error_dialog.setText("此車牌號碼和電話號碼已存在。")
                error_dialog.addButton("確定", QtWidgets.QMessageBox.AcceptRole)
                error_dialog.exec_()
            elif plate_exists(plate_info[0], plate_info[1]):
                warning_dialog = QtWidgets.QMessageBox()
                warning_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                warning_dialog.setWindowTitle("警告")
                warning_dialog.setText("此車牌號碼已存在但電話號碼不同。是否繼續保存？")
                yes_button = warning_dialog.addButton("是", QtWidgets.QMessageBox.YesRole)
                no_button = warning_dialog.addButton("否", QtWidgets.QMessageBox.NoRole)
                warning_dialog.exec_()
                if warning_dialog.clickedButton() == yes_button:
                    add_plate_info(plate_info[0], plate_info[1], plate_info[2], plate_info[3])
                    self.done(QtWidgets.QDialog.Accepted)
                else:
                    self.done(QtWidgets.QDialog.Rejected)
            else:
                add_plate_info(plate_info[0], plate_info[1], plate_info[2], plate_info[3])
                self.done(QtWidgets.QDialog.Accepted)

        else:  # plate_type == 'edit'
            if plate_and_phone_note_exists(plate_info[0], plate_info[1], plate_info[2], plate_info[3]):
                error_dialog = QtWidgets.QMessageBox()
                error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
                error_dialog.setWindowTitle("錯誤")
                error_dialog.setText("此車牌號碼、電話號碼與相同備註已經存在。")
                error_dialog.addButton("確定", QtWidgets.QMessageBox.AcceptRole)
                error_dialog.exec_()
            else:
                add_plate_info(plate_info[0], plate_info[1], plate_info[2], plate_info[3])
                self.done(QtWidgets.QDialog.Accepted)

    def reject(self) -> None:
        """Handle the reject event."""
        super(AddPlateDialog, self).reject()

    def get_plate_info(self) -> tuple:
        """Get the plate info from the input fields."""
        return self.plate_part1_line_edit.text(), self.plate_part2_line_edit.text(), self.phone_number_line_edit.text(), self.note_line_edit.text()

    def convert_to_upper(self, text: str) -> None:
        """Convert the input text to uppercase."""
        sender = self.sender()
        sender.blockSignals(True)
        sender.setText(text.upper())
        sender.blockSignals(False)

    def apply_modern_style(self):
        base_font_size = 18  # Default base font size
        style_sheet = f"""
        QDialog {{
            background-color: #f0f0f0;
            font-family: 'Microsoft YaHei', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }}
        QLineEdit {{
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: {self.parent().input_font_size}px;
        }}
        QLabel {{
            font-size: {base_font_size}px;
            color: #333;
        }}
        QPushButton {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            font-size: {self.parent().button_font_size}px;
            margin: 4px 2px;
            border-radius: 8px;
        }}
        QPushButton:hover {{
            background-color: #45a049;
        }}
        """
        self.setStyleSheet(style_sheet)
        self.adjust_font_size()
