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