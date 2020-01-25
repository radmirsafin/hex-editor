import logging

HOSE_FIELD_HEADERS = [
    "Рукав",
    "Счётчик",
    "Сумма",
    "Количество заправок",
    "Количество плохих импульсов",
]


class Hose:
    def __init__(self, name, good_impulse_count, amount, refill_count, total_impulse_count):
        self.name = name
        self.good_impulse_count = good_impulse_count
        self.amount = amount
        self.refill_count = refill_count
        self.total_impulse_count = total_impulse_count
        self.bad_impulse_amount = round(self.total_impulse_count - self.good_impulse_count, 2)

    def get_field_by_header(self, header):
        if header == HOSE_FIELD_HEADERS[0]:
            return self.name
        elif header == HOSE_FIELD_HEADERS[1]:
            return self.good_impulse_count
        elif header == HOSE_FIELD_HEADERS[2]:
            return self.amount
        elif header == HOSE_FIELD_HEADERS[3]:
            return self.refill_count
        elif header == HOSE_FIELD_HEADERS[4]:
            return self.bad_impulse_amount
        else:
            logging.error(f"Unknown hose variable name: {header}")
