class HexEditorException(Exception):
    def __init__(self, *args, **kwargs):
        self.text = args[0]
        self.informative_text = kwargs.get('informative_text', '')
        self.detailed_text = kwargs.get('detailed_text', '')


class InvalidHexFile(HexEditorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidTableItemValueException(HexEditorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnsupportedRecordTypeException(HexEditorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OutOfMemoryException(HexEditorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OddDataBlockException(HexEditorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
