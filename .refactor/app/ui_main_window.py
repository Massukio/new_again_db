"""
Main UI definition for the refactored New Again application.
This is a standalone implementation that doesn't depend on the original codebase.
"""

import os
from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow(object):
    """
    UI definition for the main window of the New Again application.
    This class defines the layout and basic UI components.
    """

    def setup_ui(self, main_window):
        """Set up the UI components for the main window."""
        main_window.setObjectName("MainWindow")
        main_window.resize(1000, 500)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        main_window.setCentralWidget(self.central_widget)

        margin = 5
        bottom_margin = 20

        # Table view area
        self.grid_layout_widget = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(margin, margin, 750 - margin, 400 - margin))
        self.grid_layout_widget.setObjectName("grid_layout_widget")

        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(margin, margin, margin, bottom_margin)
        self.grid_layout.setObjectName("grid_layout")

        self.table_view = QtWidgets.QTableWidget(self.grid_layout_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHeightForWidth(self.table_view.sizePolicy().hasHeightForWidth())
        self.table_view.setSizePolicy(size_policy)
        self.table_view.setObjectName("table_view")
        self.table_view.horizontalHeader().setVisible(True)
        self.table_view.horizontalHeader().setCascadingSectionResizes(False)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setColumnCount(3)
        self.table_view.setHorizontalHeaderLabels(["車牌號碼", "電話號碼", "備註"])
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.table_view.setFont(font)
        self.table_view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.grid_layout.addWidget(self.table_view, 0, 0, 1, 1)

        # Button area
        self.grid_layout_widget_2 = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget_2.setGeometry(QtCore.QRect(750 + margin, margin, 200 - margin, 400 - margin))
        self.grid_layout_widget_2.setObjectName("grid_layout_widget_2")

        self.grid_layout_3 = QtWidgets.QGridLayout(self.grid_layout_widget_2)
        self.grid_layout_3.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_3.setObjectName("grid_layout_3")

        # Add button
        self.add_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.add_button.setText("新增")
        self.grid_layout_3.addWidget(self.add_button, 0, 0, 1, 1)

        # Modify button
        self.modify_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.modify_button.setFont(font)
        self.modify_button.setObjectName("modify_button")
        self.modify_button.setText("修改")
        self.grid_layout_3.addWidget(self.modify_button, 1, 0, 1, 1)

        # Delete button
        self.delete_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setText("刪除")
        self.grid_layout_3.addWidget(self.delete_button, 2, 0, 1, 1)

        # Database location button
        self.connect_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.connect_button.setFont(font)
        self.connect_button.setObjectName("connect_button")
        self.connect_button.setText("資料庫位置")
        self.grid_layout_3.addWidget(self.connect_button, 3, 0, 1, 1)

        # Backup button
        self.backup_button = QtWidgets.QPushButton(self.grid_layout_widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.backup_button.setFont(font)
        self.backup_button.setObjectName("backup_button")
        self.backup_button.setText("備份")
        self.grid_layout_3.addWidget(self.backup_button, 4, 0, 1, 1)

        # Filter area
        self.grid_layout_widget_3 = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget_3.setGeometry(QtCore.QRect(margin, 400 + margin, 950 - margin, 100 - margin))
        self.grid_layout_widget_3.setObjectName("grid_layout_widget_3")

        self.grid_layout_2 = QtWidgets.QGridLayout(self.grid_layout_widget_3)
        self.grid_layout_2.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_2.setObjectName("grid_layout_2")

        # Search mode combo box
        self.search_combo_box = QtWidgets.QComboBox(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.search_combo_box.setFont(font)
        self.search_combo_box.setObjectName("search_combo_box")
        self.search_combo_box.addItem("車牌查詢")
        self.search_combo_box.addItem("電話查詢")
        self.grid_layout_2.addWidget(self.search_combo_box, 0, 0, 1, 1)

        # Filter input fields
        self.plate_filter_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.plate_filter_line_edit.setFont(font)
        self.plate_filter_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.plate_filter_line_edit.setObjectName("plate_filter_line_edit")
        self.grid_layout_2.addWidget(self.plate_filter_line_edit, 0, 1, 1, 1)

        self.plate_filter_line_edit2 = QtWidgets.QLineEdit(self.grid_layout_widget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.plate_filter_line_edit2.setFont(font)
        self.plate_filter_line_edit2.setAlignment(QtCore.Qt.AlignCenter)
        self.plate_filter_line_edit2.setObjectName("plate_filter_line_edit2")
        self.grid_layout_2.addWidget(self.plate_filter_line_edit2, 0, 2, 1, 1)

        # Create menu bar
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menu_bar.setObjectName("menu_bar")

        self.menu_settings = QtWidgets.QMenu(self.menu_bar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_settings.setTitle("設定")

        main_window.setMenuBar(self.menu_bar)
        self.menu_bar.addAction(self.menu_settings.menuAction())

        self.action_adjust_font_size = QtWidgets.QAction(main_window)
        self.action_adjust_font_size.setObjectName("action_adjust_font_size")
        self.action_adjust_font_size.setText("調整字體大小")
        self.menu_settings.addAction(self.action_adjust_font_size)
