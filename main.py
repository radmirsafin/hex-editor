from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from model.TableView import TableView
from model.HexAPI import HexAPI
from model.Hose import HOSE_FIELD_NAMES

import sys
import logging

logging.basicConfig(level=logging.DEBUG)


TABLE_VIEW_HEADERS = [
    "Рукав", "Счётчик", "Сумма",
    "Количество заправок", "Количество плохих импульсов"
]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.hex_api = None

        self.setWindowTitle("HEXeditor")
        self.setMinimumSize(QSize(800, 600))

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.table_view = TableView(HOSE_FIELD_NAMES)
        self.grid_layout.addWidget(self.table_view, 0, 0, 3, 4)

        self.checksum_label = QLabel("Контрольная сумма")
        self.checksum_label.setFixedHeight(35)
        self.checksum_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.grid_layout.addWidget(self.checksum_label, 4, 1)

        self.checksum_line = QLineEdit()
        self.checksum_line.setFixedWidth(150)
        self.grid_layout.addWidget(self.checksum_line, 4, 2)

        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.clicked.connect(self.calculate_button_clicked)
        self.calc_button.setFixedWidth(150)
        self.grid_layout.addWidget(self.calc_button, 4, 3)

        self.open_button = QPushButton("Открыть")
        self.open_button.clicked.connect(self.open_button_clicked)
        self.open_button.setFixedWidth(150)
        self.grid_layout.addWidget(self.open_button, 5, 2)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_button_clicked)
        self.save_button.setFixedWidth(150)
        self.grid_layout.addWidget(self.save_button, 5, 3)

        self.show()

    def open_button_clicked(self):
        logging.info("open_button clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                  "Hex dump (*.hex);;All Files (*)", options=options)

        if filename:
            self.hex_api = HexAPI(filename)
            self.table_view.display_data(self.hex_api.get_data())
            self.checksum_line.setText(self.hex_api.get_checksum())

    def save_button_clicked(self):
        logging.info("save_button clicked")
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
        #                                           "Hex dump (*.hex);;All Files (*)", options=options)
        # if filename:
        #     self.table.save_to_file(filename)

    def calculate_button_clicked(self):
        logging.info("calc_button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
