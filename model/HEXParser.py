from intelhex import IntelHex

HEX_DATA_TEMPLATE = [
    [('f', 0x00, 0x05), ('f', 0x06, 0x0B), ('i', 0x0C, 0x0F), ('sub', ('f', 0x100, 0x105), ('f', 0x00, 0x05))],
    [('f', 0x10, 0x15), ('f', 0x16, 0x1B), ('i', 0x1C, 0x1F), ('sub', ('f', 0x108, 0x10D), ('f', 0x10, 0x15))],
    [('f', 0x20, 0x25), ('f', 0x26, 0x2B), ('i', 0x2C, 0x2F), ('sub', ('f', 0x110, 0x115), ('f', 0x20, 0x25))],
    [('f', 0x30, 0x35), ('f', 0x36, 0x3B), ('i', 0x3C, 0x3F), ('sub', ('f', 0x118, 0x11D), ('f', 0x30, 0x35))],
    [('f', 0x40, 0x45), ('f', 0x46, 0x4B), ('i', 0x4C, 0x4F), ('sub', ('f', 0x120, 0x125), ('f', 0x40, 0x45))],
    [('f', 0x50, 0x55), ('f', 0x56, 0x5B), ('i', 0x5C, 0x5F), ('sub', ('f', 0x128, 0x12D), ('f', 0x50, 0x55))],
    [('f', 0x60, 0x65), ('f', 0x66, 0x6B), ('i', 0x6C, 0x6F), ('sub', ('f', 0x130, 0x135), ('f', 0x60, 0x65))],
    [('f', 0x70, 0x75), ('f', 0x76, 0x7B), ('i', 0x7C, 0x7F), ('sub', ('f', 0x138, 0x13D), ('f', 0x70, 0x75))],
    [('f', 0x80, 0x85), ('f', 0x86, 0x8B), ('i', 0x8C, 0x8F), ('sub', ('f', 0x140, 0x145), ('f', 0x80, 0x85))],
    [('f', 0x90, 0x95), ('f', 0x96, 0x9B), ('i', 0x9C, 0x9F), ('sub', ('f', 0x148, 0x14D), ('f', 0x90, 0x95))],
    [('f', 0xA0, 0xA5), ('f', 0xA6, 0xAB), ('i', 0xAC, 0xAF), ('sub', ('f', 0x150, 0x155), ('f', 0xA0, 0xA5))],
    [('f', 0xB0, 0xB5), ('f', 0xB6, 0xBB), ('i', 0xBC, 0xBF), ('sub', ('f', 0x158, 0x15D), ('f', 0xB0, 0xB5))],
    [('f', 0xC0, 0xC5), ('f', 0xC6, 0xCB), ('i', 0xCC, 0xCF), ('sub', ('f', 0x160, 0x165), ('f', 0xC0, 0xC5))],
    [('f', 0xD0, 0xD5), ('f', 0xD6, 0xDB), ('i', 0xDC, 0xDF), ('sub', ('f', 0x168, 0x16D), ('f', 0xD0, 0xD5))],
    [('f', 0xE0, 0xE5), ('f', 0xE6, 0xEB), ('i', 0xEC, 0xEF), ('sub', ('f', 0x170, 0x175), ('f', 0xE0, 0xE5))],
    [('f', 0xF0, 0xF5), ('f', 0xF6, 0xFB), ('i', 0xFC, 0xFF), ('sub', ('f', 0x178, 0x17D), ('f', 0xF0, 0xF5))],
]


class HEXParser:
    def __init__(self):
        self.hex = None

    def parse_from_file(self, filename):
        self.hex = IntelHex(filename)

    def get_raw_hex_data(self, start, end):
        hex_bytes = self.hex[start:end + 1]
        raw_data = []
        for r in hex_bytes.todict().values():
            bt = hex(r).replace("0x", "")
            raw_data += bt.rjust(2, '0')
        return "".join(raw_data)

    def get_number_from_hex(self, rec_type, start, end):
        if rec_type == 'i':
            return self.get_integer_from_hex(start, end)
        elif rec_type == 'f':
            return self.get_float_from_hex(start, end)
        else:
            return None

    def get_float_from_hex(self, start, end):
        raw = self.get_raw_hex_data(start, end)
        integer = raw[:-2]
        decimal = raw[-2:]
        return float(integer + "." + decimal)

    def get_integer_from_hex(self, start, end):
        return int(self.get_raw_hex_data(start, end))

    def get_hex_table_data(self, row, column):
        rec_type, first, second = HEX_DATA_TEMPLATE[row][column]

        if rec_type == 'sub':
            a = self.get_number_from_hex(*first)
            b = self.get_number_from_hex(*second)
            return round(a - b, 2)
        else:
            return self.get_number_from_hex(rec_type, first, second)


h = HEXParser()
h.parse_from_file("../dump.hex")
# raw = h.get_raw_hex_data(0x0C, 0x0F)
# print(f"RAW: {raw}")
dt = h.get_hex_table_data(9, 3)
print(dt)
