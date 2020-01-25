import logging

HOSE_FIELD_NAMES = [
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

        self.options = [
            self.name,

        ]

    def get_field_by_name(self, name):
        if name == HOSE_FIELD_NAMES[0]:
            return self.name
        elif name == HOSE_FIELD_NAMES[1]:
            return self.good_impulse_count
        elif name == HOSE_FIELD_NAMES[2]:
            return self.amount
        elif name == HOSE_FIELD_NAMES[3]:
            return self.refill_count
        elif name == HOSE_FIELD_NAMES[4]:
            return self.bad_impulse_amount
        else:
            logging.error(f"Unknown hose variable name: {name}")
