from datetime import datetime, timedelta
from .transaction import OperationResult, TransactionType

class Bank():

    __max_daily_limit = 60
    __max_weekly_bank_transfer_abroad_limit = 500
    __start_date_for_fresh_transactions = datetime(2020, 5, 18, 12, 0, 0)

    def __init__(self, datetimeprovider = datetime):
        self.__datetimeprovider = datetimeprovider

    def deposit_to_account(self, account, amount):
        return account._deposit(amount, self.__datetimeprovider.now())

    def withdraw_from_account(self, account, amount):       
        if not self.__can_withdraw(account, amount):  
            return OperationResult.NotAllowed            
            
        return account._withdraw(amount, self.__datetimeprovider.now())
    
    def transfer(self, account_from, account_to, amount):
        date = self.__datetimeprovider.now()
        withdrawal = account_from._transfer_domestic(amount, date)

        if (withdrawal == OperationResult.InsufficientFunds):
            return withdrawal

        return account_to._deposit(amount, date)

    def transfer_abroad(self, account, amount):
        if self.__can_transfer_abroad(account, amount):  
            return account._transfer_abroad(amount, self.__datetimeprovider.now())

        return OperationResult.NotAllowed

    def __can_withdraw(self, account, amount): 
        now = self.__datetimeprovider.now()
        day_of_week_index = now.weekday()     
        money_withdrawn_this_week = account._get_withdrawn_amount_this_week_so_far_for_date(now)
        
        return money_withdrawn_this_week + amount <= Bank.__max_daily_limit * (day_of_week_index + 1)        

    def __can_transfer_abroad(self, account, amount): 
        now = self.__datetimeprovider.now() 
        
        money_transfered_abroad_this_week = account._get_amount_transfered_abroad_this_week_so_far_for_date(now)

        return money_transfered_abroad_this_week + amount <= Bank.__max_weekly_bank_transfer_abroad_limit           