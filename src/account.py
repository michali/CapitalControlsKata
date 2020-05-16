from .transaction import *
from datetime import datetime, timedelta

class Account():
    
    def __init__(self):
        self.__balance = 0
        self.__transactions = set()

    @property
    def Balance(self):
        return self.__balance

    @property
    def Transactions(self):
        return self.__transactions
        
    def _deposit(self, amount, datetime):
        self.__balance += amount
        self.__transactions.add(Transaction(TransactionType.Credit, amount, datetime))
        return OperationResult.Success

    def _withdraw(self, amount, datetime):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.__transactions.add(Transaction(TransactionType.Debit, amount, datetime))
        return OperationResult.Success

    def _transfer_abroad(self, amount, datetime):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.__transactions.add(Transaction(TransactionType.Debit, amount, datetime))
        return OperationResult.Success
        
    def _get_withdrawn_amount_this_week_so_far_for_date(self, date):
        day_of_week_index = date.weekday()
        money_withdrawn = 0
        if (day_of_week_index > 0):
            for i in range(0, day_of_week_index + 1):
                money_withdrawn += self.__get_withdrawn_amount_on_date(date - timedelta(days = i))

        return money_withdrawn
    
    def __get_withdrawn_amount_on_date(self, date):     
        amount = 0   
        for trn in self.Transactions:
            if trn.Type == TransactionType.Debit and trn.DateTime.date() == date.date():
                amount += trn.Amount
        
        return amount