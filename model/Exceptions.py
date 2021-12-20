class HexEditorException(Exception):
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', '')
        self.informative_text = kwargs.get('informative_text', '')
        self.detailed_text = kwargs.get('detailed_text', '')

    def __str__(self):
        return f"""
            Error message:
                Text: {self.text}
                Info: {self.informative_text}
                Details: {self.detailed_text}
        """


class InvalidHexFileException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = kwargs.get('filename', '')
        self.text = f"Ошибка при загрузке файла '{self.filename}'"


class InvalidChecksumException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Неверная контрольная сумма"

        self.original_checksum = kwargs.get('original_checksum', 'None')
        self.calculated_checksum = kwargs.get('calculated_checksum', 'None')
        self.informative_text = f"Рассчитанная контрольная сумма не совпадает с сохраненной в фале. " \
                                f"Расчитанное значение {self.calculated_checksum}. Сохраненное {self.original_checksum}"


class UnsupportedRecordTypeException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Невозможно загрузить данные"
        self.record_type = kwargs.get("record_type", "unknown")
        self.detailed_text = f"Использован неизвестный тип записи: {self.record_type}"


class OutOfMemoryException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Выход за пределы доступной памяти"
        self.max_size = kwargs.get("max_size", "")
        self.data_type = kwargs.get("data_type", "")
        self.start_addr = kwargs.get("start_addr", "")
        self.end_addr = kwargs.get("end_addr", "")
        self.informative_text = f"Для типа {self.data_type}, выделено {self.max_size} байт памяти. " \
                                f"Неудачная попытка записи данных по адресу {self.start_addr}-{self.end_addr}"


class OddDataBlockException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Ошибка при записи данных"

        self.block_size = kwargs.get("block_size", 'None')
        self.value = kwargs.get("value", "None")
        self.informative_text = f"Размер блока данных для записи должен быть кратен 2. " \
                                f"Попытка записи блока {self.value} размером {self.block_size}"


class InvalidTableItemValueException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Ошибка при чтении данных из таблицы"
        self.row_number = kwargs.get("row_number", "None")
        self.informative_text = f"Невозможно преобразовать данные из строки: {self.row_number}"


class LibraryNotFoundException(HexEditorException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Отсутствует необходимый модуль"
        self.library_file = kwargs.get("library_file", "None")
        self.informative_text = f"Не найден файл {self.library_file}"
