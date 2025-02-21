from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models.config import settings


DATABASE_URL = settings.database_url_asyncpg

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)


fk_int = Annotated[int, mapped_column(ForeignKey("currencies.id", ondelete="CASCADE"))]
