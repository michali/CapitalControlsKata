from .transaction import *
import datetime

class Account():
    
    def __init__(self):
        self.__balance = 0
        self.Transactions = set()

    @property
    def balance(self):
        return self.__balance
        
    def _deposit(self, amount, datetime):
        self.__balance += amount
        self.Transactions.add(Transaction(TransactionType.Credit, amount, datetime))
        return OperationResult.Success

    def _withdraw(self, amount, datetime):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.Transactions.add(Transaction(TransactionType.Debit, amount, datetime))
        return OperationResult.Success