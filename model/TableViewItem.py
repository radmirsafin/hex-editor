class TableViewItem:
    def __init__(self, name, counter, amount, refill_count, bad_count=None, total_count=None):
        self.name = str(name)
        self.counter = float(counter)
        self.amount = float(amount)
        self.refill_count = int(refill_count)

        if bad_count is None and total_count is None:
            raise ValueError("Cannot initialize TableViewItem! bad_count == None and total_count == None")

        if bad_count is not None:
            self.bad_count = float(bad_count)
            self.total_count = round(self.bad_count + self.counter, 2)
        else:
            self.total_count = float(total_count)
            self.bad_count = round(self.total_count - self.counter, 2)

    def __repr__(self):
        return f"TableViewItem<{self.name}, {self.counter}, {self.amount}, " \
               f"{self.refill_count}, {self.bad_count}, {self.total_count}>"
