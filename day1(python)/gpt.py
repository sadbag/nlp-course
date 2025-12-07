from abc import ABC, abstractmethod
import uuid


# =========================
#  Классы ошибок
# =========================

class AccountError(Exception):
    """Базовая ошибка для всех ошибок счёта."""


class AccountFrozenError(AccountError):
    """Операция над замороженным счётом."""


class AccountClosedError(AccountError):
    """Операция над закрытым счётом."""


class InvalidOperationError(AccountError):
    """Некорректная операция (сумма, статус, валюта и т.п.)."""


class InsufficientFundsError(AccountError):
    """Недостаточно средств на счёте."""


# =========================
#  Абстрактный класс счёта
# =========================

class AbstractAccount(ABC):
    VALID_STATUSES = {"active", "frozen", "closed"}

    def __init__(self, account_id, owner, balance=0.0,
                 status="active", currency="RUB"):
        self.id = str(account_id)
        self.owner = owner
        self._balance = float(balance)

        if status not in self.VALID_STATUSES:
            raise InvalidOperationError(f"Недопустимый статус счёта: {status}")
        self.status = status

        self.currency = currency

    @abstractmethod
    def deposit(self, amount: float) -> None:
        """Пополнение счёта."""

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        """Снятие средств со счёта."""

    @abstractmethod
    def get_account_info(self) -> dict:
        """Получить информацию о счёте."""

    # ---- общие защищённые методы ----

    def _check_amount(self, amount: float) -> float:
        """Проверка корректности суммы операции."""
        if not isinstance(amount, (int, float)):
            raise InvalidOperationError("Сумма должна быть числом (int или float).")
        if amount <= 0:
            raise InvalidOperationError("Сумма операции должна быть > 0.")
        return float(amount)

    def _check_status_for_operation(self) -> None:
        """Проверка статуса счёта перед операцией."""
        if self.status == "frozen":
            raise AccountFrozenError("Операции по замороженному счёту запрещены.")
        if self.status == "closed":
            raise AccountClosedError("Операции по закрытому счёту запрещены.")

    @property
    def balance(self) -> float:
        """Только чтение баланса."""
        return self._balance


# =========================
#  Конкретный банковский счёт
# =========================

class BankAccount(AbstractAccount):
    ALLOWED_CURRENCIES = {"RUB", "USD", "EUR", "KZT", "CNY"}

    # класс-уровень: множество всех уже использованных id
    _used_ids: set[str] = set()

    def __init__(self, account_id: str | None = None,
                 owner: str | None = None,
                 balance: float = 0.0,
                 status: str = "active",
                 currency: str = "RUB"):

        # 1. Генерация / проверка уникального id
        if account_id is None:
            account_id = self._generate_unique_id()
        else:
            account_id = str(account_id)
            if account_id in BankAccount._used_ids:
                raise InvalidOperationError(
                    f"Счёт с id '{account_id}' уже существует."
                )

        # 2. Проверка валюты
        if currency not in self.ALLOWED_CURRENCIES:
            raise InvalidOperationError(
                f"Валюта {currency!r} не поддерживается. "
                f"Доступны: {', '.join(self.ALLOWED_CURRENCIES)}"
            )

        # 3. Вызов конструктора абстрактного класса
        super().__init__(account_id=account_id,
                         owner=owner,
                         balance=balance,
                         status=status,
                         currency=currency)

        # 4. Регистрируем id как занятый
        BankAccount._used_ids.add(self.id)

    # ---- служебные методы ----

    @classmethod
    def _generate_unique_id(cls) -> str:
        """Сгенерировать короткий уникальный UUID (8 hex-символов)."""
        while True:
            new_id = uuid.uuid4().hex[:8]
            if new_id not in cls._used_ids:
                return new_id

    # ---- реализация абстрактных методов ----

    def deposit(self, amount: float) -> float:
        """Пополнение счёта."""
        amount = self._check_amount(amount)
        self._check_status_for_operation()
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        """Снятие средств со счёта."""
        amount = self._check_amount(amount)
        self._check_status_for_operation()

        if amount > self._balance:
            raise InsufficientFundsError(
                f"Недостаточно средств: нужно {amount}, доступно {self._balance}"
            )

        self._balance -= amount
        return self._balance

    def get_account_info(self) -> dict:
        """Вернуть словарь с данными по счёту."""
        return {
            "id": self.id,
            "owner": self.owner,
            "balance": self._balance,
            "status": self.status,
            "currency": self.currency,
            "type": self.__class__.__name__,
        }

    # ---- строковое представление ----

    def __str__(self) -> str:
        last4 = self.id[-4:]  # "последние 4 цифры" (символа) id
        return (
            f"{self.__class__.__name__} | "
            f"Клиент: {self.owner} | "
            f"№ ***{last4} | "
            f"Статус: {self.status} | "
            f"Баланс: {self._balance:.2f} {self.currency}"
        )


# =========================
#  Демонстрация работы
# =========================

if __name__ == "__main__":
    # ➕ создание активного и замороженного счёта
    active = BankAccount(
        owner="Иван Иванов",
        balance=10_000,
        status="active",
        currency="RUB",
    )

    frozen = BankAccount(
        owner="Пётр Петров",
        balance=5_000,
        status="frozen",
        currency="USD",
    )

    print("Созданные счета:")
    print(active)
    print(frozen)
    print("-" * 60)

    # ✅ валидное пополнение и снятие
    print("Пополнение активного счёта на 1500:")
    active.deposit(1500)
    print(active)

    print("\nСнятие 3000 с активного счёта:")
    active.withdraw(3000)
    print(active)
    print("-" * 60)

    # 🚫 попытка операций над замороженным счётом
    print("Попытка пополнения замороженного счёта:")
    try:
        frozen.deposit(1000)
    except AccountError as e:
        print(f"Ошибка при пополнении: {e}")

    print("\nПопытка снятия с замороженного счёта:")
    try:
        frozen.withdraw(500)
    except AccountError as e:
        print(f"Ошибка при снятии: {e}")
    print("-" * 60)

    # 💸 попытка снять больше, чем есть
    print("Попытка снять больше, чем доступно на активном счёте:")
    try:
        active.withdraw(1_000_000)
    except InsufficientFundsError as e:
        print(f"Ошибка: {e}")

    print("\nФинальное состояние активного счёта:")
    print(active)
