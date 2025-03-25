from abc import ABC, abstractmethod
from typing import TypeVar, Sequence

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository[T](ABC):
    _model: type[T]

    @property
    def model(self) -> type[T]:
        return self._model

    @abstractmethod
    async def find_all(self) -> Sequence[T]:
        pass

    @abstractmethod
    async def find_one_or_none(self, filters: BaseModel) -> T | None:
        pass

    @abstractmethod
    async def create_one(self, filters: BaseModel) -> T:
        pass

    @abstractmethod
    async def update(self, filters: BaseModel) -> T:
        pass

    #
    # @abstractmethod
    # async def delete(self, session: AsyncSession, filters: BaseModel):
    #     pass
