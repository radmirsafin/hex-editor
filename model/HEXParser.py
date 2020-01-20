from intelhex import IntelHex


class HEXParser:
    def __init__(self):
        self.hex = None

    def parse_from_file(self, filename):
        self.hex = IntelHex(filename)
        print(hex)
