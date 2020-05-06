from .transaction import *
import datetime

class Account():
    
    def __init__(self, datetime = datetime.datetime):
        self.balance = 0
        self.Transactions = set()
        self.datetime = datetime
        
    def _deposit(self, amount):
        self.balance += amount
        self.Transactions.add(Transaction(TransactionType.Credit, amount, self.datetime.now()))
        return OperationResult.Success