class InvalidTableDataException(Exception):
    def __init__(self, message, row):
        self.message = message
        self.row = row


class SetHexDataException(Exception):
    def __init__(self, message):
        self.message = message
