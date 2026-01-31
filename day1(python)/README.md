# Банковская система управления счетами

## Описание проекта

Данный проект представляет собой объектно-ориентированную систему управления банковскими счетами на языке Python. Система реализует абстракцию банковского счёта с поддержкой различных статусов, валют и операций пополнения/снятия средств.

Проект демонстрирует использование абстрактных базовых классов (ABC), наследования, обработки исключений и валидации данных в реальном сценарии банковской системы.

## Структура проекта

```
.
├── README.md                 # Документация проекта
├── src/                      # Исходный код проекта
│   ├── AbstractAccount.py    # Абстрактный базовый класс счёта
│   ├── BankAccount.py        # Конкретная реализация банковского счёта
│   └── Errors.py             # Классы исключений
└── test/                     # Тесты и примеры использования
    └── test.py               # Демонстрационный тестовый скрипт
```

## Ключевые функции и возможности

### 1. Абстракция счёта
- **AbstractAccount** — абстрактный базовый класс, определяющий интерфейс для всех типов счетов
- Реализует общие атрибуты: `id`, `info`, `balance`, `status`
- Определяет абстрактные методы, которые должны быть реализованы в наследниках:
  - `deposit(amount)` — пополнение счёта
  - `withdraw(amount)` — снятие средств
  - `get_account_info()` — получение информации о счёте

### 2. Банковский счёт (BankAccount)
Класс [`BankAccount`](src/BankAccount.py:6) реализует полный функционал банковского счёта:

**Основные возможности:**
- ✅ Создание счёта с уникальным идентификатором
- ✅ Автоматическая генерация номера счёта (UUID)
- ✅ Поддержка множества валют: RUB, USD, EUR, KZT, CNY
- ✅ Управление статусами счёта: активный, замороженный, закрытый
- ✅ Операции пополнения и снятия средств
- ✅ Валидация всех входных данных

**Валидация данных:**
- Проверка уникальности ID счёта
- Проверка корректности статуса счёта
- Проверка допустимости валюты
- Проверка суммы операций (должна быть положительным числом)
- Проверка достаточности средств при снятии

### 3. Обработка исключений
Система включает иерархию пользовательских исключений:

| Исключение | Описание |
|------------|----------|
| [`BankError`](src/Errors.py:2) | Базовый класс для всех ошибок банка |
| [`AccountFrozenError`](src/Errors.py:6) | Счёт заморожен, операции недоступны |
| [`AccountClosedError`](src/Errors.py:10) | Счёт закрыт, операции недоступны |
| [`InsufficientFundsError`](src/Errors.py:14) | Недостаточно средств на счёте |
| [`InvalidOperationError`](src/Errors.py:18) | Недопустимая операция (невалидные данные) |

## Технологии и инструменты

- **Python 3.x** — основной язык программирования
- **ABC (Abstract Base Classes)** — для создания абстрактных классов
- **UUID** — для генерации уникальных идентификаторов
- **ООП принципы** — инкапсуляция, наследование, полиморфизм

## Установка зависимостей

### Требования
- Python 3.7 или выше

### Установка
Проект не требует установки внешних зависимостей — все используемые модули входят в стандартную библиотеку Python.

Для проверки версии Python:
```bash
python --version
```

или

```bash
python3 --version
```

## Настройка окружения

### 1. Клонирование или создание проекта
Если проект уже клонирован, перейдите к следующему шагу. В противном случае создайте структуру проекта:

```bash
mkdir bank-account-system
cd bank-account-system
mkdir src test
```

### 2. Размещение файлов
Убедитесь, что файлы находятся в правильных директориях:
- [`src/AbstractAccount.py`](src/AbstractAccount.py)
- [`src/BankAccount.py`](src/BankAccount.py)
- [`src/Errors.py`](src/Errors.py)
- [`test/test.py`](test/test.py)

### 3. Проверка структуры проекта
```bash
tree /F
```

или на Unix-системах:
```bash
ls -R
```

## Запуск проекта

### Запуск тестового скрипта

Для запуска демонстрационного теста выполните:

```bash
python test/test.py
```

или

```bash
python3 test/test.py
```

### Ожидаемый вывод

