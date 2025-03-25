from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ExchangeRateNotFoundError, CurrencyConversionError
from src.services.exchange_service import ExchangeService
from src.schemas import ExchangeConvertAddSchemas, ExchangeConvertOutSchemas
from src.logger_config import logger


class ConversionService:
    def __init__(self, exchange_service: ExchangeService):
        self.exchange_service = exchange_service

    async def convert_rate(self, schema: ExchangeConvertAddSchemas):
        try:
            return await self._get_direct_rate(schema=schema)
        except ExchangeRateNotFoundError:
            try:
                return await self._get_reverse_rate(schema=schema)
            except ExchangeRateNotFoundError:
                try:
                    return await self._calculate_cross_rate(schema=schema)
                except ExchangeRateNotFoundError:
                    logger.error(f"Конвертация не выполнена {schema}")
                    raise CurrencyConversionError

    async def _get_direct_rate(self, schema: ExchangeConvertAddSchemas):
        exchange_rate = await self.exchange_service.find_one_or_none_exchange(
            currency_code=schema.base_currency + schema.target_currency
        )
        converted_amount = round(schema.amount * exchange_rate.rate, 2)
        return ExchangeConvertOutSchemas(
            base_currency=exchange_rate.base_currency,
            target_currency=exchange_rate.target_currency,
            rate=exchange_rate.rate,
            amount=schema.amount,
            converted_amount=converted_amount,
        )

    async def _get_reverse_rate(self, schema: ExchangeConvertAddSchemas):
        exchange_rate = await self.exchange_service.find_one_or_none_exchange(
            currency_code=schema.target_currency + schema.base_currency
        )
        converted_amount = round(schema.amount * (1 / exchange_rate.rate), 2)
        return ExchangeConvertOutSchemas(
            base_currency=exchange_rate.base_currency,
            target_currency=exchange_rate.target_currency,
            rate=exchange_rate.rate,
            amount=schema.amount,
            converted_amount=converted_amount,
        )

    async def _calculate_cross_rate(self, schema: ExchangeConvertAddSchemas):
        exchange_usd_a = await self.exchange_service.find_one_or_none_exchange(
            currency_code="USD" + schema.base_currency
        )
        logger.debug(f"Найден курс для пары 'USD'/ {schema.base_currency}")

        exchange_usd_b = await self.exchange_service.find_one_or_none_exchange(
            currency_code="USD" + schema.target_currency
        )
        logger.debug(f"Найден курс для пары 'USD'/ {schema.target_currency}")

        rate = exchange_usd_b.rate / exchange_usd_a.rate
        converted_amount = round(rate * schema.amount, 2)

        return ExchangeConvertOutSchemas(
            base_currency=exchange_usd_a.target_currency,
            target_currency=exchange_usd_b.target_currency,
            rate=round(rate, 2),
            amount=schema.amount,
            converted_amount=converted_amount,
        )
