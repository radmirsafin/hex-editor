from model.RecordType import RecordType
import logging


class TableData:
    def __init__(self):
        self.sleeves = []
        self.check_sum



    #
    # ROWS_COUNT = 16
    # COLUMNS_COUNT = 5
    # HEADERS = [
    #     "Рукав", "Счётчик", "Сумма",
    #     "Количество заправок", "Количество плохих импульсов"
    # ]
    #
    # def __init__(self):
    #     self.data = [[0.0] * self.COLUMNS_COUNT] * self.ROWS_COUNT
    #     self.delta_base = [0.0] * self.COLUMNS_COUNT
    #     self.check_sum = None
    #
    # def set_data(self, record_type, raw_hex, row, column):
    #     self.data[row][column] = self._create_value(record_type, raw_hex)
    #
    # def set_delta_base(self, record_type, raw_hex, row):
    #     self.delta_base[row] = self._create_value(record_type, raw_hex)
    #
    # def recalculate(self):
    #     for index, row in enumerate(self.data):
    #         row[-1] = self.delta_base[index] - row[0]
    #
    # def _create_value(self, record_type, raw_hex):
    #     if type(record_type) is not RecordType:
    #         record_type = RecordType(record_type)
    #     if record_type is RecordType.INTEGER:
    #         return self._create_int(raw_hex)
    #     elif record_type is RecordType.FLOAT:
    #         return self._create_float(raw_hex)
    #     else:
    #         logging.error(f"Unknown record type: {record_type}")
    #
    # @classmethod
    # def _create_float(cls, raw_hex):
    #     integer = raw_hex[:-2]
    #     decimal = raw_hex[-2:]
    #     return float(integer + "." + decimal)
    #
    # @classmethod
    # def _create_int(cls, raw_hex):
    #     return int(raw_hex)