```
===Создание активного и замороженного счёта===
Тип счета: BankAccount
Клиент: Иван Иванов
Номер: ****[последние 4 цифры]
Статус: активный
Баланс: 1000 RUB

Тип счета: BankAccount
Клиент: Пётр Петров
Номер: ****[последние 4 цифры]
Статус: замороженный
Баланс: 500 RUB

===Попытка операций над замороженным счётом===
Ошибка при пополнении: Ошибка: счет заморожен.
Ошибка при снятии: Ошибка: счет заморожен.

===Валидное пополнение и снятие с активного счёта===
Пополнение прошло успешно. Новый баланс: 1300
Снятие прошло успешно. Новый баланс: 900

===Итоговые состояния счетов===
Тип счета: BankAccount
Клиент: Иван Иванов
Номер: ****[последние 4 цифры]
Статус: активный
Баланс: 900 RUB

Тип счета: BankAccount
Клиент: Пётр Петров
Номер: ****[последние 4 цифры]
Статус: замороженный
Баланс: 500 RUB
```

## Практическое использование

### Создание банковского счёта

```python
from BankAccount import BankAccount

# Создание активного счёта
account = BankAccount(
    id=1,
    info="Иван Иванов",
    balance=1000,
    status="активный",
    number=None,  # Автоматическая генерация UUID
    currency="RUB"
)

print(account)
```

**Параметры конструктора:**
- `id` (int) — уникальный идентификатор счёта
- `info` (str) — информация о владельце счёта
- `balance` (float) — начальный баланс
- `status` (str) — статус счёта: `"активный"`, `"замороженный"`, `"закрытый"`
- `number` (str/int/None) — номер счёта (если None, генерируется автоматически)
- `currency` (str) — валюта счёта: `"RUB"`, `"USD"`, `"EUR"`, `"KZT"`, `"CNY"`

### Пополнение счёта

```python
try:
    new_balance = account.deposit(500)
    print(f"Баланс после пополнения: {new_balance}")
except Exception as e:
    print(f"Ошибка: {e}")
```

### Снятие средств

```python
try:
    new_balance = account.withdraw(300)
    print(f"Баланс после снятия: {new_balance}")
except InsufficientFundsError as e:
    print(f"Недостаточно средств: {e}")
except Exception as e:
    print(f"Ошибка: {e}")
```

### Получение информации о счёте

```python
info = account.get_account_info()
print(info)
# Вывод:
# {
#     'id': 1,
#     'info': 'Иван Иванов',
#     'number': 'a1b2c3d4',
#     'currency': 'RUB',
#     'balance': 1200.0,
#     'status': 'активный'
# }
```

### Обработка ошибок

```python
from Errors import (
    InsufficientFundsError,
    AccountFrozenError,
    AccountClosedError,
    InvalidOperationError
)

try:
    account.withdraw(10000)
except InsufficientFundsError:
    print("Недостаточно средств на счёте")
except AccountFrozenError:
    print("Счёт заморожен, операции недоступны")
except AccountClosedError:
    print("Счёт закрыт, операции недоступны")
except InvalidOperationError as e:
    print(f"Недопустимая операция: {e}")
```

### Работа с замороженными и закрытыми счетами

```python
# Замороженный счёт
frozen_account = BankAccount(
    id=2,
    info="Пётр Петров",
    balance=500,
    status="замороженный",
    number=None,
    currency="USD"
)

# Попытка операции вызовет исключение
try:
    frozen_account.deposit(100)
except AccountFrozenError as e:
    print(e)  # Ошибка: счет заморожен.
```

### Использование разных валют

```python
# Счёт в долларах
usd_account = BankAccount(
    id=3,
    info="John Doe",
    balance=5000,
    status="активный",
    number="12345678",
    currency="USD"
)

# Счёт в евро
eur_account = BankAccount(
    id=4,
    info="Jane Smith",
    balance=3000,
    status="активный",
    number="87654321",
    currency="EUR"
)
```

## Архитектура проекта

### Диаграмма классов

```
┌─────────────────────────┐
│   AbstractAccount (ABC) │
├─────────────────────────┤
│ + id: int               │
│ + info: str             │
│ + _balance: float       │
│ + status: str           │
├─────────────────────────┤
│ + deposit(amount)       │
│ + withdraw(amount)      │
│ + get_account_info()    │
└─────────────────────────┘
            ▲
            │ наследует
            │
┌─────────────────────────┐
│     BankAccount         │
├─────────────────────────┤
│ + number: str           │
│ + currency: str         │
│ - used_ids: set         │
│ - allowed_statuses: set │
│ - allowed_currencies: set│
├─────────────────────────┤
│ + deposit(amount)       │
│ + withdraw(amount)      │
│ + get_account_info()    │
│ + __str__()             │
│ - _validate_unique_id() │
│ - _validate_status()    │
│ - _validate_currency()  │
│ - _validate_amount()    │
│ - _assert_account_active()│
│ - _generate_number_if_needed()│
└─────────────────────────┘
```

