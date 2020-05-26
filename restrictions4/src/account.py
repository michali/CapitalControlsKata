from .transaction import *
from datetime import datetime, timedelta

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
        return self.__debit(amount, datetime, DebitType.CashWithdrawal)

    def _transfer_domestic(self, amount, datetime):
        return self.__debit(amount, datetime, DebitType.ElectronicTransferDomestic)
   
    def _transfer_abroad(self, amount, datetime):
        return self.__debit(amount, datetime, DebitType.ElectronicTransferAbroad)

    def __debit(self, amount, datetime, debit_type):
        if (self.__balance < amount):
            return OperationResult.InsufficientFunds

        self.__balance -= amount
        self.__transactions.add(Transaction(TransactionType.Debit, amount, datetime, debit_type))
        return OperationResult.Success
        
    def _get_withdrawn_amount_this_week_so_far_for_date(self, date):
        return self._get_debited_amount_this_week_so_far_for_date(date, DebitType.CashWithdrawal)

    def _get_amount_transfered_abroad_this_week_so_far_for_date(self, date):
        return self._get_debited_amount_this_week_so_far_for_date(date, DebitType.ElectronicTransferAbroad)

    def _get_debited_amount_this_week_so_far_for_date(self, date, debit_type):
        day_of_week_index = date.weekday()
        money_withdrawn = 0
        for i in range(0, day_of_week_index + 1):
            money_withdrawn += self.__get_debited_amount_on_date(date - timedelta(days = i), debit_type)

        return money_withdrawn    

    def __get_debited_amount_on_date(self, date, debit_type):     
        amount = 0   
        for trn in self.Transactions:
            if trn.Type == TransactionType.Debit \
                and trn.DebitType == debit_type \
                and trn.DateTime.date() == date.date():
                amount += trn.Amount
        
        return amount

    def _get_total_amount_for_credits_on_and_after_date(self, date):
        total_deposits_after_cutoff_date = 0
        for trn in self.Transactions:
            if trn.Type == TransactionType.Credit and trn.DateTime.date() >= date.date():
                total_deposits_after_cutoff_date += trn.Amount        

        return total_deposits_after_cutoff_date
