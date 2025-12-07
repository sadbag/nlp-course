
class BankError(Exception):
    """Базовая ошибка банка."""
    pass

class AccountFrozenError(BankError):
    def __str__(self):
        return "Ошибка: счет заморожен."
    
class AccountClosedError(BankError):
    def __str__(self):
        return "Ошибка: счет закрыт."
    
class InsufficientFundsError(BankError):
    def __str__(self):
        return "Ошибка: недостаточно средств на счете."
    
class InvalidOperationError(BankError):
    def __str__(self):
        return "Ошибка: недопустимая операция."