### Иерархия исключений

```
Exception
    └── BankError
            ├── AccountFrozenError
            ├── AccountClosedError
            ├── InsufficientFundsError
            └── InvalidOperationError
```

## Примеры использования

### Пример 1: Полный цикл работы со счётом

```python
from BankAccount import BankAccount
from Errors import InsufficientFundsError

# Создание счёта
account = BankAccount(
    id=10,
    info="Алексей Смирнов",
    balance=0,
    status="активный",
    number=None,
    currency="RUB"
)

print("Счёт создан:")
print(account)
print()

# Пополнение
print("Пополнение на 5000 RUB...")
account.deposit(5000)
print(f"Баланс: {account.get_account_info()['balance']} RUB")
print()

# Снятие
print("Снятие 2000 RUB...")
account.withdraw(2000)
print(f"Баланс: {account.get_account_info()['balance']} RUB")
print()

# Попытка снять больше, чем есть
print("Попытка снять 5000 RUB...")
try:
    account.withdraw(5000)
except InsufficientFundsError as e:
    print(f"Ошибка: {e}")
```

### Пример 2: Работа с несколькими счетами

```python
from BankAccount import BankAccount

accounts = []

# Создание нескольких счетов
for i in range(3):
    account = BankAccount(
        id=i+1,
        info=f"Клиент {i+1}",
        balance=1000 * (i+1),
        status="активный",
        number=None,
        currency="RUB"
    )
    accounts.append(account)

# Вывод информации о всех счетах
for acc in accounts:
    print(acc)
    print("-" * 30)
```

### Пример 3: Валидация входных данных

```python
from BankAccount import BankAccount
from Errors import InvalidOperationError

# Попытка создать счёт с недопустимой валютой
try:
    account = BankAccount(
        id=100,
        info="Тест",
        balance=100,
        status="активный",
        number=None,
        currency="JPY"  # Недопустимая валюта
    )
except InvalidOperationError as e:
    print(f"Ошибка создания: {e}")

# Попытка пополнить отрицательной суммой
try:
    account = BankAccount(
        id=101,
        info="Тест",
        balance=100,
        status="активный",
        number=None,
        currency="RUB"
    )
    account.deposit(-50)
except InvalidOperationError as e:
    print(f"Ошибка пополнения: {e}")
```

## Ограничения и особенности

1. **Уникальность ID**: Каждый счёт должен иметь уникальный идентификатор. Повторное использование ID вызовет ошибку.

2. **Статус счёта**: Операции пополнения и снятия доступны только для активных счетов. Замороженные и закрытые счета блокируют все операции.

3. **Валюта**: Поддерживаются только следующие валюты: RUB, USD, EUR, KZT, CNY.

4. **Генерация номера**: Если номер счёта не указан или не является числом, автоматически генерируется UUID (8 символов).

5. **Баланс**: Баланс не может быть отрицательным. Попытка снятия суммы, превышающей баланс, вызовет исключение.

6. **Валидация суммы**: Сумма операций должна быть положительным числом.

## Расширение функционала

### Создание нового типа счёта

```python
from AbstractAccount import AbstractAccount

class SavingsAccount(AbstractAccount):
    """Сберегательный счёт с процентной ставкой"""
    
    def __init__(self, id, info, balance, status, interest_rate):
        super().__init__(id, info, balance, status)
        self.interest_rate = interest_rate
    
    def deposit(self, amount):
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        if amount > self._balance:
            raise Exception("Недостаточно средств")
        self._balance -= amount
        return self._balance
    
    def get_account_info(self):
        return {
            "id": self.id,
            "info": self.info,
            "balance": self._balance,
            "status": self.status,
            "interest_rate": self.interest_rate
        }
    
    def apply_interest(self):
        """Начисление процентов"""
        interest = self._balance * (self.interest_rate / 100)
        self._balance += interest
        return self._balance
```

## Тестирование

Для запуска тестов выполните:

```bash
python test/test.py
```

Тестовый скрипт [`test/test.py`](test/test.py:1) демонстрирует:
- Создание активных и замороженных счетов
- Попытку выполнения операций над замороженным счётом
- Валидные операции пополнения и снятия
- Обработку исключений
