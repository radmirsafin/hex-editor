import logging
from model.TableViewItem import TableViewItem
from model.HexFile import HexFile


HEX_OBJECTS_MAP = {
    "A1": ((float, 0x00, 0x05), (float, 0x06, 0x0B), (int, 0x0C, 0x0F), (float, 0x100, 0x105)),
    "A2": ((float, 0x10, 0x15), (float, 0x16, 0x1B), (int, 0x1C, 0x1F), (float, 0x108, 0x10D)),
    "A3": ((float, 0x20, 0x25), (float, 0x26, 0x2B), (int, 0x2C, 0x2F), (float, 0x110, 0x115)),
    "A4": ((float, 0x30, 0x35), (float, 0x36, 0x3B), (int, 0x3C, 0x3F), (float, 0x118, 0x11D)),
    "A5": ((float, 0x40, 0x45), (float, 0x46, 0x4B), (int, 0x4C, 0x4F), (float, 0x120, 0x125)),
    "A6": ((float, 0x50, 0x55), (float, 0x56, 0x5B), (int, 0x5C, 0x5F), (float, 0x128, 0x12D)),
    "A7": ((float, 0x60, 0x65), (float, 0x66, 0x6B), (int, 0x6C, 0x6F), (float, 0x130, 0x135)),
    "A8": ((float, 0x70, 0x75), (float, 0x76, 0x7B), (int, 0x7C, 0x7F), (float, 0x138, 0x13D)),
    "B1": ((float, 0x80, 0x85), (float, 0x86, 0x8B), (int, 0x8C, 0x8F), (float, 0x140, 0x145)),
    "B2": ((float, 0x90, 0x95), (float, 0x96, 0x9B), (int, 0x9C, 0x9F), (float, 0x148, 0x14D)),
    "B3": ((float, 0xA0, 0xA5), (float, 0xA6, 0xAB), (int, 0xAC, 0xAF), (float, 0x150, 0x155)),
    "B4": ((float, 0xB0, 0xB5), (float, 0xB6, 0xBB), (int, 0xBC, 0xBF), (float, 0x158, 0x15D)),
    "B5": ((float, 0xC0, 0xC5), (float, 0xC6, 0xCB), (int, 0xCC, 0xCF), (float, 0x160, 0x165)),
    "B6": ((float, 0xD0, 0xD5), (float, 0xD6, 0xDB), (int, 0xDC, 0xDF), (float, 0x168, 0x16D)),
    "B7": ((float, 0xE0, 0xE5), (float, 0xE6, 0xEB), (int, 0xEC, 0xEF), (float, 0x170, 0x175)),
    "B8": ((float, 0xF0, 0xF5), (float, 0xF6, 0xFB), (int, 0xFC, 0xFF), (float, 0x178, 0x17D)),
}


class HexDataMapper:
    def __init__(self, filename):
        self.hex = HexFile(filename)

    def get_data(self):
        table_items = []
        for name, values in HEX_OBJECTS_MAP.items():
            it = TableViewItem(
                name=name,
                counter=self.hex.load_number(*values[0]),
                amount=self.hex.load_number(*values[1]),
                refill_count=self.hex.load_number(*values[2]),
                total_count=self.hex.load_number(*values[3])
            )
            logging.debug(f"Item loaded from file: {it}")
            table_items.append(it)
        return table_items

    def set_data(self, table_items):
        for item in table_items:
            self.hex.set_number(*HEX_OBJECTS_MAP[item.name][0], item.counter)
            self.hex.set_number(*HEX_OBJECTS_MAP[item.name][1], item.amount)
            self.hex.set_number(*HEX_OBJECTS_MAP[item.name][2], item.refill_count)
            self.hex.set_number(*HEX_OBJECTS_MAP[item.name][3], item.total_count)

    def get_checksum(self):
        return self.hex.get_checksum()

    def write_dump_to_file(self, filename):
        return self.hex.write_dump_to_file(filename)
