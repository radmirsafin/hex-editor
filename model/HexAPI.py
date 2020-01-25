from model.RecordType import RecordType
from model.Hose import Hose
from model.Hex import Hex

HEX_DATA_MAPPING = [
    ["A1", (RecordType.FLOAT, 0x00, 0x05), (RecordType.FLOAT, 0x06, 0x0B), (RecordType.INTEGER, 0x0C, 0x0F), (RecordType.FLOAT, 0x100, 0x105)],
    ["A2", (RecordType.FLOAT, 0x10, 0x15), (RecordType.FLOAT, 0x16, 0x1B), (RecordType.INTEGER, 0x1C, 0x1F), (RecordType.FLOAT, 0x108, 0x10D)],
    ["A3", (RecordType.FLOAT, 0x20, 0x25), (RecordType.FLOAT, 0x26, 0x2B), (RecordType.INTEGER, 0x2C, 0x2F), (RecordType.FLOAT, 0x110, 0x115)],
    ["A4", (RecordType.FLOAT, 0x30, 0x35), (RecordType.FLOAT, 0x36, 0x3B), (RecordType.INTEGER, 0x3C, 0x3F), (RecordType.FLOAT, 0x118, 0x11D)],
    ["A5", (RecordType.FLOAT, 0x40, 0x45), (RecordType.FLOAT, 0x46, 0x4B), (RecordType.INTEGER, 0x4C, 0x4F), (RecordType.FLOAT, 0x120, 0x125)],
    ["A6", (RecordType.FLOAT, 0x50, 0x55), (RecordType.FLOAT, 0x56, 0x5B), (RecordType.INTEGER, 0x5C, 0x5F), (RecordType.FLOAT, 0x128, 0x12D)],
    ["A7", (RecordType.FLOAT, 0x60, 0x65), (RecordType.FLOAT, 0x66, 0x6B), (RecordType.INTEGER, 0x6C, 0x6F), (RecordType.FLOAT, 0x130, 0x135)],
    ["A8", (RecordType.FLOAT, 0x70, 0x75), (RecordType.FLOAT, 0x76, 0x7B), (RecordType.INTEGER, 0x7C, 0x7F), (RecordType.FLOAT, 0x138, 0x13D)],
    ["B1", (RecordType.FLOAT, 0x80, 0x85), (RecordType.FLOAT, 0x86, 0x8B), (RecordType.INTEGER, 0x8C, 0x8F), (RecordType.FLOAT, 0x140, 0x145)],
    ["B2", (RecordType.FLOAT, 0x90, 0x95), (RecordType.FLOAT, 0x96, 0x9B), (RecordType.INTEGER, 0x9C, 0x9F), (RecordType.FLOAT, 0x148, 0x14D)],
    ["B3", (RecordType.FLOAT, 0xA0, 0xA5), (RecordType.FLOAT, 0xA6, 0xAB), (RecordType.INTEGER, 0xAC, 0xAF), (RecordType.FLOAT, 0x150, 0x155)],
    ["B4", (RecordType.FLOAT, 0xB0, 0xB5), (RecordType.FLOAT, 0xB6, 0xBB), (RecordType.INTEGER, 0xBC, 0xBF), (RecordType.FLOAT, 0x158, 0x15D)],
    ["B5", (RecordType.FLOAT, 0xC0, 0xC5), (RecordType.FLOAT, 0xC6, 0xCB), (RecordType.INTEGER, 0xCC, 0xCF), (RecordType.FLOAT, 0x160, 0x165)],
    ["B6", (RecordType.FLOAT, 0xD0, 0xD5), (RecordType.FLOAT, 0xD6, 0xDB), (RecordType.INTEGER, 0xDC, 0xDF), (RecordType.FLOAT, 0x168, 0x16D)],
    ["B7", (RecordType.FLOAT, 0xE0, 0xE5), (RecordType.FLOAT, 0xE6, 0xEB), (RecordType.INTEGER, 0xEC, 0xEF), (RecordType.FLOAT, 0x170, 0x175)],
    ["B8", (RecordType.FLOAT, 0xF0, 0xF5), (RecordType.FLOAT, 0xF6, 0xFB), (RecordType.INTEGER, 0xFC, 0xFF), (RecordType.FLOAT, 0x178, 0x17D)],
]


class HexAPI:
    def __init__(self, filename):
        self.hex = Hex(filename)

    def get_data(self):
        hoses = []
        for rw in HEX_DATA_MAPPING:
            hoses.append(Hose(
                name=rw[0],
                good_impulse_count=self.hex.get_number(*rw[1]),
                amount=self.hex.get_number(*rw[2]),
                refill_count=self.hex.get_number(*rw[3]),
                total_impulse_count=self.hex.get_number(*rw[4])
            ))
        return hoses

    def get_checksum(self):
        return self.hex.get_checksum()
