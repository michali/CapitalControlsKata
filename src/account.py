class Account():
    
    def __init__(self, initial_amount = None):
        if initial_amount is None:
            self.balance = 0
        else:
            self.balance = initial_amount

    def _deposit(self, amount):
        self.balance += amount

    def _withdraw(self, amount):
        if (amount <= self.balance):
            self.balance -= amount

    def _transfer(self, account, amount):
        if (amount <= self.balance):
            self.balance -= amount
            account.balance += amount
    