from src.bank import Bank
from src.account import Account
import unittest

class BankTest(unittest.TestCase):
    def test_deposit_to_account(self):
        account = Account()
        bank = Bank()

        bank.deposit_to_account(account, 100)

        self.assertEqual(100, account.balance)

    def test_add_to_balance(self):
        account = Account(100)
        bank = Bank()

        bank.deposit_to_account(account, 100)

        self.assertEqual(200, account.balance)

    def test_withdraw(self):
        account = Account(100)
        bank = Bank()

        bank.withdraw_from_account(account, 100)

        self.assertEqual(0, account.balance)

    def test_withdraw_overdraft_doesnotallow(self):
        account = Account(100)
        bank = Bank()

        bank.withdraw_from_account(account, 200)

        self.assertEqual(100, account.balance)

if __name__ == '__main__':
    unittest.main()