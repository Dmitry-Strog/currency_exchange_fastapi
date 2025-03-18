from decimal import Decimal

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
from schemas import InCurrencySchemas, ExchangeRateAddSchemas
from src.models.config import settings
from src.models.session_maker import session_manager, SessionMakerManager
from src.models.database import Base


engine_test = create_async_engine(settings.database_test_url_asyncpg, echo=False)

async_session_maker_test = async_sessionmaker(engine_test, expire_on_commit=False)

session_manager_test = SessionMakerManager(async_session_maker_test)

data_currency = [
    {"code": "RUB", "fullname": "Russian Ruble", "sign": "₽"},
    {"code": "USD", "fullname": "US Dollar", "sign": "$"},
    {"code": "CNY", "fullname": "Chinese Yuan", "sign": "¥"},
]

data_exchange = [
    {"base_currency": "USD", "target_currency": "RUB", "rate": "87.70"},
    {"base_currency": "USD", "target_currency": "CNY", "rate": "7.28"},
]


@pytest.fixture(scope="function", autouse=True)
def override_dependencies():
    app.dependency_overrides[session_manager.get_session] = (
        session_manager_test.get_session
    )
    app.dependency_overrides[session_manager.get_transaction_session] = (
        session_manager_test.get_transaction_session
    )

    yield

    app.dependency_overrides.clear()


@pytest.fixture(scope="function", autouse=True)
async def setup_database(client):
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    for currency in data_currency:
        await client.post("/currencies", data=currency)

    for exchange in data_exchange:
        await client.post("/exchange_rates", data=exchange)

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as cl:
        yield cl
