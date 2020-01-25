from intelhex import IntelHex
from model.RecordType import RecordType
import logging


class Hex:
    def __init__(self, filename):
        self.hex = IntelHex(filename)

    def get_range(self, start_addr, end_addr):
        data = []
        for b in self.hex[start_addr:end_addr + 1].todict().values():
            data += hex(b).replace("0x", "").rjust(2, '0')
        return "".join(data).upper()

    def get_integer(self, start_addr, end_addr):
        return int(self.get_range(start_addr, end_addr))

    def get_float(self, start_addr, end_addr):
        raw = self.get_range(start_addr, end_addr)
        integer = raw[:-2]
        decimal = raw[-2:]
        return float(integer + "." + decimal)

    def get_number(self, record_type, start_addr, end_addr):
        if record_type is RecordType.INTEGER:
            return self.get_integer(start_addr, end_addr)
        elif record_type is RecordType.FLOAT:
            return self.get_float(start_addr, end_addr)
        else:
            logging.error(f"Unknown record type: {record_type}")
            return None

    def get_checksum(self):
        raw = self.get_range(0x180, 0x181)
        raw = raw[2:] + raw[:2]
        return "0x" + raw.upper()
