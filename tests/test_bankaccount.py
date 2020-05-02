from src.bank_account import BankAccount
import unittest

class BankAccountTest(unittest.TestCase):
    def test_deposit(self):
        account = BankAccount()

        self.assertEqual(1, account.deposit())

if __name__ == '__main__':
    unittest.main()