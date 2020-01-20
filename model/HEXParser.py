from intelhex import IntelHex

class HEXParser:
    def __init__(self):
        self.hex = None

    def parse_from_file(self, filename):
        self.hex = IntelHex(filename)
        print(hex)

    def get_raw_hex_data(self, start, end):
        hex_bytes = self.hex[start:end + 1]
        raw_data = []
        for r in hex_bytes.todict().values():
            bt = hex(r).replace("0x", "")
            raw_data += bt.rjust(2, '0')
        return "".join(raw_data)

    def get_number_from_hex(self, start, end):
        raw = self.get_raw_hex_data(start, end)
        integer = raw[:-2]
        decimal = raw[-2:]
        return float(integer + "." + decimal)


h = HEXParser()
h.parse_from_file("../dump.hex")
dt = h.get_number_from_hex(10, 15)
print(dt)
