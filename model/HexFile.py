import logging
import pathlib
from intelhex import IntelHex
from model.Exceptions import *
from ctypes import CDLL, c_ubyte, c_ulong


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


class HexFile:
    INTEGER_STRING_SIZE = 8
    FLOAT_STRING_SIZE = 12

    def __init__(self, filename):
        try:
            self.hex = IntelHex(filename)
        except Exception as exc:
            exc = InvalidHexFileException(filename=filename, detailed_text=str(exc))
            logging.error(exc)
            raise exc

        self.crc_library_so = pathlib.Path(pathlib.Path().absolute(), 'crc_library.dll')
        if not self.crc_library_so.exists():
            exc = LibraryNotFoundException(library_file=self.crc_library_so)
            logging.error(exc)
            raise exc

        self.crc_library = CDLL(str(self.crc_library_so))

        self.checksum = self.get_checksum()
        original = self.load_checksum()
        if self.checksum != original:
            exc = InvalidChecksumException(original_checksum=original, calculated_checksum=self.checksum)
            logging.error(exc)
            raise exc

    def load_number(self, record_type, start_addr, end_addr):
        if record_type is int:
            return self.load_integer(start_addr, end_addr)
        elif record_type is float:
            return self.load_float(start_addr, end_addr)
        else:
            exc = UnsupportedRecordTypeException(record_type=record_type)
            logging.error(exc)
            raise exc

    def load_integer(self, start_addr, end_addr):
        num = int(self._load_range(start_addr, end_addr))
        logging.debug(f"Loaded integer from {hex(start_addr)}-{hex(end_addr)}: {num}")
        return num

    def load_float(self, start_addr, end_addr):
        raw = self._load_range(start_addr, end_addr)
        num = str(raw[:-2]) + "." + str(raw[-2:])
        num = float(num)
        logging.debug(f"Loaded float from {hex(start_addr)}-{hex(end_addr)}: {num}")
        return num

    def _load_range(self, start_addr, end_addr):
        data = []
        for b in self.hex[start_addr:end_addr + 1].todict().values():
            data += hex(b).replace("0x", "").rjust(2, '0')
        result = "".join(data).upper()
        logging.debug(f"Loaded data from {hex(start_addr)}-{hex(end_addr)}: {result}")
        return result

    def set_number(self, record_type, start_addr, end_addr, value_to_set):
        if record_type is int:
            return self.set_integer(start_addr, end_addr, value_to_set)
        elif record_type is float:
            return self.set_float(start_addr, end_addr, value_to_set)
        else:
            exc = UnsupportedRecordTypeException(record_type=record_type)
            logging.error(exc)
            raise exc

    def set_integer(self, start_addr, end_addr, value_to_set):
        string_value = str(value_to_set).rjust(self.INTEGER_STRING_SIZE, '0')

        if len(string_value) > self.INTEGER_STRING_SIZE:
            exc = OutOfMemoryException(max_size=self.INTEGER_STRING_SIZE / 2, data_type='int',
                                       start_addr=hex(start_addr), end_addr=hex(end_addr))
            logging.error(exc)
            raise exc

        logging.debug(f"Write integer {string_value} to {hex(start_addr)}-{hex(end_addr)}")
        self._set_range(start_addr, string_value)

    def set_float(self, start_addr, end_addr, value_to_set):
        integer = int(value_to_set)
        decimal = round(value_to_set - integer, 2)
        string_value = str(integer).rjust(10, '0') + str(decimal)[2:].ljust(2, '0')

        if len(string_value) > self.FLOAT_STRING_SIZE:
            exc = OutOfMemoryException(max_size=self.FLOAT_STRING_SIZE / 2, data_type='float',
                                       start_addr=hex(start_addr), end_addr=hex(end_addr))
            logging.error(exc)
            raise exc

        logging.debug(f"Write float {string_value} to {hex(start_addr)}-{hex(end_addr)}")
        self._set_range(start_addr, string_value)

    def _set_range(self, start_addr, value_to_set):
        if len(value_to_set) % 2 != 0:
            exc = OddDataBlockException(block_size=len(value_to_set), value=value_to_set)
            logging.error(exc)
            raise exc

        logging.debug(f"Write data {value_to_set} starts with {hex(start_addr)}")
        curr_addr = start_addr
        for frame in ["".join(i) for i in grouper(value_to_set, 2)]:
            frame_as_int = int(bytes(frame.encode()), 16)
            self.hex[curr_addr] = frame_as_int
            curr_addr += 1

    def load_checksum(self):
        checksum = self._load_range(0x180, 0x181)
        checksum = checksum[2:] + checksum[:2]
        checksum = "0x" + checksum.upper()
        logging.info(f"Checksum loaded from hex data: {checksum}")
        return checksum

    def get_checksum(self):
        checksum_data = self.hex[0x000:0x17F + 1].todict().values()
        c_array = (c_ubyte * len(checksum_data))(*checksum_data)
        checksum = self.crc_library.crcbitbybit(c_array, c_ulong(len(checksum_data)))
        checksum = "0x" + hex(checksum).replace("0x", "").upper()
        logging.info(f"Checksum calculated: {checksum}")
        return checksum

    def write_dump_to_file(self, filename):
        checksum = self.get_checksum()
        checksum = checksum.replace("0x", "")
        checksum = checksum[2:] + checksum[:2]
        self._set_range(0x180, checksum)
        logging.info(f"Write checksum: {checksum}")

        for addr, value in self.hex[0x0000:0x0181 + 1].todict().items():
            new_addr = 0x2D6 + addr
            logging.debug(f"Duplicate data from {hex(addr)} to {hex(new_addr)}")
            self.hex[new_addr] = value

        self.hex.write_hex_file(filename)
