from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    CurrencyNotFoundError,
    CurrencyCodeAlreadyExistsError,
    MissingFormField,
)
from src.repository.interface.currency_repository import CurrencyRepository
from src.schemas import (
    CurrencySchemas,
    CurrencyCodeSchemas,
    InCurrencySchemas,
)
from src.logger_config import logger


class CurrencyService:
    def __init__(self, currency_repo: CurrencyRepository):
        self.currency_repo = currency_repo

    async def find_all_currency(self, session: AsyncSession) -> list[CurrencySchemas]:
        currency_sequence = await self.currency_repo.find_all(session=session)
        return [
            CurrencySchemas.model_validate(currency) for currency in currency_sequence
        ]

    async def find_one_or_none_currency(
        self, currency_code: str, session: AsyncSession
    ) -> CurrencySchemas:
        validated_schema = CurrencyCodeSchemas(code=currency_code)
        currency_record = await self.currency_repo.find_one_or_none(
            session=session, filters=validated_schema
        )
        if currency_record is not None:
            return CurrencySchemas.model_validate(currency_record)
        raise CurrencyNotFoundError

    async def create_one_currency(
        self, currency: InCurrencySchemas, session: AsyncSession
    ) -> CurrencySchemas:
        if not currency.sign or not currency.fullname:
            raise MissingFormField
        try:
            new_currency = await self.currency_repo.create_one(
                session=session, filters=currency
            )
        except IntegrityError as e:
            logger.error(f"Ошибка при создании валюты {e}")
            raise CurrencyCodeAlreadyExistsError
        logger.info(f"Валюта добавлена: {new_currency.fullname} - {new_currency.sign}")
        return CurrencySchemas.model_validate(new_currency)
