from src.bank import Bank
from src.account import Account
from src.transaction import *
from unittest.mock import Mock
from parameterized import parameterized, parameterized_class
import unittest
import datetime;

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
        class DateTimeMock(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2020, 1, 1, 15, 45, 0)

        datetimemock = DateTimeMock

        account = Account()
        bank = Bank(datetimemock)
                
        operationResult = bank.deposit_to_account(account, amount)

        self.assertEqual(OperationResult.Success, operationResult)

        transaction = self.__get_first_transaction(account)
        self.assertEqual(TransactionType.Credit, transaction.Type)
        self.assertEqual(amount, transaction.Amount)
        self.assertEqual(datetime.datetime(2020, 1, 1, 15, 45, 0), transaction.DateTime)

    @parameterized.expand([
       (100, 50),
       (200, 100),
       (300, 100),
    ])
    def test_withdraw_removes_from_balance(self, initialbalance, withdrawalamount):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, initialbalance)

        result = bank.withdraw_from_account(account, withdrawalamount)

        self.assertEqual(OperationResult.Success, result)
        self.assertEqual(initialbalance - withdrawalamount, account.Balance)

    @parameterized.expand([
       (200,),
       (400,),
       (600,),
    ])
    def test_withdraw_overdraft_results_in_error(self, withdrawalamount):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, 100)

        result = bank.withdraw_from_account(account, withdrawalamount)

        self.assertEqual(OperationResult.InsufficientFunds, result)
        self.assertEqual(account.Balance, 100)
    
    @parameterized.expand([
       (100,),
       (50,),
       (30,),
    ])
    def test_withdraw_creates_transaction(self, withdrawal_amount):
        class DateTimeMock(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2020, 1, 1, 15, 45, 0)        
        datetimemock = DateTimeMock

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

    def test_eletronic_transfer_domestic_creates_transactions(self):
        account_from = Account()
        account_to = Account()

        class DateTimeMock(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2020, 1, 1, 15, 45, 0)   

        datetimemock = DateTimeMock
        bank = Bank(datetimemock)

        bank.deposit_to_account(account_from, 100)
        bank.deposit_to_account(account_to, 50)

        bank.transfer(account_from, account_to, 50)

        transaction = self.__get_transaction(account_from, lambda t: t.Type == TransactionType.Debit)
        self.assertNotEqual(None, transaction)
        self.assertEqual(50, transaction.Amount)
        self.assertEqual(datetime.datetime(2020, 1, 1, 15, 45, 0), transaction.DateTime)
        self.assertEqual(DebitType.ElectronicTransferDomestic, transaction.DebitType)

    @parameterized.expand([
       (100, 50),
       (200, 100),
       (300, 100),
    ])
    def test_transfer_abroad_removes_from_balance(self, initialbalance, withdrawalamount):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, initialbalance)

        result = bank.transfer_abroad(account, withdrawalamount)

        self.assertEqual(OperationResult.Success, result)
        self.assertEqual(initialbalance - withdrawalamount, account.Balance)

    @parameterized.expand([
       (200,),
       (400,),
       (600,),
    ])
    def test__transfer_abroad_insufficient_sender_funds(self, withdrawalamount):
        account = Account()
        bank = Bank()
        bank.deposit_to_account(account, 100)

        result = bank.transfer_abroad(account, withdrawalamount)

        self.assertEqual(OperationResult.InsufficientFunds, result)
        self.assertEqual(account.Balance, 100)
    
    @parameterized.expand([
       (100,),
       (50,),
       (30,),
    ])
    def test__transfer_abroad_creates_transaction(self, withdrawal_amount):
        class DateTimeMock(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2020, 1, 1, 15, 45, 0)        
        datetimemock = DateTimeMock

        account = Account()
        bank = Bank(datetimemock)
        bank.deposit_to_account(account, 100)

        bank.transfer_abroad(account, withdrawal_amount)
        transaction = self.__get_transaction(account, lambda t: t.Type == TransactionType.Debit)
        self.assertNotEqual(None, transaction)
        self.assertEqual(withdrawal_amount, transaction.Amount)
        self.assertEqual(datetime.datetime(2020, 1, 1, 15, 45, 0), transaction.DateTime)
        self.assertEqual(DebitType.ElectronicTransferAbroad, transaction.DebitType)

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