#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MainWindow:

    def __init__(self):
        # Margins
        self.margin = 5
        self.bottom_margin = 10

        # App and window
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()
        self.window.setObjectName('MainWindow')
        self.central_widget = QtWidgets.QWidget(self.window)
        self.central_widget.setObjectName('central_widget')
        self.window.setCentralWidget(self.central_widget)

        # Setup components
        self.setup()

    def setup_grids(self):
        self.table_widget = QtWidgets.QWidget(self.central_widget)
        self.table_widget.setObjectName("table_grid_widget")
        self.table_widget.setGeometry(QtCore.QRect(
            self.margin, self.margin,750 - self.margin, 400 - self.margin))

        self.table_grid = QtWidgets.QGridLayout(self.table_widget)
        self.table_grid.setObjectName("table_layout")
        self.table_grid.setContentsMargins(
            self.margin, self.margin, self.margin, self.bottom_margin)

        self.btn_widget = QtWidgets.QWidget(self.central_widget)
        self.btn_widget.setObjectName("button_grid_widget")
        self.btn_widget.setGeometry(QtCore.QRect(
            750+self.margin, self.margin, 200-self.margin, 400-self.margin))

        self.btn_grid = QtWidgets.QGridLayout(self.btn_widget)
        self.btn_grid.setObjectName("button_layout")
        self.btn_grid.setContentsMargins(
            self.margin, self.margin, self.margin, self.bottom_margin)

        self.input_widget = QtWidgets.QWidget(self.central_widget)
        self.input_widget.setObjectName("input_grid_widget")
        self.input_widget.setGeometry(QtCore.QRect(
            self.margin, 400+self.margin,
            750-self.margin, 100-self.bottom_margin))

        self.input_grid = QtWidgets.QGridLayout(self.input_widget)
        self.input_grid.setObjectName("input_layout")
        self.input_grid.setContentsMargins(
            self.margin, self.margin, self.margin, self.bottom_margin)

    def setup_buttons(self):
        self.connect_button = QtWidgets.QPushButton("連接資料庫", self.btn_widget)
        self.connect_button.setObjectName("connect_button")
        self.btn_grid.addWidget(self.connect_button, 0, 0, 1, 1)

        self.view_all_button = QtWidgets.QPushButton("瀏覽全部資料", self.btn_widget)
        self.view_all_button.setObjectName("view_all_button")
        self.btn_grid.addWidget(self.view_all_button, 1, 0, 1, 1)

        self.add_button = QtWidgets.QPushButton("新增資料", self.btn_widget)
        self.add_button.setObjectName("add_button")
        self.btn_grid.addWidget(self.add_button, 2, 0, 1, 1)

        self.delete_button = QtWidgets.QPushButton("刪除所選資料", self.btn_widget)
        self.delete_button.setObjectName("delete_button")
        self.btn_grid.addWidget(self.delete_button, 3, 0, 1, 1)

        self.modify_button = QtWidgets.QPushButton("修改所選資料", self.btn_widget)
        self.modify_button.setObjectName("modify_button")
        self.btn_grid.addWidget(self.modify_button, 4, 0, 1, 1)

        self.backup_button = QtWidgets.QPushButton("備份資料庫", self.btn_widget)
        self.backup_button.setObjectName("backup_button")
        self.btn_grid.addWidget(self.backup_button, 5, 0, 1, 1)

    def setup_inputs(self):
        self.search_combo_box = QtWidgets.QComboBox(self.input_widget)
        self.search_combo_box.setObjectName("search_combo_box")
        self.search_combo_box.addItem("車牌查詢")
        self.search_combo_box.addItem("電話查詢")
        self.search_combo_box.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.input_grid.addWidget(self.search_combo_box, 0, 0, 1, 1)

        self.plate_input1 = QtWidgets.QLineEdit(self.input_widget)
        self.plate_input1.setObjectName("plate_input1")
        self.plate_input1.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.input_grid.addWidget(self.plate_input1, 0, 1, 1, 1)

        self.plate_input2 = QtWidgets.QLineEdit(self.input_widget)
        self.plate_input2.setObjectName("plate_input2")
        self.plate_input2.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.input_grid.addWidget(self.plate_input2, 0, 2, 1, 1)

        # Adjust the stretch factors to evenly distribute the items
        self.input_grid.setColumnStretch(0, 1)
        self.input_grid.setColumnStretch(1, 3)
        self.input_grid.setColumnStretch(2, 3)

    def setup_tables(self):
        self.table_view = QtWidgets.QTableWidget(self.table_widget)
        self.table_view.horizontalHeader().setVisible(True)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setColumnCount(3)
        self.table_view.setHorizontalHeaderLabels(["車牌號碼", "電話號碼", "備註"])
        self.table_view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_grid.addWidget(self.table_view, 0, 0, 1, 1)


    def setup(self):
        self.setup_grids()
        self.setup_buttons()
        self.setup_inputs()
        self.setup_tables()


    def start(self):
        self.window.show()
        self.window.showMaximized()
        exit_code = self.app.exec_()

        self.window.close()  # Ensure the main window is closed
        sys.exit(exit_code)



MainWindow().start()
