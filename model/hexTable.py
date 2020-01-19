from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import Qt


class HexTable(QTableWidget):

    COLUMNS_COUNT = 5
    ROWS_COUNT = 16
    HEADERS = [
        "Рукав", "Счётчик", "Сумма",
        "Количество заправок", "Количество плохих импульсов"
    ]

    def __init__(self):
        QTableWidget.__init__(self)

        self.setColumnCount(self.COLUMNS_COUNT)
        self.setRowCount(self.ROWS_COUNT)

        self.setHorizontalHeaderLabels([f"   {h}   " for h in self.HEADERS])

        for n in range(0, self.COLUMNS_COUNT):
            self.horizontalHeaderItem(n).setTextAlignment(Qt.AlignHCenter)

        # table.setItem(0, 0, QTableWidgetItem("Text in column 1"))
        # table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        # table.setItem(0, 2, QTableWidgetItem("Text in column 3"))

        self.resizeColumnsToContents()

    def load_from_file(self, filename):
        pass

    def save_to_file(self, filename):
        pass
