import logging
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from model.TableViewItem import TableViewItem
from model.Exceptions import *

HEADERS = [
    "Рукав",
    "Счётчик",
    "Сумма",
    "Количество заправок",
    "Количество плохих импульсов",
]


class TableView(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.setColumnCount(len(HEADERS))
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.setHorizontalHeaderLabels([f"   {h}   " for h in HEADERS])
        for n in range(0, len(HEADERS)):
            self.horizontalHeaderItem(n).setTextAlignment(Qt.AlignHCenter)

    def display_table_items(self, table_view_items):
        self.clean_table()
        row_position = self.rowCount()
        for table_item in table_view_items:
            self.insertRow(row_position)
            self.set_cell_value(row_position, 0, table_item.name)
            self.set_cell_value(row_position, 1, table_item.counter)
            self.set_cell_value(row_position, 2, table_item.amount)
            self.set_cell_value(row_position, 3, table_item.refill_count)
            self.set_cell_value(row_position, 4, table_item.bad_count)
            row_position += 1

    def clean_table(self):
        self.setRowCount(0)

    def set_cell_value(self, row, column, value):
        w = QTableWidgetItem(str(value))
        w.setTextAlignment(Qt.AlignRight)
        if column == 0:
            w.setFlags(Qt.ItemIsEditable)
        self.setItem(row, column, w)

    def get_table_items(self):
        table_view_items = []
        for row_i in range(0, self.rowCount()):
            try:
                table_item = TableViewItem(
                    name=self.item(row_i, 0).text(),
                    counter=self.item(row_i, 1).text(),
                    amount=self.item(row_i, 2).text(),
                    refill_count=self.item(row_i, 3).text(),
                    bad_count=self.item(row_i, 4).text(),
                )
            except ValueError as exc:
                exc = InvalidTableItemValueException(row_number=row_i, detailed_text=str(exc))
                logging.error(exc)
                raise exc
            logging.debug(f"Item loaded from table: {table_item}")
            table_view_items.append(table_item)
        return table_view_items
