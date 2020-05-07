from .transaction import *
import datetime

class Account():
    
    def __init__(self, datetime = datetime.datetime):
        self.__balance = 0
        self.Transactions = set()
        self.datetime = datetime

    @property
    def balance(self):
        return self.__balance
        
    def _deposit(self, amount):
        self.__balance += amount
        self.Transactions.add(Transaction(TransactionType.Credit, amount, self.datetime.now()))
        return OperationResult.Success

    def _withdraw(self, amount):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.Transactions.add(Transaction(TransactionType.Debit, amount, self.datetime.now()))
        return OperationResult.Success