class TableViewItem:
    def __init__(self, name, counter, amount, refill_count, bad_count=None, total_count=None):
        self.name = name
        self.counter = counter
        self.amount = amount
        self.refill_count = refill_count
        self.bad_count = bad_count
        self.total_count = total_count

        if self.bad_count is None and self.total_count is None:
            raise ValueError("Cannot initialize TableViewItem! bad_count == None and total_count == None")
        elif self.bad_count is None:
            self.bad_count = round(self.total_count - self.counter, 2)
        else:
            self.total_count = round(self.bad_count + self.counter, 2)

    def __repr__(self):
        return f"TableViewItem<{self.name}, {self.counter}, {self.amount}, " \
               f"{self.refill_count}, {self.bad_count}, {self.total_count}>"
