from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.interface.currency_repository import CurrencyRepository
from src.models.models import CurrencyModel
from src.schemas import CurrencySchemas


class CurrencyRepositoryImpl(CurrencyRepository):
    @classmethod
    async def find_all_currency(cls, session: AsyncSession) -> list[CurrencySchemas]:
        # CurrencyModel вывести в зависимость
        query = select(CurrencyModel)
        result = await session.execute(query)
        currencies = result.scalars().all()

        return [CurrencySchemas.model_validate(currency) for currency in currencies]

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        # Найти одну запись по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True)
        try:
            # CurrencyModel вывести в зависимость
            query = select(CurrencyModel).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise
