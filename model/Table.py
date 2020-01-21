from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from model.HexBinding import HexBinding
import logging


class Table(QTableWidget):

    COLUMNS_COUNT = 5
    ROWS_COUNT = 16
    HEADERS = [
        "Рукав", "Счётчик", "Сумма",
        "Количество заправок", "Количество плохих импульсов"
    ]

    def __init__(self):
        QTableWidget.__init__(self)

        self.hex_binding = HexBinding()
        self.setColumnCount(self.COLUMNS_COUNT)
        self.setRowCount(self.ROWS_COUNT)

        self.setHorizontalHeaderLabels([f"   {h}   " for h in self.HEADERS])
        for n in range(0, self.COLUMNS_COUNT):
            self.horizontalHeaderItem(n).setTextAlignment(Qt.AlignHCenter)

        first_column = [f"A{i}" for i in range(1, 9)] + [f"B{i}" for i in range(1, 9)]
        for i in range(0, self.ROWS_COUNT):
            self.set_cell_value(i, 0, first_column[i])

        self.resizeColumnsToContents()

    def set_cell_value(self, row, column, value):
        w = QTableWidgetItem(str(value))
        w.setTextAlignment(Qt.AlignRight)
        self.setItem(row, column, w)

    def load_from_file(self, filename):
        logging.info(f"Load HEX table from file {filename}")
        self.hex_binding.load_from_file(filename)
        for i in range(0, self.ROWS_COUNT):
            for j in range(0, self.COLUMNS_COUNT - 1):
                self.set_cell_value(i, j + 1, self.hex_binding.get_mapped_hex_data(i, j))
        self.resizeColumnsToContents()

    def save_to_file(self, filename):
        logging.info(f"Save HEX table to file {filename}")
