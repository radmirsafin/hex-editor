from intelhex import IntelHex
from model.RecordType import RecordType
from model.Sleeve import Sleeve
import logging


HEX_DATA_MAPPING = [
    ["A1", ('f', 0x00, 0x05), ('f', 0x06, 0x0B), ('i', 0x0C, 0x0F), ('f', 0x100, 0x105)],
    ["A2", ('f', 0x10, 0x15), ('f', 0x16, 0x1B), ('i', 0x1C, 0x1F), ('f', 0x108, 0x10D)],
    ["A3", ('f', 0x20, 0x25), ('f', 0x26, 0x2B), ('i', 0x2C, 0x2F), ('f', 0x110, 0x115)],
    ["A4", ('f', 0x30, 0x35), ('f', 0x36, 0x3B), ('i', 0x3C, 0x3F), ('f', 0x118, 0x11D)],
    ["A5", ('f', 0x40, 0x45), ('f', 0x46, 0x4B), ('i', 0x4C, 0x4F), ('f', 0x120, 0x125)],
    ["A6", ('f', 0x50, 0x55), ('f', 0x56, 0x5B), ('i', 0x5C, 0x5F), ('f', 0x128, 0x12D)],
    ["A7", ('f', 0x60, 0x65), ('f', 0x66, 0x6B), ('i', 0x6C, 0x6F), ('f', 0x130, 0x135)],
    ["A8", ('f', 0x70, 0x75), ('f', 0x76, 0x7B), ('i', 0x7C, 0x7F), ('f', 0x138, 0x13D)],
    ["B1", ('f', 0x80, 0x85), ('f', 0x86, 0x8B), ('i', 0x8C, 0x8F), ('f', 0x140, 0x145)],
    ["B2", ('f', 0x90, 0x95), ('f', 0x96, 0x9B), ('i', 0x9C, 0x9F), ('f', 0x148, 0x14D)],
    ["B3", ('f', 0xA0, 0xA5), ('f', 0xA6, 0xAB), ('i', 0xAC, 0xAF), ('f', 0x150, 0x155)],
    ["B4", ('f', 0xB0, 0xB5), ('f', 0xB6, 0xBB), ('i', 0xBC, 0xBF), ('f', 0x158, 0x15D)],
    ["B5", ('f', 0xC0, 0xC5), ('f', 0xC6, 0xCB), ('i', 0xCC, 0xCF), ('f', 0x160, 0x165)],
    ["B6", ('f', 0xD0, 0xD5), ('f', 0xD6, 0xDB), ('i', 0xDC, 0xDF), ('f', 0x168, 0x16D)],
    ["B7", ('f', 0xE0, 0xE5), ('f', 0xE6, 0xEB), ('i', 0xEC, 0xEF), ('f', 0x170, 0x175)],
    ["B8", ('f', 0xF0, 0xF5), ('f', 0xF6, 0xFB), ('i', 0xFC, 0xFF), ('f', 0x178, 0x17D)],
]


class HexParser:
    def __init__(self, filename):
        self.hex = IntelHex(filename)

    def get_mapped_data(self):
        sleeves = []
        for rw in HEX_DATA_MAPPING:
            name = rw[0]
            counter = self.get_number(*rw[1])
            summary = self.get_number(*rw[2])
            refill_count = self.get_number(*rw[3])
            impulse_count = self.get_number(*rw[4])
            sleeves.append(Sleeve(name, counter, summary, refill_count, impulse_count))
        return sleeves

    def get_integer(self, start_addr, end_addr):
        return int(self.get_raw_data_from_range(start_addr, end_addr))

    def get_float(self, start_addr, end_addr):
        raw = self.get_raw_data_from_range(start_addr, end_addr)
        integer = raw[:-2]
        decimal = raw[-2:]
        return float(integer + "." + decimal)

    def get_number(self, record_type, start_addr, end_addr):
        if type(record_type) is not RecordType:
            record_type = RecordType(record_type)
        if record_type is RecordType.INTEGER:
            return self.get_integer(start_addr, end_addr)
        elif record_type is RecordType.FLOAT:
            return self.get_float(start_addr, end_addr)
        else:
            logging.error(f"Unknown record type: {record_type}")
            return None

    @classmethod
    def convert_bytes_to_string(cls, hex_bytes):
        raw_data = []
        for b in hex_bytes.todict().values():
            raw_data += hex(b).replace("0x", "").rjust(2, '0')
        return "".join(raw_data).upper()

    def get_raw_data_from_range(self, start_addr, end_addr):
        hex_bytes = self.hex[start_addr:end_addr + 1]
        return self.convert_bytes_to_string(hex_bytes)

    def get_check_sum(self):
        raw = self.get_raw_data_from_range(0x180, 0x181)
        raw = raw[2:] + raw[:2]
        return "0x" + raw.upper()

# h = HexBinding()
# h.load_from_file("../dump.hex")
# # raw = h.get_raw_hex_data(0x0C, 0x0F)
# # print(f"RAW: {raw}")
# dt = h.get_mapped_hex_data(0, 4)
# print(dt)
