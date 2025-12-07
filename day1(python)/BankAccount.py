from AbstractAccount import AbstractAccount
from Errors import InsufficientFundsError, AccountFrozenError, AccountClosedError, InvalidOperationError
import uuid


class BankAccount(AbstractAccount):

    listId = set()
    listStatus = ['активный', 'замороженный', 'закрытый']
    
    def __init__(self, id, info, balance, status, number, currency):
        self.check_unique_id(id)
        self.check_status(status)               # проверяем допустимость статуса
        number = self.check_number(number)      # генерируем если нужно
        currency = self.check_currency(currency)# проверяем валюту
        super().__init__(id, info, balance, status)
        self.number = number
        self.currency = currency

    def check_number(self, number):
        if number == '' or number is None or not str(number).isdigit():
            return uuid.uuid4().hex[:8]         # ✔ генерируем СТРОКУ UUID
        return number
    
    def check_currency(self, currency):
        if currency not in ['RUB', 'USD', 'EUR', 'KZT', 'CNY']:
            raise ValueError("Недопустимая валюта счета.")
        return currency

    def check_unique_id(self, id):
        if id in BankAccount.listId:
            raise ValueError("ID уже используется.")
        BankAccount.listId.add(id)

    def check_status(self, status):
        """Проверка допустимого статуса при создании."""
        if status not in BankAccount.listStatus:
            raise ValueError("Недопустимый статус счета.")
        
    def check_state_status(self):
        """Проверка статуса перед операцией."""
        if self.status in ['замороженный', 'закрытый']:
            raise ValueError("Недопустимый статус счета для выполнения операции.")

    def deposit(self, amount):
        self.check_state_status()      # теперь вызывается правильно
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        self.check_state_status()      # тоже правильно
        self._balance -= amount
        return self._balance
    
    def get_account_info(self):
        return {
            "id": self.id,
            "info": self.info,
            "number": self.number,       # ✔ добавлено (иначе теряется)
            "currency": self.currency,   # ✔ добавлено
            "balance": self._balance,
            "status": self.status
        }
