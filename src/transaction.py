from enum import Enum

class TransactionType(Enum):
    Credit = 1

class OperationResult(Enum):
    Success = 1
    InsufficientFunds = 2

class Transaction():

    def __init__(self, type, amount, datetime):
        self.__type = type
        self.__amount = amount
        self.__dateTime = datetime

    @property
    def Type(self):
        return self.__type

    @property
    def Amount(self):
        return self.__amount

    @property
    def DateTime(self):
        return self.__dateTime

    
        