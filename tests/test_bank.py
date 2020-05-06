from src.bank import Bank
from src.account import Account
from src.transaction import *
from parameterized import parameterized, parameterized_class

import unittest

class BankTest(unittest.TestCase):
    def test_deposit_to_account_adds_to_balance(self):
        account = Account()
        bank = Bank()

        bank.deposit_to_account(account, 100)

        self.assertEqual(100, account.balance)

    @parameterized.expand([
       (100,),
       (200,),
       (300,),
    ])
    def test_deposit_to_account_creates_transaction(self, amount):
        account = Account()
        bank = Bank()

        operationResult = bank.deposit_to_account(account, amount)

        self.assertEqual(OperationStatus.Success, operationResult.OperationStatus)
        self.assertEqual(TransactionType.Credit, operationResult.Transaction.Type)
        self.assertEqual(amount, operationResult.Transaction.Amount)        
    
if __name__ == '__main__':
    unittest.main()