from .transaction import *
from .operationResult import *

class Account():
    
    def __init__(self):
        self.balance = 0
        
    def _deposit(self, amount):
        self.balance += amount
        return OperationResult(Transaction(TransactionType.Credit, amount), OperationStatus.Success)