import logging
import pathlib

from intelhex import IntelHex
from model.RecordType import RecordType
from ctypes import CDLL, c_ubyte, c_ulong


class Hex:
    def __init__(self, filename):
        self.hex = IntelHex(filename)
        self.checksum = self.load_checksum()

        self.crc_library_so = pathlib.Path(__file__).parent.absolute() / 'crc_library.so'
        if not self.crc_library_so.exists():
            raise FileNotFoundError(f"{self.crc_library_so} file not found!")
        self.crc_library = CDLL(self.crc_library_so)

    def load_range(self, start_addr, end_addr):
        data = []
        for b in self.hex[start_addr:end_addr + 1].todict().values():
            data += hex(b).replace("0x", "").rjust(2, '0')
        return "".join(data).upper()

    def load_integer(self, start_addr, end_addr):
        return int(self.load_range(start_addr, end_addr))

    def load_float(self, start_addr, end_addr):
        raw = self.load_range(start_addr, end_addr)
        integer = raw[:-2]
        decimal = raw[-2:]
        return float(integer + "." + decimal)

    def load_number(self, record_type, start_addr, end_addr):
        if record_type is RecordType.INTEGER:
            return self.load_integer(start_addr, end_addr)
        elif record_type is RecordType.FLOAT:
            return self.load_float(start_addr, end_addr)
        else:
            logging.error(f"Unknown record type: {record_type}")
            return None

    def load_checksum(self):
        raw = self.load_range(0x180, 0x181)
        raw = raw[2:] + raw[:2]
        return "0x" + raw.upper()

    def get_checksum(self):
        checksum_data = self.hex[0x000:0x17F + 1].todict().values()
        c_array = (c_ubyte * len(checksum_data))(*checksum_data)
        result = self.crc_library.crcbitbybit(c_array, c_ulong(len(checksum_data)))
        return "0x" + hex(result).replace("0x", "").upper()
