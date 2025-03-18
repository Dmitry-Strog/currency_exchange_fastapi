from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.exceptions import DatabaseUnavailableException
from src.models.models import ExchangeRateModel, CurrencyModel
from src.repository.interface.exchange_repository import ExchangeRepository
from src.logger_config import logger


class ExchangeRateRepositoryImpl(ExchangeRepository):
    async def find_all(self, session: AsyncSession) -> Sequence[ExchangeRateModel]:
        try:
            stmt = select(self.model)
            result = await session.execute(stmt)
            currency_exchanges = result.scalars().all()
            return currency_exchanges
        except Exception as e:
            logger.error(f"Ошибка при получении всех пар валют: {e}")
            raise DatabaseUnavailableException

    async def find_one_or_none(
        self, session: AsyncSession, filters: BaseModel
    ) -> ExchangeRateModel:
        try:
            BaseCurrency = aliased(CurrencyModel, name="base_currency")
            TargetCurrency = aliased(CurrencyModel, name="target_currency")

            stmt = (
                select(self.model)
                .join(
                    BaseCurrency,
                    self.model.base_currency_id == BaseCurrency.id,
                )
                .join(
                    TargetCurrency,
                    self.model.target_currency_id == TargetCurrency.id,
                )
                .filter(
                    BaseCurrency.code == filters.base_currency,
                    TargetCurrency.code == filters.target_currency,
                )
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            return record
        except Exception as e:
            logger.error(f"Ошибка при получении одной парной валюты: {e}")
            raise DatabaseUnavailableException

    async def create_one(
        self, session: AsyncSession, filters: BaseModel
    ) -> ExchangeRateModel:
        data_exchange = filters.model_dump(exclude_unset=True)
        exchange_model = self.model(**data_exchange)
        session.add(exchange_model)
        try:
            await session.flush()
            await session.refresh(exchange_model)
            return exchange_model
        except IntegrityError:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении парной валюты: {e}")
            raise DatabaseUnavailableException

    async def update(
        self, session: AsyncSession, filters: BaseModel
    ) -> ExchangeRateModel:
        try:
            stmt = (
                select(self.model)
                .where(self.model.base_currency.has(code=filters.base_currency))
                .where(self.model.target_currency.has(code=filters.target_currency))
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            await session.flush()
            return record
        except Exception as e:
            logger.error(f"Ошибка при обновлении парной валюты: {e}")
            raise DatabaseUnavailableException
