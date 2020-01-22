from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from model.Table import Table
from model.HexBinding import HexBinding
import sys
import logging

logging.basicConfig(level=logging.DEBUG)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.table = Table()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("HEXeditor")
        self.setMinimumSize(QSize(800, 600))

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        grid_layout.addWidget(self.table, 0, 0, 3, 4)

        sum_label = QLabel("Контрольная сумма")
        sum_label.setFixedHeight(35)
        sum_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        grid_layout.addWidget(sum_label, 4, 1)

        check_sum_edit = QLineEdit()
        check_sum_edit.setFixedWidth(150)
        grid_layout.addWidget(self.check_sum_edit, 4, 2)

        calc_button = QPushButton("Рассчитать")
        calc_button.setFixedWidth(150)
        grid_layout.addWidget(calc_button, 4, 3)

        open_button = QPushButton("Открыть")
        open_button.clicked.connect(self.open_button_clicked)
        open_button.setFixedWidth(150)
        grid_layout.addWidget(open_button, 5, 2)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_button_clicked)
        save_button.setFixedWidth(150)
        grid_layout.addWidget(save_button, 5, 3)

        self.show()

    def open_button_clicked(self):
        logging.info("open_button clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                  "Hex dump (*.hex);;All Files (*)", options=options)

        if filename:
            hex_binding = HexBinding(filename)
            self.table.load_from_file(filename)
            self.check_sum_edit.setText(self.table.hex_binding.get_check_sum())

    def save_button_clicked(self):
        logging.info("save_button clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                  "Hex dump (*.hex);;All Files (*)", options=options)
        if filename:
            self.table.save_to_file(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
