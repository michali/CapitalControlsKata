from src.bank import Bank
from src.account import Account
from src.transaction import *

import unittest

class BankTest(unittest.TestCase):
    def test_deposit_to_account_adds_to_balance(self):
        account = Account()
        bank = Bank()

        bank.deposit_to_account(account, 100)

        self.assertEqual(100, account.balance)

    def test_deposit_to_account_creates_transaction(self):
        account = Account()
        bank = Bank()

        operationResult = bank.deposit_to_account(account, 100)

        self.assertEqual(OperationStatus.Success, operationResult.OperationStatus)
        self.assertEqual(TransactionType.Credit, operationResult.Transaction.Type)
        
if __name__ == '__main__':
    unittest.main()