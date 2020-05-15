import datetime
from .transaction import OperationResult, TransactionType
from .restriction import *

class Bank():

    def __init__(self, datetimeprovider = datetime.datetime):
        self.__datetimeprovider = datetimeprovider
        self.__restrictions = DailyLimit().set_next(TransactionsToday(self.__datetimeprovider))

    def deposit_to_account(self, account, amount):
        return account._deposit(amount, self.__datetimeprovider.now())

    def withdraw_from_account(self, account, amount):
        if self.__restrictions.is_restricted(account, amount):
            return OperationResult.NotAllowed
         
        return account._withdraw(amount, self.__datetimeprovider.now())

    def transfer(self, account_from, account_to, amount):
        date = self.__datetimeprovider.now()
        withdrawal = account_from._withdraw(amount, date)

        if (withdrawal == OperationResult.InsufficientFunds):
            return withdrawal

        return account_to._deposit(amount, date)

    def transfer_abroad(self, account, amount):
        return OperationResult.NotAllowed