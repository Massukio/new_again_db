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
        self.setup_grids()

    def setup_grids(self):
        self.table_widget = QtWidgets.QWidget(self.central_widget)
        self.table_widget.setObjectName("table_grid_widget")
        self.table_widget.setGeometry(QtCore.QRect(
            self.margin, self.margin,750 - self.margin, 400 - self.margin))
        self.table_widget.setStyleSheet("background-color: lightgray;")

        self.table_grid = QtWidgets.QGridLayout(self.table_widget)
        self.table_grid.setObjectName("table_layout")
        self.table_grid.setContentsMargins(
            self.margin, self.margin, self.margin, self.bottom_margin)

        self.btn_widget = QtWidgets.QWidget(self.central_widget)
        self.btn_widget.setGeometry(QtCore.QRect(
            750+self.margin, self.margin, 200-self.margin, 400-self.margin))
        self.btn_widget.setObjectName("button_grid_widget")
        self.btn_widget.setStyleSheet("background-color: red;")

        self.btn_grid = QtWidgets.QGridLayout(self.btn_widget)
        self.btn_grid.setContentsMargins(
            self.margin, self.margin, self.margin, self.bottom_margin)
        self.btn_grid.setObjectName("button_layout")

        self.input_widget = QtWidgets.QWidget(self.central_widget)
        self.input_widget.setGeometry(QtCore.QRect(
            self.margin, 400+self.margin,
            750-self.margin, 100-self.bottom_margin))
        self.input_widget.setObjectName("input_grid_widget")

        self.input_grid = QtWidgets.QGridLayout(self.input_widget)
        self.input_grid.setContentsMargins(
            self.margin, self.margin, self.margin, self.bottom_margin)
        self.input_grid.setObjectName("input_layout")


    def setup(self):
        pass


    def start(self):
        self.window.show()
        self.window.showMaximized()
        exit_code = self.app.exec_()

        self.window.close()  # Ensure the main window is closed
        sys.exit(exit_code)



MainWindow().start()
