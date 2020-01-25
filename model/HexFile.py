import logging
import pathlib
from intelhex import IntelHex
from model.Exceptions import *
from ctypes import CDLL, c_ubyte, c_ulong


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


class HexFile:
    def __init__(self, filename):
        try:
            self.hex = IntelHex(filename)
        except Exception as exc:
            exc = InvalidHexFile(f"Ошибка при загрузке файла {filename}", detailed_text=str(exc))
            logging.error(exc)
            raise exc

        self.crc_library_so = pathlib.Path(__file__).parent.absolute() / 'crc_library.so'
        if not self.crc_library_so.exists():
            raise FileNotFoundError(f"{self.crc_library_so} file not found!")
        self.crc_library = CDLL(self.crc_library_so)

    def load_number(self, record_type, start_addr, end_addr):
        if record_type is int:
            return self.load_integer(start_addr, end_addr)
        elif record_type is float:
            return self.load_float(start_addr, end_addr)
        else:
            exc = UnsupportedRecordTypeException(
                f"Невозможно загрузить данные",
                informative_text=f"Использован неизвестный тип записи: {record_type}")
            logging.error(exc)
            raise exc

    def load_integer(self, start_addr, end_addr):
        num = int(self._load_range(start_addr, end_addr))
        logging.debug(f"Loaded integer value: {num} from {hex(start_addr)}-{hex(end_addr)}")
        return num

    def load_float(self, start_addr, end_addr):
        raw = self._load_range(start_addr, end_addr)
        num = str(raw[:-2]) + "." + str(raw[-2:])
        num = float(num)
        logging.debug(f"Loaded float value: {num} from {hex(start_addr)}-{hex(end_addr)}")
        return num

    def _load_range(self, start_addr, end_addr):
        data = []
        for b in self.hex[start_addr:end_addr + 1].todict().values():
            data += hex(b).replace("0x", "").rjust(2, '0')
        return "".join(data).upper()

    def set_number(self, record_type, start_addr, end_addr, value_to_set):
        if record_type is int:
            return self.set_integer(start_addr, end_addr, value_to_set)
        elif record_type is float:
            return self.set_float(start_addr, end_addr, value_to_set)
        else:
            exc = UnsupportedRecordTypeException(
                "Невозможно выгрузить данные",
                informative_text=f"Использован неизвестный тип записи: {record_type}")
            logging.error(exc)
            raise exc

    def set_integer(self, start_addr, end_addr, value_to_set):
        string_value = str(value_to_set).rjust(8, '0')
        if len(string_value) > 8:
            exc = OutOfMemoryException(
                "Выход за пределы памяти",
                informative_text=f"Для типа int() выделено 4 байта памяти. Неудачная попытка записи '{value_to_set}' "
                                 f"по адресам {hex(start_addr)}-{hex(end_addr)}")
            logging.error(exc)
            raise exc

        logging.debug(f"Set integer value: {string_value} to {hex(start_addr)}-{hex(end_addr)}")
        self._set_range(start_addr, string_value)

    def set_float(self, start_addr, end_addr, value_to_set):
        integer = int(value_to_set)
        decimal = round(value_to_set - integer, 2)
        string_value = str(integer).rjust(10, '0') + str(decimal)[2:].ljust(2, '0')
        if len(string_value) > 12:
            exc = OutOfMemoryException(
                "Выход за пределы памяти",
                informative_text=f"Для типа float() выделено 6 байт памяти. Неудачная попытка записи '{value_to_set}' "
                                 f"по адресам {hex(start_addr)}-{hex(end_addr)}")
            logging.error(exc)
            raise exc

        logging.debug(f"Set float value: {string_value} to {hex(start_addr)}-{hex(end_addr)}")
        self._set_range(start_addr, string_value)

    def _set_range(self, start_addr, value_to_set):
        if len(value_to_set) % 2 != 0:
            exc = OddDataBlockException(
                f"Ошибка записи",
                informative_text=f"Размер блока данных для записи должен быть кратен 2. "
                                 f"Попытка записи блока размера: {len(value_to_set)}")
            logging.error(exc)
            raise exc

        curr_addr = start_addr
        for frame in ["".join(i) for i in grouper(value_to_set, 2)]:
            frame_as_int = int(bytes(frame.encode()), 16)
            self.hex[curr_addr] = frame_as_int
            curr_addr += 1

    def load_checksum(self):
        checksum = self._load_range(0x180, 0x181)
        checksum = checksum[2:] + checksum[:2]
        checksum = "0x" + checksum.upper()
        logging.info(f"Checksum loaded from file: {checksum}")
        return checksum

    def get_checksum(self):
        checksum_data = self.hex[0x000:0x17F + 1].todict().values()
        c_array = (c_ubyte * len(checksum_data))(*checksum_data)
        checksum = self.crc_library.crcbitbybit(c_array, c_ulong(len(checksum_data)))
        checksum = "0x" + hex(checksum).replace("0x", "").upper()
        logging.info(f"Checksum calculated from data: {checksum}")
        return checksum

    def write_dump_to_file(self, filename):
        self.hex.write_hex_file(filename)
