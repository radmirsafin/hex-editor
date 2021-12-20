import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from model.TableView import TableView
from model.HexDataMapper import HexDataMapper
from model.Exceptions import *


logging.basicConfig(
    level=logging.DEBUG,
    filename="hex_editor.log",
    format='%(asctime)-15s %(message)s'
)


def with_exception_message(f):
    def with_message(*args):
        try:
            f(args[0])
        except Exception as exc:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Ошибка!")
            msg.setStandardButtons(QMessageBox.Ok)

            if isinstance(exc, HexEditorException):
                msg.setText(exc.text)
                msg.setInformativeText(exc.informative_text)
                msg.setDetailedText(exc.detailed_text)
            else:
                msg.setText("Необработанное исключение")
                msg.setDetailedText(str(exc))

            msg.exec_()

    return with_message


def show_info_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setText(message)
    msg.exec_()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.hex_mapper = None

        self.setWindowTitle("HEXeditor")
        self.setMinimumSize(QSize(800, 600))

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.table_view = TableView()
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

    @with_exception_message
    def open_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Hex dump (*.hex);;All Files (*)", options=options)

        if filename:
            logging.info(f"Open file: {filename}")
            self.hex_mapper = HexDataMapper(filename)
            table_items = self.hex_mapper.get_data()
            self.table_view.display_table_items(table_items)
            self.checksum_line.setText(self.hex_mapper.get_checksum())
        else:
            logging.info("Hex file not selected")

    @with_exception_message
    def save_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                  "Hex dump (*.hex);;All Files (*)", options=options)
        if filename and self.hex_mapper:
            table_items = self.table_view.get_table_items()
            self.hex_mapper.set_data(table_items)
            self.hex_mapper.write_dump_to_file(filename)
            show_info_message("Файл сохранён")
        else:
            logging.info("Nothing to save")

    @with_exception_message
    def calculate_button_clicked(self):
        if self.hex_mapper:
            table_items = self.table_view.get_table_items()
            self.hex_mapper.set_data(table_items)
            self.checksum_line.setText(self.hex_mapper.get_checksum())
        else:
            logging.info("Cannot found any loaded *.hex files")


if __name__ == "__main__":
    logging.info("Application started")
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
