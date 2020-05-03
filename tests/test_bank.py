from src.bank import Bank
from src.account import Account
from src.account_result import AccountResult
import unittest

class BankTest(unittest.TestCase):
    def test_deposit_to_account(self):
        account = Account()
        bank = Bank()

        result = bank.deposit_to_account(account, 100)

        self.assertEqual(100, account.balance)
        self.assertEqual(AccountResult.Success, result)

    def test_add_to_balance(self):
        account = Account(100)
        bank = Bank()

        result = bank.deposit_to_account(account, 100)

        self.assertEqual(200, account.balance)
        self.assertEqual(AccountResult.Success, result)

    def test_withdraw(self):
        account = Account(100)
        bank = Bank()

        result = bank.withdraw_from_account(account, 100)

        self.assertEqual(0, account.balance)
        self.assertEqual(AccountResult.Success, result)

    def test_withdraw_overdraft_doesnotallow(self):
        account = Account(100)
        bank = Bank()

        result = bank.withdraw_from_account(account, 200)

        self.assertEqual(100, account.balance)
        self.assertEqual(AccountResult.InsufficientFunds, result)

    def test_eletronic_transfer(self):
        account_from = Account(100)
        account_to = Account(100)
        bank = Bank()

        result = bank.transfer(account_from, account_to, 50)

        self.assertEqual(50, account_from.balance)
        self.assertEqual(150, account_to.balance)
        self.assertEqual(AccountResult.Success, result)

    def test_transfer_overdraft_doesnotallow(self):
        account_from = Account(100)
        account_to = Account(100)
        bank = Bank()

        result = bank.transfer(account_from, account_to, 101)

        self.assertEqual(AccountResult.InsufficientFunds, result)
        self.assertEqual(100, account_from.balance)
        self.assertEqual(100, account_to.balance)


if __name__ == '__main__':
    unittest.main()