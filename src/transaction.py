from enum import Enum

class TransactionType(Enum):
    Credit = 1

class OperationStatus(Enum):
    Success = 1

class Transaction():

    def __init__(self, type, amount):
        self.Type = type
        self.Amount = amount
        