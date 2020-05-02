class Bank():

    def deposit_to_account(self, account, amount):
        account._deposit(amount)

    def withdraw_from_account(self, account, amount):
        account._withdraw(amount)

    def e_transfer(self, account_from, account_to, amount):
        initial_from_balance = account_from.balance
        account_from._withdraw(amount)

        if (account_from.balance == initial_from_balance):
            return

        account_to._deposit(amount)