from .transaction import *
import datetime

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
        self.__transactions.add(Transaction(TransactionType.Debit, amount, datetime, DebitType.CashWithdrawal))
        return OperationResult.Success

    def _transfer_domestic(self, amount, datetime):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.__transactions.add(Transaction(TransactionType.Debit, amount, datetime, DebitType.ElectronicTransferDomestic))
        return OperationResult.Success


    def _transfer_abroad(self, amount, datetime):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.__transactions.add(Transaction(TransactionType.Debit, amount, datetime, DebitType.ElectronicTransferAbroad))
        return OperationResult.Success