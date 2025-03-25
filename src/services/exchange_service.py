from decimal import Decimal

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.exceptions import (
    ExchangeRateNotFoundError,
    ExchangeCodeAlreadyExistsError,
    CurrencyNotFoundException,
    CurrencyPairMissingException,
    DuplicateCurrencyPairException,
)
from src.repository.interface.currency_repository import CurrencyRepository
from src.repository.interface.exchange_repository import ExchangeRepository
from src.schemas import (
    CurrencyCodeSchemas,
    ExchangeRateSchemas,
    InExchangeRateSchemas,
    ExchangeRateAddSchemas,
    ExchangeRateIDAddSchemas,
)
from src.logger_config import logger


class ExchangeService:
    def __init__(
        self, currency_repo: CurrencyRepository, exchange_repo: ExchangeRepository
    ):
        self.currency_repo = currency_repo
        self.exchange_repo = exchange_repo

    async def find_all_exchange(self) -> list[ExchangeRateSchemas]:
        exchange_sequence = await self.exchange_repo.find_all()
        return [
            ExchangeRateSchemas.model_validate(exchange)
            for exchange in exchange_sequence
        ]

    async def find_one_or_none_exchange(
        self, currency_code: str
    ) -> ExchangeRateSchemas:
        base, target = currency_code[:3], currency_code[3:]
        validated_schema = InExchangeRateSchemas(
            base_currency=base, target_currency=target
        )
        exchange_record = await self.exchange_repo.find_one_or_none(
            filters=validated_schema
        )
        logger.info(f"Запрос на пару валют: {exchange_record}")
        if exchange_record is None:
            raise ExchangeRateNotFoundError
        return ExchangeRateSchemas.model_validate(exchange_record)

    async def create_one_exchange(self, currency_exchange: ExchangeRateAddSchemas):
        base_currency = await self.currency_repo.find_one_or_none(
            filters=CurrencyCodeSchemas(code=currency_exchange.base_currency),
        )
        target_currency = await self.currency_repo.find_one_or_none(
            filters=CurrencyCodeSchemas(code=currency_exchange.target_currency),
        )
        if base_currency is None or target_currency is None:
            raise CurrencyNotFoundException
        if base_currency == target_currency:
            raise DuplicateCurrencyPairException

        data = ExchangeRateIDAddSchemas(
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id,
            rate=currency_exchange.rate,
        )
        try:
            exchange_model = await self.exchange_repo.create_one(filters=data)
        except IntegrityError as e:
            logger.error(f"Ошибка при создании валютной пары {e}")
            raise ExchangeCodeAlreadyExistsError

        return ExchangeRateSchemas.model_validate(exchange_model)

    async def update_exchange_pair(
        self, currency_pair: str, rate: Decimal
    ) -> ExchangeRateSchemas:
        base, target = currency_pair[:3], currency_pair[3:]
        validated_schema = ExchangeRateAddSchemas(
            base_currency=base, target_currency=target, rate=rate
        )
        exchange_record = await self.exchange_repo.update(filters=validated_schema)
        try:
            schema = ExchangeRateSchemas.model_validate(exchange_record)
            return schema
        except ValidationError as e:
            raise CurrencyPairMissingException
