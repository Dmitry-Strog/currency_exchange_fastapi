from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import CurrencySchemas


class CurrencyRepository(ABC):

    @abstractmethod
    async def find_all_currency(self, session: AsyncSession) -> list[CurrencySchemas]:
        pass

    @abstractmethod
    async def find_one_or_none(self, session: AsyncSession, filters: BaseModel):
        pass
