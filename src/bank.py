class Bank():

    def deposit_to_account(self, account, amount):
        account._deposit(amount)

    def withdraw_from_account(self, account, amount):
        account._withdraw(amount)