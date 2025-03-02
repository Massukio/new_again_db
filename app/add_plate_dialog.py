from PyQt5 import QtWidgets, QtCore, QtGui
from app.logger import logger

class AddPlateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddPlateDialog, self).__init__(parent)
        self.setWindowTitle("新增車牌資料")
        self.resize(801, 267)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(450, 230, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.grid_layout_widget = QtWidgets.QWidget(self)
        self.grid_layout_widget.setGeometry(QtCore.QRect(0, 0, 801, 115))
        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.plate_part1_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.plate_part1_line_edit.setFont(font)
        self.plate_part1_line_edit.setMaxLength(4)
        self.plate_part1_line_edit.textChanged.connect(self.convert_to_upper)
        self.grid_layout.addWidget(self.plate_part1_line_edit, 1, 0, 1, 1)

        self.label = QtWidgets.QLabel(self.grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(20)
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
        self.plate_part2_line_edit.textChanged.connect(self.convert_to_upper)
        self.grid_layout.addWidget(self.plate_part2_line_edit, 1, 1, 1, 1)

        self.grid_layout_widget_2 = QtWidgets.QWidget(self)
        self.grid_layout_widget_2.setGeometry(QtCore.QRect(0, 120, 801, 91))
        self.grid_layout_2 = QtWidgets.QGridLayout(self.grid_layout_widget_2)
        self.grid_layout_2.setContentsMargins(0, 0, 0, 0)

        self.phone_number_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.phone_number_line_edit.setFont(font)
        self.phone_number_line_edit.setMaxLength(10)
        self.phone_number_line_edit.setValidator(QtGui.QIntValidator())
        self.grid_layout_2.addWidget(self.phone_number_line_edit, 1, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setText("電話號碼")
        self.grid_layout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.grid_layout_widget_3 = QtWidgets.QWidget(self)
        self.grid_layout_widget_3.setGeometry(QtCore.QRect(0, 220, 801, 91))
        self.grid_layout_3 = QtWidgets.QGridLayout(self.grid_layout_widget_3)
        self.grid_layout_3.setContentsMargins(0, 0, 0, 0)

        self.note_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.note_line_edit.setFont(font)
        self.grid_layout_3.addWidget(self.note_line_edit, 1, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setText("備註")
        self.grid_layout_3.addWidget(self.label_3, 0, 0, 1, 1)

    def resizeEvent(self, event):
        self.grid_layout_widget.setGeometry(0, 0, int(self.width() * 0.8), int(self.height() * 0.3))
        self.grid_layout_widget_2.setGeometry(0, int(self.height() * 0.3), int(self.width() * 0.8), int(self.height() * 0.3))
        self.grid_layout_widget_3.setGeometry(0, int(self.height() * 0.6), int(self.width() * 0.8), int(self.height() * 0.3))
        self.button_box.setGeometry(int(self.width() * 0.8), int(self.height() * 0.9), int(self.width() * 0.2), int(self.height() * 0.1))
        self.adjust_font_size()
        super(AddPlateDialog, self).resizeEvent(event)

    def adjust_font_size(self):
        base_font_size = 35
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
                self.accept()
            elif isinstance(focus_widget, QtWidgets.QLineEdit):
                self.focusNextChild()
        else:
            super(AddPlateDialog, self).keyPressEvent(event)

    def accept(self) -> None:
        """Handle the accept event."""
        plate_info = self.get_plate_info()
        logger.debug(f"Plate Info: {plate_info}")
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
