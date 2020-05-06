from enum import Enum

class TransactionType(Enum):
    Credit = 1

class OperationResult(Enum):
    Success = 1

class Transaction():

    def __init__(self, type, amount, datetime):
        self.Type = type
        self.Amount = amount
        self.DateTime = datetime
        