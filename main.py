from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI

from src.models.session_maker import SessionDep
from src.repository.currency_repository_impl import CurrencyRepositoryImpl
from src.schemas import CurrencySchemas, CurrencyCodeSchemas


app = FastAPI()


@app.get("/currencies", summary="Получение списка валют")
async def get_all_currency(session: AsyncSession = SessionDep) -> list[CurrencySchemas]:
    currencies = await CurrencyRepositoryImpl.find_all_currency(session)
    return currencies


@app.get("/currency/{code}", summary="Получение конкретной валюты")
async def get_one_currency(
    code: str, session: AsyncSession = SessionDep
) -> CurrencySchemas:
    currency = await CurrencyRepositoryImpl.find_one_or_none(
        session, CurrencyCodeSchemas(code=code)
    )
    print(currency)
    return currency
