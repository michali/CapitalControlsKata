import datetime

class Bank():

    def __init__(self, datetimeprovider = datetime.datetime):
        self.__datetimeprovider = datetimeprovider

    def deposit_to_account(self, account, amount):
        return account._deposit(amount, self.__datetimeprovider.now())

    def withdraw_from_account(self, account, amount):
        return account._withdraw(amount, self.__datetimeprovider.now())
       