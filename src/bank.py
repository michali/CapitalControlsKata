class Bank():

    def deposit_to_account(self, account, amount):
        account._deposit(amount)

    def withdraw_from_account(self, account, amount):
        account._withdraw(amount)

    def transfer(self, account_from, account_to, amount):
        initial_from_balance = account_from.balance
        account_from._transfer(account_to, amount)