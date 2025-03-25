class BaseCurrencyException(Exception):
    def __init__(self, message="Error"):
        super().__init__(message)


class CurrencyNotFoundError(BaseCurrencyException):
    def __init__(self, message="Валюта не найдена"):
        super().__init__(message)


class MissingFormField(BaseCurrencyException):
    def __init__(self, message="Отсутствует нужное поле формы"):
        super().__init__(message)


class CurrencyCodeAlreadyExistsError(BaseCurrencyException):
    def __init__(self, message="Валюта с таким кодом уже существует"):
        super().__init__(message)


# class CurrencyPairMissingError(BaseCurrencyException):
#     def __init__(self, message="Код валюты отсутствует в адресе"):
#         super().__init__(message)


class ExchangeRateNotFoundError(BaseCurrencyException):
    def __init__(self, message="Обменный курс для пары не найден"):
        super().__init__(message)


class ExchangeCodeAlreadyExistsError(BaseCurrencyException):
    def __init__(self, message="Валютная пара с таким кодом уже существует"):
        super().__init__(message)


class CurrencyNotFoundException(BaseCurrencyException):
    def __init__(
        self, message="Одна (или обе) валюта из валютной пары не существует в БД"
    ):
        super().__init__(message)


class CurrencyPairMissingException(BaseCurrencyException):
    def __init__(self, message="Валютная пара отсутствует в базе данных"):
        super().__init__(message)


class CurrencyConversionError(BaseCurrencyException):
    def __init__(self, message="Курс обмена для пары валют не найден"):
        super().__init__(message)


class DuplicateCurrencyPairException(BaseCurrencyException):
    def __init__(self, message="Базовая и целевая валюта не могут совпадать"):
        super().__init__(message)


class DatabaseUnavailableException(BaseCurrencyException):
    def __init__(self, message="База данных недоступна"):
        super().__init__(message)
