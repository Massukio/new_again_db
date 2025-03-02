from PyQt5 import QtCore, QtWidgets
from db.database import get_all_plate_info, delete_plate_info, filter_plate_info

class TableViewHandler:
    def __init__(self, table_view, plate_line_edit, plate_line_edit2, search_combo_box):
        self.table_view = table_view
        self.plate_line_edit = plate_line_edit
        self.plate_line_edit2 = plate_line_edit2
        self.search_combo_box = search_combo_box
        self.plate_line_edit.textChanged.connect(self.filter_table)
        self.plate_line_edit2.textChanged.connect(self.filter_table)
        self.search_combo_box.currentIndexChanged.connect(self.filter_table)
        self.table_view.verticalHeader().setVisible(False)  # Hide row numbers
        self.load_data()

    def load_data(self):
        data = get_all_plate_info()
        self._populate_table(data)

    def _populate_table(self, data):
        self.table_view.setRowCount(len(data))
        for row, (plate, info) in enumerate(data.items()):
            self.table_view.setItem(row, 0, QtWidgets.QTableWidgetItem(plate))
            self.table_view.setItem(row, 1, QtWidgets.QTableWidgetItem(info["phone_number"]))
            self.table_view.setItem(row, 2, QtWidgets.QTableWidgetItem(info["note"]))

    def filter_table(self):
        part1_filter_text = phone_filter_text = \
            self.plate_line_edit.text().lower()
        part2_filter_text = self.plate_line_edit2.text().lower()
        search_mode = self.search_combo_box.currentText()
        if search_mode == "電話查詢":
            data = filter_plate_info("", "", phone_filter_text, search_mode)
        else:
            data = filter_plate_info(part1_filter_text, part2_filter_text, "", search_mode)
        self._populate_table(data)

    def delete_selected_row(self):
        selected_row = self.table_view.currentRow()
        if selected_row >= 0:
            plate_info = self.table_view.item(selected_row, 0).text()
            part1, part2 = plate_info.split('-')
            delete_plate_info(part1, part2)
            self.table_view.removeRow(selected_row)
