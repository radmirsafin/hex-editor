
class Sleeve:
    def __init__(self, name, counter, summary, refill_count, impulse_count):
        self.name = name
        self.counter = counter
        self.summary = summary
        self.refill_count = refill_count
        self.impulse_count = impulse_count

        self.bad_impulse_count = impulse_count - counter
