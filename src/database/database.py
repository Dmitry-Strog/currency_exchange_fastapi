from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database.config import settings


DATABASE_URL = settings.database_url_asyncpg

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
