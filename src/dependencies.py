from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session_maker import (
    SessionDep,
    TransactionSessionDep,
)
from src.services.conversion_service import ConversionService
from src.services.exchange_service import ExchangeService
from src.repository.currency_repository_impl import CurrencyRepositoryImpl
from src.repository.exchange_rate_repository_impl import ExchangeRateRepositoryImpl
from src.services.currency_service import CurrencyService


def get_currency_service(session: AsyncSession = SessionDep):
    instance = CurrencyService(CurrencyRepositoryImpl(session=session))
    return instance


def get_currency_service_with_transaction(
    session: AsyncSession = TransactionSessionDep,
):
    instance = CurrencyService(CurrencyRepositoryImpl(session=session))
    return instance


def get_exchange_service(
    session: AsyncSession = TransactionSessionDep,
):
    instance = ExchangeService(
        CurrencyRepositoryImpl(session=session),
        ExchangeRateRepositoryImpl(session=session),
    )
    return instance


def get_exchange_service_with_transaction(
    session: AsyncSession = TransactionSessionDep,
):
    instance = ExchangeService(
        CurrencyRepositoryImpl(session=session),
        ExchangeRateRepositoryImpl(session=session),
    )
    return instance


def convert_service_depends(
    session: AsyncSession = TransactionSessionDep,
):
    instance = ConversionService(
        ExchangeService(
            CurrencyRepositoryImpl(session=session),
            ExchangeRateRepositoryImpl(session=session),
        )
    )
    return instance
