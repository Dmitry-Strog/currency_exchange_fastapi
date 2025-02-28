class BaseCurrencyException(Exception):
    def __init__(self):
        self.message = "Error"


class CurrencyNotFoundError(BaseCurrencyException):
    def __init__(self):
        self.message = f"Валюта не найдена"


class MissingFormField(BaseCurrencyException):
    def __init__(self):
        self.message = f"Отсутствует нужное поле формы"


class CurrencyCodeAlreadyExistsError(BaseCurrencyException):
    def __init__(self):
        self.message = f"Валюта с таким кодом уже существует"


# class CurrencyPairMissingError(BaseCurrencyException):
#     def __init__(self):
#         self.message = f"Код валюты отсутствует в адресе"


class ExchangeRateNotFoundError(BaseCurrencyException):
    def __init__(self):
        self.message = f"Обменный курс для пары не найден"


class ExchangeCodeAlreadyExistsError(BaseCurrencyException):
    def __init__(self):
        self.message = f"Валютная пара с таким кодом уже существует"


class CurrencyNotFoundException(BaseCurrencyException):
    def __init__(self):
        self.message = f"Одна (или обе) валюта из валютной пары не существует в БД"


class CurrencyPairMissingException(BaseCurrencyException):
    def __init__(self):
        self.message = f"Валютная пара отсутствует в базе данных"


class CurrencyConversionError(BaseCurrencyException):
    def __init__(self):
        self.message = f"Курс обмена для пары валют не найден"


class DuplicateCurrencyPairException(BaseCurrencyException):
    def __init__(self):
        self.message = f"Базовая и целевая валюта не могут совпадать"


class DatabaseUnavailableException(BaseCurrencyException):
    def __init__(self):
        self.message = f"База данных недоступна"
