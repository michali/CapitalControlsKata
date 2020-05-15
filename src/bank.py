from datetime import datetime, timedelta
from .transaction import OperationResult, TransactionType

class Bank():

    __max_daily_limit = 60

    def __init__(self, datetimeprovider = datetime):
        self.__datetimeprovider = datetimeprovider

    def deposit_to_account(self, account, amount):
        return account._deposit(amount, self.__datetimeprovider.now())

    def withdraw_from_account(self, account, amount):           
        amount_already_drawn = 0

        for trn in account.Transactions:
            if trn.Type == TransactionType.Debit and trn.DateTime.date() == self.__datetimeprovider.now().date():
                amount_already_drawn += trn.Amount

        if amount_already_drawn + amount > Bank.__max_daily_limit:
            diff = amount_already_drawn + amount - Bank.__max_daily_limit
            money_drawn_previous_day = 0
            for trn in account.Transactions:
                if trn.Type == TransactionType.Debit and trn.DateTime.date() == self.__datetimeprovider.now().date() - timedelta(days = 1):
                    money_drawn_previous_day += trn.Amount

            if money_drawn_previous_day + diff <= Bank.__max_daily_limit:
                return account._withdraw(amount, self.__datetimeprovider.now())

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
