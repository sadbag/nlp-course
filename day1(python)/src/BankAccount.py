from .AbstractAccount import AbstractAccount
from .Errors import InsufficientFundsError, AccountFrozenError, AccountClosedError, InvalidOperationError
import uuid


class BankAccount(AbstractAccount):

    used_ids = set()
    allowed_statuses = {'активный', 'замороженный', 'закрытый'}
    allowed_currencies = {'RUB', 'USD', 'EUR', 'KZT', 'CNY'}

    def __init__(self, id, info, balance, status, number, currency):
        self._validate_unique_id(id)
        self._validate_status(status)
        number = self._generate_number_if_needed(number)
        currency = self._validate_currency(currency)

        super().__init__(id, info, balance, status)

        self.number = str(number)
        self.currency = currency

    def _generate_number_if_needed(self, number):
        if not number or not str(number).isdigit():
            return uuid.uuid4().hex[:8]
        return str(number)

    def _validate_currency(self, currency):
        if currency not in self.allowed_currencies:
            raise InvalidOperationError(f"Недопустимая валюта: {currency}")
        return currency

    def _validate_unique_id(self, id):
        if id in BankAccount.used_ids:
            raise InvalidOperationError("ID уже используется.")
        BankAccount.used_ids.add(id)

    def _validate_status(self, status):
        if status not in self.allowed_statuses:
            raise InvalidOperationError("Недопустимый статус счета.")

    def _assert_account_active(self):
        """Проверка статуса перед операцией."""
        if self.status == 'замороженный':
            raise AccountFrozenError()
        if self.status == 'закрытый':
            raise AccountClosedError()

    def _validate_amount(self, amount):
        """Проверка суммы: число и > 0."""
        if not isinstance(amount, (int, float)):
            raise InvalidOperationError("Сумма должна быть числом.")
        if amount <= 0:
            raise InvalidOperationError("Сумма должна быть больше 0.")


    def deposit(self, amount):
        self._assert_account_active()
        self._validate_amount(amount)
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        self._assert_account_active()
        self._validate_amount(amount)

        if amount > self._balance:
            raise InsufficientFundsError()

        self._balance -= amount
        return self._balance

    def get_account_info(self):
        return {
            "id": self.id,
            "info": self.info,
            "number": self.number,
            "currency": self.currency,
            "balance": self._balance,
            "status": self.status
        }

    def __str__(self):
        return (
            f"Тип счета: {self.__class__.__name__}\n"
            f"Клиент: {self.info}\n"
            f"Номер: ****{self.number[-4:]}\n"
            f"Статус: {self.status}\n"
            f"Баланс: {self._balance} {self.currency}"
        )
