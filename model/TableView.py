from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt


class TableView(QTableWidget):
    def __init__(self, headers):
        QTableWidget.__init__(self)

        self.headers = headers
        self.setColumnCount(len(self.headers))

        self.setup_headers()

    def setup_headers(self):
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.setHorizontalHeaderLabels([f"   {h}   " for h in self.headers])
        for n in range(0, len(self.headers)):
            self.horizontalHeaderItem(n).setTextAlignment(Qt.AlignHCenter)

    def display_data(self, hoses):
        self.clean_table()
        row_position = self.rowCount()
        for h in hoses:
            self.insertRow(row_position)
            for column_position, column_name in enumerate(self.headers):
                self.set_cell_value(row_position, column_position, h.get_field_by_name(column_name))
            row_position += 1

    def clean_table(self):
        self.clear()
        self.setRowCount(0)

    def set_cell_value(self, row, column, value):
        w = QTableWidgetItem(str(value))
        w.setTextAlignment(Qt.AlignRight)
        self.setItem(row, column, w)
