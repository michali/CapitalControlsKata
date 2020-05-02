class Account():
    
    def __init__(self, initial_amount = None):
        if initial_amount is None:
            self.balance = 0
        else:
            self.balance = initial_amount

    def _deposit(self, amount):
        self.balance += amount

    def _withdraw(self, amount):
        self.balance -= amount
    