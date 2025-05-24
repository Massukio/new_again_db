"""
Dialog for adjusting font sizes in the application.
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class FontSizeDialog(QtWidgets.QDialog):
    """Dialog for adjusting the font sizes of different UI elements."""

    def __init__(self, parent, button_font_size, table_font_size, input_font_size):
        """Initialize the font size dialog with current values."""
        super(FontSizeDialog, self).__init__(parent)
        self.setWindowTitle("調整字體大小")
        self.resize(400, 300)

        # Store initial values
        self.button_font_size = button_font_size
        self.table_font_size = table_font_size
        self.input_font_size = input_font_size

        # Create layout
        layout = QtWidgets.QVBoxLayout(self)

        # Button font size
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(QtWidgets.QLabel("按鈕字體大小:"))
        self.button_font_spinner = QtWidgets.QSpinBox()
        self.button_font_spinner.setRange(10, 40)
        self.button_font_spinner.setValue(button_font_size)
        button_layout.addWidget(self.button_font_spinner)
        layout.addLayout(button_layout)

        # Table font size
        table_layout = QtWidgets.QHBoxLayout()
        table_layout.addWidget(QtWidgets.QLabel("表格字體大小:"))
        self.table_font_spinner = QtWidgets.QSpinBox()
        self.table_font_spinner.setRange(10, 40)
        self.table_font_spinner.setValue(table_font_size)
        table_layout.addWidget(self.table_font_spinner)
        layout.addLayout(table_layout)

        # Input field font size
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(QtWidgets.QLabel("輸入欄位字體大小:"))
        self.input_font_spinner = QtWidgets.QSpinBox()
        self.input_font_spinner.setRange(10, 40)
        self.input_font_spinner.setValue(input_font_size)
        input_layout.addWidget(self.input_font_spinner)
        layout.addLayout(input_layout)

        # Preview section
        preview_group = QtWidgets.QGroupBox("預覽")
        preview_layout = QtWidgets.QVBoxLayout(preview_group)

        # Button preview
        self.button_preview = QtWidgets.QPushButton("按鈕預覽")
        self.button_preview.setFixedHeight(50)
        preview_layout.addWidget(self.button_preview)

        # Table preview
        self.table_preview = QtWidgets.QTableWidget(1, 1)
        self.table_preview.setItem(0, 0, QtWidgets.QTableWidgetItem("表格預覽"))
        preview_layout.addWidget(self.table_preview)

        # Input field preview
        self.input_preview = QtWidgets.QLineEdit("輸入欄位預覽")
        preview_layout.addWidget(self.input_preview)

        layout.addWidget(preview_group)

        # Dialog buttons
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Connect signals
        self.button_font_spinner.valueChanged.connect(self.update_preview)
        self.table_font_spinner.valueChanged.connect(self.update_preview)
        self.input_font_spinner.valueChanged.connect(self.update_preview)

        # Initial preview update
        self.update_preview()

    def update_preview(self):
        """Update the preview based on current spinner values."""
        # Button preview
        button_size = self.button_font_spinner.value()
        button_style = f"QPushButton {{ font-size: {button_size}px; }}"
        self.button_preview.setStyleSheet(button_style)

        # Table preview
        table_size = self.table_font_spinner.value()
        table_style = f"QTableWidget {{ font-size: {table_size}px; }}"
        self.table_preview.setStyleSheet(table_style)

        # Input field preview
        input_size = self.input_font_spinner.value()
        input_style = f"QLineEdit {{ font-size: {input_size}px; }}"
        self.input_preview.setStyleSheet(input_style)

    def get_button_font_size(self):
        """Get the selected button font size."""
        return self.button_font_spinner.value()

    def get_table_font_size(self):
        """Get the selected table font size."""
        return self.table_font_spinner.value()

    def get_input_font_size(self):
        """Get the selected input field font size."""
        return self.input_font_spinner.value()
