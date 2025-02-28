from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import DatabaseUnavailableException
from src.models.models import CurrencyModel
from src.repository.interface.currency_repository import CurrencyRepository
from src.logger_config import logger


class CurrencyRepositoryImpl(CurrencyRepository):
    async def find_all(self, session: AsyncSession) -> Sequence[CurrencyModel]:
        try:
            stmt = select(self.model)
            result = await session.execute(stmt)
            currencies = result.scalars().all()
            return currencies
        except Exception as e:
            logger.error(f"Ошибка при получении валют: {e}")
            raise DatabaseUnavailableException

    async def find_one_or_none(
        self, session: AsyncSession, filters: BaseModel
    ) -> CurrencyModel | None:
        filter_dict = filters.model_dump(exclude_unset=True)
        try:
            stmt = select(self.model).filter_by(**filter_dict)
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            return record
        except Exception as e:
            logger.error(f"Ошибка при получении одной валюты: {e}")
            raise DatabaseUnavailableException

    async def create_one(
        self, session: AsyncSession, filters: BaseModel
    ) -> CurrencyModel:
        data_currency = filters.model_dump(exclude_unset=True)
        currency_model = self.model(**data_currency)
        session.add(currency_model)
        try:
            await session.flush()
            return currency_model
        except InterfaceError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении валюты: {e}")
            raise DatabaseUnavailableException

    async def update(self, session: AsyncSession, filters: BaseModel):
        pass
