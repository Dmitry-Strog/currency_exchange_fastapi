from src.services.conversion_service import ConversionService
from src.services.exchange_service import ExchangeService
from src.repository.currency_repository_impl import CurrencyRepositoryImpl
from src.repository.exchange_rate_repository_impl import ExchangeRateRepositoryImpl
from src.services.currency_service import CurrencyService


def currency_service_depends():
    instance = CurrencyService(CurrencyRepositoryImpl())
    return instance


def exchange_service_depends():
    instance = ExchangeService(CurrencyRepositoryImpl(), ExchangeRateRepositoryImpl())
    return instance


def convert_service_depends():
    instance = ConversionService(exchange_service_depends())
    return instance
