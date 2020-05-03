class Bank():

    def deposit_to_account(self, account, amount):
        return account._deposit(amount)

    def withdraw_from_account(self, account, amount):
        return account._withdraw(amount)

    def transfer(self, account_from, account_to, amount):
        return account_from._transfer(account_to, amount)