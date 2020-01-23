from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import logging


class Table(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)

        self.hex_binding = None

        self.setColumnCount(self.COLUMNS_COUNT)
        self.setRowCount(self.ROWS_COUNT)

        self.setup_headers()

        first_column = [f"A{i}" for i in range(1, 9)] + [f"B{i}" for i in range(1, 9)]
        for i in range(0, self.ROWS_COUNT):
            self.set_cell_value(i, 0, first_column[i])

    def setup_headers(self):
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.setHorizontalHeaderLabels([f"   {h}   " for h in self.HEADERS])
        for n in range(0, self.COLUMNS_COUNT):
            self.horizontalHeaderItem(n).setTextAlignment(Qt.AlignHCenter)

    def set_cell_value(self, row, column, value):
        w = QTableWidgetItem(str(value))
        w.setTextAlignment(Qt.AlignRight)
        self.setItem(row, column, w)

    # def load_from_file(self, filename):
    #     logging.info(f"Load HEX table from file {filename}")
    #     self.hex_binding = HexBinding(filename)
    #     for i in range(0, self.ROWS_COUNT):
    #         for j in range(0, self.COLUMNS_COUNT - 1):
    #             self.set_cell_value(i, j + 1, self.hex_binding.get_mapped_hex_data(i, j))
    #
    # def save_to_file(self, filename):
    #     logging.info(f"Save HEX table to file {filename}")
