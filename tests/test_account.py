from src.bank import Bank
from src.account import BankAccount
import unittest

class BankTest(unittest.TestCase):
    def test_deposit_to_account(self):
        account = BankAccount()
        bank = Bank()

        bank.deposit_to_account(account, 100)

        self.assertEqual(100, account.balance)

if __name__ == '__main__':
    unittest.main()