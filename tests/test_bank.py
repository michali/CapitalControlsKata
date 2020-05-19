from src.bank import Bank
from src.account import Account
from src.transaction import *
from unittest.mock import Mock
from parameterized import parameterized, parameterized_class
import unittest
import datetime

class BankTest(unittest.TestCase):
    def test_deposit_to_account_updates_balance(self):
        account = Account()
        bank = Bank()

        bank.deposit_to_account(account, 100)

        self.assertEqual(100, account.Balance)

    def test_deposit_to_account_add_balances(self):
        account = Account()
        bank = Bank()

        operationResult = bank.deposit_to_account(account, 100)
        operationResult = bank.deposit_to_account(account, 50)

        self.assertEqual(OperationResult.Success, operationResult)

        self.assertEqual(150, account.Balance)

    @parameterized.expand([
       (100,),
       (200,),
       (300,),
    ])
    def test_deposit_to_account_creates_transaction(self, amount):
        datetimemock = Mock()
        datetimemock.now.return_value = datetime.datetime(2020, 1, 1, 15, 45, 0)
        account = Account()
        bank = Bank(datetimemock)
                
        operationResult = bank.deposit_to_account(account, amount)

        self.assertEqual(OperationResult.Success, operationResult)

        transaction = self.__get_first_transaction(account)
        self.assertEqual(TransactionType.Credit, transaction.Type)
        self.assertEqual(amount, transaction.Amount)
        self.assertEqual(datetime.datetime(2020, 1, 1, 15, 45, 0), transaction.DateTime)

    @parameterized.expand([
       (10, 5),
       (20, 10),
       (30, 10),
    ])
    def test_withdraw_removes_from_balance(self, initialbalance, withdrawalamount):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, initialbalance)

        result = bank.withdraw_from_account(account, withdrawalamount)

        self.assertEqual(OperationResult.Success, result)
        self.assertEqual(initialbalance - withdrawalamount, account.Balance)

    @parameterized.expand([
       (20,),
       (40,),
       (60,),
    ])
    def test_withdraw_overdraft_results_in_error(self, withdrawalamount):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, 10)

        result = bank.withdraw_from_account(account, withdrawalamount)

        self.assertEqual(OperationResult.InsufficientFunds, result)
        self.assertEqual(account.Balance, 10)
    
    @parameterized.expand([
       (50,),
       (40,),
       (30,),
    ])
    def test_withdraw_creates_transaction(self, withdrawal_amount):
        datetimemock = Mock()
        datetimemock.now.return_value = datetime.datetime(2020, 1, 1, 15, 45, 0)

        account = Account()
        bank = Bank(datetimemock)
        bank.deposit_to_account(account, 100)

        bank.withdraw_from_account(account, withdrawal_amount)
        transaction = self.__get_transaction(account, lambda t: t.Type == TransactionType.Debit)
        self.assertNotEqual(None, transaction)
        self.assertEqual(withdrawal_amount, transaction.Amount)
        self.assertEqual(datetime.datetime(2020, 1, 1, 15, 45, 0), transaction.DateTime)
        self.assertEqual(DebitType.CashWithdrawal, transaction.DebitType)

    def test_eletronic_transfer(self):
        account_from = Account()
        account_to = Account()
        bank = Bank()

        bank.deposit_to_account(account_from, 100)
        bank.deposit_to_account(account_to, 50)

        result = bank.transfer(account_from, account_to, 50)

        self.assertEqual(50, account_from.Balance)
        self.assertEqual(100, account_to.Balance)
        self.assertEqual(OperationResult.Success, result)

    @parameterized.expand([
       (101,),
       (102,),
       (104,),
    ])
    def test_eletronic_transfer_insufficient_sender_funds(self, transfer_amount):
        account_from = Account()
        account_to = Account()
        bank = Bank()

        bank.deposit_to_account(account_from, 100)
        bank.deposit_to_account(account_to, 50)

        result = bank.transfer(account_from, account_to, transfer_amount)

        self.assertEqual(100, account_from.Balance)
        self.assertEqual(50, account_to.Balance)
        self.assertEqual(OperationResult.InsufficientFunds, result)    
    
    def test_withdrawal_over_daily_amount_in_multiple_transactions_across_two_days_is_allowed(self):
        datetimemock = Mock()
        datetimemock.now.return_value = datetime.datetime(2020, 1, 1, 15, 45, 0)

        account = Account()
        bank = Bank(datetimemock)
        bank.deposit_to_account(account, 100)

        bank.withdraw_from_account(account, 60)

        datetimemock.now.return_value = datetime.datetime(2020, 1, 2, 15, 46, 0)
        result = bank.withdraw_from_account(account, 10)

        self.assertEqual(OperationResult.Success, result)
        self.assertEqual(30, account.Balance)

    @parameterized.expand([
       (11, 60, 16, 250, OperationResult.Success), #first day: Monday, second day: Saturday
       (12, 60, 17, 360, OperationResult.Success), #first day: Tuesday, second day: Sunday
       (14, 60, 17, 361, OperationResult.NotAllowed), #first day: Thursday, second day: Sunday
       (11, 60, 12, 61, OperationResult.NotAllowed), #first day: Monday, second day: Tuesday
       (16, 60, 20, 181, OperationResult.NotAllowed), #first day: Saturday, second day: Wednesday next week
       (11, 60, 12, 61, OperationResult.NotAllowed), #first day: Monday, second day: Saturday
    ])
    def test_withdrawal_if_less_than_the_limit_was_drawn_throughout_the_week_allow_withdrawal_up_to_today(self, day_of_month_first_trn, first_withdrawal_amount, day_of_month_second_trn, second_withdrawal_amount, second_trn_operation_result):
        account = Account()
        datetimemock = Mock()
        bank = Bank(datetimemock)
        datetimemock.now.return_value = datetime.datetime(2020, 5, 10, 12, 0, 0) 
        bank.deposit_to_account(account, 2000)

        datetimemock.now.return_value = datetime.datetime(2020, 5, day_of_month_first_trn, 12, 0, 0)  
        bank.withdraw_from_account(account, first_withdrawal_amount)

        datetimemock.now.return_value = datetime.datetime(2020, 5, day_of_month_second_trn, 12, 0, 0) 
        result = bank.withdraw_from_account(account, second_withdrawal_amount)

        self.assertEqual(second_trn_operation_result, result)

    @parameterized.expand([
       (489, OperationResult.Success),
       (499, OperationResult.Success),
       (500, OperationResult.Success),
       (500.50, OperationResult.NotAllowed),
       (501, OperationResult.NotAllowed),
       (502, OperationResult.NotAllowed)
    ])
    def test_transfer_abroad_up_to_weekly_limit(self, amount, operation_result):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, 1000)

        result = bank.transfer_abroad(account, amount)

        self.assertEqual(operation_result, result)

    @parameterized.expand([
       (11, 250, 16, 250, OperationResult.Success), # same week
       (12, 400, 17, 99, OperationResult.Success), # same week
       (14, 100, 17, 401, OperationResult.NotAllowed), # same week
       (16, 400, 20, 500, OperationResult.Success), # second transaction occurs next week
    ])
    def test_transfer_abroad_up_to_weekly_limit_two_transactions(self, day_of_month_first_trn, first_withdrawal_amount, day_of_month_second_trn, second_withdrawal_amount, second_trn_operation_result):
        datetimemock = Mock()        
        account = Account()        
        bank = Bank(datetimemock)     
        datetimemock.now.return_value = datetime.datetime(2020, 5, 15, 12, 0, 0)
        bank.deposit_to_account(account, 2000)     

        datetimemock.now.return_value = datetime.datetime(2020, 5, day_of_month_first_trn, 12, 0, 0)  
        bank.transfer_abroad(account, first_withdrawal_amount)

        datetimemock.now.return_value = datetime.datetime(2020, 5, day_of_month_second_trn, 12, 0, 0) 
        result = bank.transfer_abroad(account, second_withdrawal_amount)

        self.assertEqual(second_trn_operation_result, result)

    def test_withdraw_to_limit_and_transfer_abroad_to_limit_in_same_week(self):
        datetimemock = Mock()        
        account = Account()        
        bank = Bank(datetimemock)       
        bank.deposit_to_account(account, 2000)  
        datetimemock.now.return_value = datetime.datetime(2020, 5, 17, 12, 0, 0) # End of week, can withdraw to maximum withdrawal limit
   
        result_withdraw = bank.withdraw_from_account(account, 420)
        result_transfer_abroad = bank.transfer_abroad(account, 500)

        self.assertEqual(OperationResult.Success, result_withdraw)        
        self.assertEqual(OperationResult.Success, result_transfer_abroad)

    def test_transfer_abroad_to_limit_and_withdraw_to_limit_and_in_same_week(self):
        datetimemock = Mock()        
        account = Account()        
        bank = Bank(datetimemock)        
        bank.deposit_to_account(account, 2000)   
        datetimemock.now.return_value = datetime.datetime(2020, 5, 17, 12, 0, 0) # End of week, can withdraw to maximum withdrawal limit
         
        result_transfer_abroad = bank.transfer_abroad(account, 500) 
        result_withdraw = bank.withdraw_from_account(account, 420)

        self.assertEqual(OperationResult.Success, result_transfer_abroad)
        self.assertEqual(OperationResult.Success, result_withdraw)

    @parameterized.expand([
       (200, 200, 0, OperationResult.Success),
       (200, 100, 100, OperationResult.Success)
    ])
    def test_deposits_after_20200518_are_exempt_from_withdrawal_restrictions(self, deposit_amount, withdrawal_amount, balance, operation_result):
        datetimemock = Mock()        
        account = Account() 
        bank = Bank(datetimemock)      
        datetimemock.now.return_value = datetime.datetime(2020, 5, 18, 12, 0, 0) ## Monday
        bank.deposit_to_account(account, deposit_amount)
        result_withdraw = bank.withdraw_from_account(account, withdrawal_amount)

        self.assertEqual(operation_result, result_withdraw)
        self.assertEqual(balance, account.Balance) 

    @parameterized.expand([
       (18, 260, OperationResult.Success), # Monday, Day restrictions are eased for new deposits
       (19, 320, OperationResult.Success),
       (19, 321, OperationResult.NotAllowed)
    ])
    def test_can_withdraw_daily_amount_with_rollover_plus_deposits_after_20200518(self, day_of_month_to_withdraw, withdrawal_amount, withdrawal_result):
        datetimemock = Mock()        
        account = Account() 
        bank = Bank(datetimemock)  
        datetimemock.now.return_value = datetime.datetime(2020, 5, 17, 12, 0, 0) # Day before restrictions are eased for new deposits
        bank.deposit_to_account(account, 120)

        datetimemock.now.return_value = datetime.datetime(2020, 5, day_of_month_to_withdraw, 12, 0, 0) 
        bank.deposit_to_account(account, 200)
        result = bank.withdraw_from_account(account, withdrawal_amount)

        self.assertEqual(withdrawal_result, result)

        if withdrawal_result==OperationResult.Success:
            self.assertEqual(320 - withdrawal_amount, account.Balance)
        else:
            self.assertEqual(320, account.Balance)

    @parameterized.expand([
       (500, 500, OperationResult.Success),
       (500, 499, OperationResult.Success),
       (500, 1001, OperationResult.NotAllowed)
    ])
    def test_can_transfer_abroad_above_weekly_limit_with_deposits_after_20200518(self, after_restrictions_deposit_amount, withdrawal_amount, withdrawal_operation_result):
        datetimemock = Mock()        
        account = Account() 
        bank = Bank(datetimemock)      
        datetimemock.now.return_value = datetime.datetime(2020, 5, 17, 12, 0, 0) # Day before restrictions are eased for new deposits
        bank.deposit_to_account(account, 1000)

        datetimemock.now.return_value = datetime.datetime(2020, 5, 19, 12, 0, 0) 
        bank.deposit_to_account(account, after_restrictions_deposit_amount)
        result = bank.transfer_abroad(account, withdrawal_amount)

        self.assertEqual(withdrawal_operation_result, result)

        if withdrawal_operation_result == OperationResult.Success:
            self.assertEqual(1000 + after_restrictions_deposit_amount - withdrawal_amount, account.Balance)
        else:
            self.assertEqual(1000 + after_restrictions_deposit_amount, account.Balance)
    

    # def test_new_deposits intertwine with withdrawals and transfer abroad
    # intertwine with withdrawals and transfers abroad
    

    def __get_transaction(self, account, condition):
        for transaction in account.Transactions:
            if (condition(transaction)):
                return transaction
        return None

    def __get_first_transaction(self, account):
        for transaction in account.Transactions:
            break
        return transaction
        
if __name__ == '__main__':
    unittest.main()