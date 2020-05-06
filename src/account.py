from .transaction import *

class Account():
    
    def __init__(self):
        self.balance = 0
        self.Transactions = set()
        
    def _deposit(self, amount):
        self.balance += amount
        self.Transactions.add(Transaction(TransactionType.Credit, amount))
        return OperationResult.Success