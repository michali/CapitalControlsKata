class Bank():

    def deposit_to_account(self, account, amount):
        return account._deposit(amount)

    def withdraw_from_account(self, account, amount):
        return account._withdraw(amount)
       