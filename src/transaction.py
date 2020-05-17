from enum import Enum
from .operationresult import *

class TransactionType(Enum):
    Credit = 1
    Debit = 2

class DebitType(Enum):
    CashWithdrawal = 1,
    DomesticElectronicTransfer = 2

class Transaction():

    def __init__(self, type, amount, datetime, debitType = None):
        self.__type = type
        self.__amount = amount
        self.__dateTime = datetime
        self.__debitType = debitType

    @property
    def Type(self):
        return self.__type

    @property
    def Amount(self):
        return self.__amount

    @property
    def DateTime(self):
        return self.__dateTime

    @property
    def DebitType(self):
        return self.__debitType

    
        