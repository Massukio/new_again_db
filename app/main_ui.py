import os
from PyQt5 import QtCore, QtGui, QtWidgets
from app.table_view_handler import TableViewHandler
from app.add_plate_dialog import AddPlateDialog
from db.database import delete_plate_info, update_plate_info

class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(874, 450)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        self.grid_layout_widget = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(0, 0, 671, 341))
        self.grid_layout_widget.setObjectName("grid_layout_widget")

        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")

        self.table_view = QtWidgets.QTableWidget(self.grid_layout_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHeightForWidth(self.table_view.sizePolicy().hasHeightForWidth())
        self.table_view.setSizePolicy(size_policy)
        self.table_view.setObjectName("table_view")
        self.table_view.horizontalHeader().setVisible(True)
        self.table_view.horizontalHeader().setCascadingSectionResizes(False)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setColumnCount(2)
        self.table_view.setHorizontalHeaderLabels(["車牌號碼", "電話號碼"])
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.table_view.setFont(font)
        self.table_view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.grid_layout.addWidget(self.table_view, 1, 0, 1, 1)

        self.title_label = QtWidgets.QLabel(self.grid_layout_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 1)

        self.grid_layout_widget_2 = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget_2.setGeometry(QtCore.QRect(670, 0, 201, 341))
        self.grid_layout_widget_2.setObjectName("grid_layout_widget_2")

        self.grid_layout_3 = QtWidgets.QGridLayout(self.grid_layout_widget_2)
        self.grid_layout_3.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_3.setObjectName("grid_layout_3")

        self.modify_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.modify_button.sizePolicy().hasHeightForWidth())
        self.modify_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.modify_button.setFont(font)
        self.modify_button.setObjectName("modify_button")
        self.grid_layout_3.addWidget(self.modify_button, 4, 0, 1, 1)

        self.add_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.grid_layout_3.addWidget(self.add_button, 2, 0, 1, 1)

        self.connect_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.connect_button.setFont(font)
        self.connect_button.setIconSize(QtCore.QSize(4, 16))
        self.connect_button.setObjectName("connect_button")
        self.grid_layout_3.addWidget(self.connect_button, 0, 0, 1, 1)

        self.delete_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.grid_layout_3.addWidget(self.delete_button, 3, 0, 1, 1)

        self.view_all_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.view_all_button.sizePolicy().hasHeightForWidth())
        self.view_all_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.view_all_button.setFont(font)
        self.view_all_button.setObjectName("view_all_button")
        self.grid_layout_3.addWidget(self.view_all_button, 1, 0, 1, 1)

        self.grid_layout_widget_3 = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget_3.setGeometry(QtCore.QRect(0, 340, 671, 101))
        self.grid_layout_widget_3.setObjectName("grid_layout_widget_3")

        self.grid_layout_5 = QtWidgets.QGridLayout(self.grid_layout_widget_3)
        self.grid_layout_5.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_5.setObjectName("grid_layout_5")

        self.plate_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget_3)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.plate_line_edit.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.plate_line_edit.setFont(font)
        self.plate_line_edit.setMaxLength(4)
        self.plate_line_edit.setObjectName("plate_line_edit")
        self.grid_layout_5.addWidget(self.plate_line_edit, 0, 1, 1, 1)

        self.plate_line_edit2 = QtWidgets.QLineEdit(self.grid_layout_widget_3)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.plate_line_edit2.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.plate_line_edit2.setFont(font)
        self.plate_line_edit2.setMaxLength(4)
        self.plate_line_edit2.setObjectName("plate_line_edit2")
        self.grid_layout_5.addWidget(self.plate_line_edit2, 0, 2, 1, 1)

        self.search_combo_box = QtWidgets.QComboBox(self.grid_layout_widget_3)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.search_combo_box.sizePolicy().hasHeightForWidth())
        self.search_combo_box.setSizePolicy(size_policy)
        self.search_combo_box.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.search_combo_box.setFont(font)
        self.search_combo_box.setObjectName("search_combo_box")
        self.search_combo_box.addItem("")
        self.search_combo_box.addItem("")
        self.grid_layout_5.addWidget(self.search_combo_box, 0, 0, 1, 1)

        self.grid_layout_widget_6 = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget_6.setGeometry(QtCore.QRect(670, 340, 201, 101))
        self.grid_layout_widget_6.setObjectName("grid_layout_widget_6")

        self.grid_layout_8 = QtWidgets.QGridLayout(self.grid_layout_widget_6)
        self.grid_layout_8.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_8.setObjectName("grid_layout_8")

        self.backup_button = QtWidgets.QPushButton(self.grid_layout_widget_6)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHeightForWidth(self.backup_button.sizePolicy().hasHeightForWidth())
        self.backup_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.backup_button.setFont(font)
        self.backup_button.setObjectName("backup_button")
        self.grid_layout_8.addWidget(self.backup_button, 0, 0, 1, 1)

        main_window.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 874, 37))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_other = QtWidgets.QMenu(self.menu_bar)
        self.menu_other.setObjectName("menu_other")

        main_window.setMenuBar(self.menu_bar)

        self.action_about = QtWidgets.QAction(main_window)
        self.action_about.setObjectName("action_about")

        self.menu_other.addAction(self.action_about)
        self.menu_bar.addAction(self.menu_other.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        # Connect textChanged signals to the method
        self.plate_line_edit.textChanged.connect(self.convert_to_upper)
        self.plate_line_edit2.textChanged.connect(self.convert_to_upper)

        self.search_combo_box.currentIndexChanged.connect(self.update_line_edits)
        self.view_all_button.clicked.connect(self.reset_table_view)
        self.action_about.triggered.connect(self.show_about_dialog)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "再新洗車資料庫"))
        self.title_label.setText(_translate("MainWindow", "若要查詢請按瀏覽"))
        self.modify_button.setText(_translate("MainWindow", "修改所選資料"))
        self.add_button.setText(_translate("MainWindow", "新增資料"))
        self.connect_button.setText(_translate("MainWindow", "連接資料庫"))
        self.delete_button.setText(_translate("MainWindow", "刪除所選資料"))
        self.view_all_button.setText(_translate("MainWindow", "瀏覽全部資料"))
        self.search_combo_box.setItemText(0, _translate("MainWindow", "車牌查詢"))
        self.search_combo_box.setItemText(1, _translate("MainWindow", "電話查詢"))
        self.backup_button.setText(_translate("MainWindow", "備份資料庫"))
        self.menu_other.setTitle(_translate("MainWindow", "其他"))
        self.action_about.setText(_translate("MainWindow", "關於"))
        self.table_view.horizontalHeaderItem(0).setText(_translate("MainWindow", "車牌號碼"))
        self.table_view.horizontalHeaderItem(1).setText(_translate("MainWindow", "電話號碼"))

    def convert_to_upper(self, text):
        sender = self.sender()
        sender.blockSignals(True)
        sender.setText(text.upper())
        sender.blockSignals(False)

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

    def reset_table_view(self):
        self.plate_line_edit.clear()
        self.plate_line_edit2.clear()
        self.search_combo_box.setCurrentIndex(0)
        self.table_handler.load_data()
        for row in range(self.table_view.rowCount()):
            self.table_view.setRowHidden(row, False)
        self.plate_line_edit.setFocus()

    def show_about_dialog(self):
        about_text = (
            "Author: Sukio Lin\n"
            "Version: 1.0\n"
            "Release Date: 2025-03-01\n\n"
            "License: MIT License\n\n"
            "This application is licensed under the MIT License.\n"
            "For more information, visit https://opensource.org/licenses/MIT"
        )
        QtWidgets.QMessageBox.about(None, "About", about_text)
