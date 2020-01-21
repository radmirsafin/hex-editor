from intelhex import IntelHex
from enum import Enum
import logging


HEX_DATA_MAPPING = [
    [('f', 0x00, 0x05), ('f', 0x06, 0x0B), ('i', 0x0C, 0x0F), ('diff', ('f', 0x100, 0x105), ('f', 0x00, 0x05))],
    [('f', 0x10, 0x15), ('f', 0x16, 0x1B), ('i', 0x1C, 0x1F), ('diff', ('f', 0x108, 0x10D), ('f', 0x10, 0x15))],
    [('f', 0x20, 0x25), ('f', 0x26, 0x2B), ('i', 0x2C, 0x2F), ('diff', ('f', 0x110, 0x115), ('f', 0x20, 0x25))],
    [('f', 0x30, 0x35), ('f', 0x36, 0x3B), ('i', 0x3C, 0x3F), ('diff', ('f', 0x118, 0x11D), ('f', 0x30, 0x35))],
    [('f', 0x40, 0x45), ('f', 0x46, 0x4B), ('i', 0x4C, 0x4F), ('diff', ('f', 0x120, 0x125), ('f', 0x40, 0x45))],
    [('f', 0x50, 0x55), ('f', 0x56, 0x5B), ('i', 0x5C, 0x5F), ('diff', ('f', 0x128, 0x12D), ('f', 0x50, 0x55))],
    [('f', 0x60, 0x65), ('f', 0x66, 0x6B), ('i', 0x6C, 0x6F), ('diff', ('f', 0x130, 0x135), ('f', 0x60, 0x65))],
    [('f', 0x70, 0x75), ('f', 0x76, 0x7B), ('i', 0x7C, 0x7F), ('diff', ('f', 0x138, 0x13D), ('f', 0x70, 0x75))],
    [('f', 0x80, 0x85), ('f', 0x86, 0x8B), ('i', 0x8C, 0x8F), ('diff', ('f', 0x140, 0x145), ('f', 0x80, 0x85))],
    [('f', 0x90, 0x95), ('f', 0x96, 0x9B), ('i', 0x9C, 0x9F), ('diff', ('f', 0x148, 0x14D), ('f', 0x90, 0x95))],
    [('f', 0xA0, 0xA5), ('f', 0xA6, 0xAB), ('i', 0xAC, 0xAF), ('diff', ('f', 0x150, 0x155), ('f', 0xA0, 0xA5))],
    [('f', 0xB0, 0xB5), ('f', 0xB6, 0xBB), ('i', 0xBC, 0xBF), ('diff', ('f', 0x158, 0x15D), ('f', 0xB0, 0xB5))],
    [('f', 0xC0, 0xC5), ('f', 0xC6, 0xCB), ('i', 0xCC, 0xCF), ('diff', ('f', 0x160, 0x165), ('f', 0xC0, 0xC5))],
    [('f', 0xD0, 0xD5), ('f', 0xD6, 0xDB), ('i', 0xDC, 0xDF), ('diff', ('f', 0x168, 0x16D), ('f', 0xD0, 0xD5))],
    [('f', 0xE0, 0xE5), ('f', 0xE6, 0xEB), ('i', 0xEC, 0xEF), ('diff', ('f', 0x170, 0x175), ('f', 0xE0, 0xE5))],
    [('f', 0xF0, 0xF5), ('f', 0xF6, 0xFB), ('i', 0xFC, 0xFF), ('diff', ('f', 0x178, 0x17D), ('f', 0xF0, 0xF5))],
]


class RecordType(Enum):
    FLOAT = "f"
    INTEGER = "i"
    DIFFERENCE = "diff"


class HexBinding:
    STRING_MODE = True

    def __init__(self):
        self.hex = None

    @classmethod
    def bytes_to_string(cls, hex_bytes):
        raw_data = []
        for b in hex_bytes.todict().values():
            raw_data += hex(b).replace("0x", "").rjust(2, '0')
        return "".join(raw_data)

    def load_from_file(self, filename):
        self.hex = IntelHex(filename)

    def get_raw_data(self, start_addr, end_addr):
        hex_bytes = self.hex[start_addr:end_addr + 1]
        return self.bytes_to_string(hex_bytes)

    def get_check_sum(self):
        raw = self.get_raw_data(0x180, 0x181)
        return raw[2:] + raw[:2]

    def get_integer(self, start_addr, end_addr, string_mode):
        if string_mode:
            return self.get_raw_data(start_addr, end_addr)
        else:
            return int(self.get_raw_data(start_addr, end_addr))

    def get_float(self, start_addr, end_addr, string_mode):
        raw = self.get_raw_data(start_addr, end_addr)
        integer = raw[:-2]
        decimal = raw[-2:]
        if string_mode:
            return integer + "." + decimal
        else:
            return float(integer + "." + decimal)

    def get_number(self, record_type, start_addr, end_addr, string_mode=False):
        if type(record_type) is not RecordType:
            record_type = RecordType(record_type)
        if record_type is RecordType.INTEGER:
            return self.get_integer(start_addr, end_addr, string_mode)
        elif record_type is RecordType.FLOAT:
            return self.get_float(start_addr, end_addr, string_mode)
        else:
            logging.warning(f"Unknown record type: {record_type}")
            return None

    def get_mapped_hex_data(self, row, column):
        record_type, start_addr, end_addr = HEX_DATA_MAPPING[row][column]
        record_type = RecordType(record_type)
        if record_type is RecordType.DIFFERENCE:
            a = self.get_number(*start_addr, False)
            b = self.get_number(*end_addr, False)
            return_value = round(a - b, 2)
        else:
            return_value = self.get_number(record_type, start_addr, end_addr, False)
        logging.debug(f"[{row}:{column}] = {return_value}")
        return return_value


# h = HexBinding()
# h.load_from_file("../dump.hex")
# # raw = h.get_raw_hex_data(0x0C, 0x0F)
# # print(f"RAW: {raw}")
# dt = h.get_mapped_hex_data(0, 4)
# print(dt)
