from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from model.Hose import Hose
from model.Exceptions import InvalidTableDataException

import logging


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
                self.set_cell_value(row_position, column_position, h.get_field_by_header(column_name))
            row_position += 1

    def clean_table(self):
        self.setRowCount(0)

    def set_cell_value(self, row, column, value):
        w = QTableWidgetItem(str(value))
        w.setTextAlignment(Qt.AlignRight)
        if column == 0:
            w.setFlags(Qt.ItemIsEditable)
        self.setItem(row, column, w)

    def get_data(self):
        hoses = []
        for row_i in range(0, self.rowCount()):
            try:
                hose = Hose(
                      name=self.item(row_i, 0).text(),
                      good_impulse_count=float(self.item(row_i, 1).text()),
                      amount=float(self.item(row_i, 2).text()),
                      refill_count=int(self.item(row_i, 3).text()),
                      bad_impulse_count=float(self.item(row_i, 4).text()),
                )
            except ValueError as exc:
                raise InvalidTableDataException(str(exc), row_i)

            logging.debug(f"Item loaded from table: {hose}")
            hoses.append(hose)
        return hoses

