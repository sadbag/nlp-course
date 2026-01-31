from src.Errors import InsufficientFundsError, AccountFrozenError, AccountClosedError, InvalidOperationError
from src.BankAccount import BankAccount


print("===Создание активного и замороженного счёта===")

active = BankAccount(
    id=1,
    info="Иван Иванов",
    balance=1000,
    status="активный",
    number=None,
    currency="RUB"
)

frozen = BankAccount(
    id=2,
    info="Пётр Петров",
    balance=500,
    status="замороженный",
    number=None,
    currency="RUB"
)

print(active)
print()
print(frozen)


print("\n===Попытка операций над замороженным счётом===")

# Пополнение замороженного
try:
    frozen.deposit(200)
except AccountFrozenError as e:
    print("Ошибка при пополнении:", e)

# Снятие замороженного
try:
    frozen.withdraw(100)
except AccountFrozenError as e:
    print("Ошибка при снятии:", e)


print("\n===Валидное пополнение и снятие с активного счёта===")

# Пополнение
try:
    new_balance = active.deposit(300)
    print(f"Пополнение прошло успешно. Новый баланс: {new_balance}")
except Exception as e:
    print("Ошибка при пополнении:", e)

# Снятие
try:
    new_balance = active.withdraw(400)
    print(f"Снятие прошло успешно. Новый баланс: {new_balance}")
except Exception as e:
    print("Ошибка при снятии:", e)


print("\n===Итоговые состояния счетов===")
print(active)
print()
print(frozen)
