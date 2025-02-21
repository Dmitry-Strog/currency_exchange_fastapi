from typing import AsyncGenerator, Callable
from contextlib import asynccontextmanager

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.database import async_session_maker


class SessionMakerManager:
    """
    Класс для управления асинхронными сессиями базы данных, включая поддержку транзакций и зависимости FastAPI.
    """

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    @asynccontextmanager
    async def create_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Создаёт и предоставляет новую сессию базы данных.
        Гарантирует закрытие сессии по завершении работы.
        """
        async with self.session_maker() as session:
            try:
                yield session
            except Exception as e:
                print(f"Ошибка при создании сессии базы данных: {e}")
                raise
            finally:
                await session.close()

    @asynccontextmanager
    async def transaction(self, session: AsyncSession) -> AsyncGenerator[None, None]:
        """
        Управление транзакцией: коммит при успехе, откат при ошибке.
        """
        try:
            yield
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка транзакции: {e}")
            raise

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Зависимость для FastAPI, возвращающая сессию без управления транзакцией.
        """
        async with self.create_session() as session:
            yield session

    async def get_transaction_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Зависимость для FastAPI, возвращающая сессию с управлением транзакцией.
        """
        async with self.create_session() as session:
            async with self.transaction(session):
                yield session

    @property
    def session_dependency(self) -> Callable:
        """Возвращает зависимость для FastAPI, обеспечивающую доступ к сессии без транзакции."""
        return Depends(self.get_session)

    @property
    def transaction_session_dependency(self) -> Callable:
        """Возвращает зависимость для FastAPI с поддержкой транзакций."""
        return Depends(self.get_transaction_session)


# Инициализация менеджера сессий базы данных
session_manager = SessionMakerManager(async_session_maker)

# Зависимости FastAPI для использования сессий
SessionDep = session_manager.session_dependency
TransactionSessionDep = session_manager.transaction_session_dependency
