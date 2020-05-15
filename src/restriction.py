from abc import ABC, abstractmethod
from .transaction import TransactionType
import datetime

class Restriction(ABC):

    _max_daily_limit = 60
    
    def __init__(self):
        self._next = None

    def set_next(self, next):
        """
        Sets the next restriction in the chain
        """
        self._next = next
        return self._next

    def is_restricted(self, account, amount):

        if not self.handle(account, amount):
            if self._next:
                return self._next.is_restricted(account, amount)
            return False

        return True

    @abstractmethod
    def handle(self, account, amount):
        pass

class DailyLimit(Restriction):

    def __init__(self):
        Restriction.__init__(self)

    def handle(self, account, amount):
        return amount > Restriction._max_daily_limit

class TransactionsToday(Restriction):

    def __init__(self, datetimeprovider = datetime.datetime):
        self.__datetimeprovider = datetimeprovider
        Restriction.__init__(self)

    def handle(self, account, amount):
        amount_already_drawn = 0

        for trn in account.Transactions:
            if trn.Type == TransactionType.Debit and trn.DateTime.date() == self.__datetimeprovider.now().date():
                amount_already_drawn += trn.Amount

        return amount_already_drawn + amount > Restriction._max_daily_limit