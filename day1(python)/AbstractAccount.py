from abc import ABC, abstractmethod


class AbstractAccount(ABC):

    def __init__(self, id, info, balance, status):
        self.id = id
        self.info = info
        self._balance = balance
        self.status = status

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_account_info(self):
        pass
