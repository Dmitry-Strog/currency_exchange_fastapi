from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path, Form, status, Depends, APIRouter

from src.dependencies import currency_service_depends
from src.services.currency_service import CurrencyService
from src.models.session_maker import SessionDep, TransactionSessionDep
from src.schemas import (
    CurrencySchemas,
    InCurrencySchemas,
)

router = APIRouter(tags=["currencies"])


@router.get(
    "/currencies",
    summary="Получение списка валют",
    status_code=status.HTTP_200_OK,
)
async def get_all_currency(
    session: AsyncSession = SessionDep,
    service: CurrencyService = Depends(currency_service_depends),
) -> list[CurrencySchemas]:
    currencies = await service.find_all_currency(session=session)
    return currencies


@router.get(
    "/currency/{code}",
    summary="Получение конкретной валюты",
    status_code=status.HTTP_200_OK,
)
async def get_one_currency(
    code: Annotated[str, Path(min_length=3, max_length=3, example="RUB")],
    session: AsyncSession = SessionDep,
    service: CurrencyService = Depends(currency_service_depends),
) -> CurrencySchemas:
    currency = await service.find_one_or_none_currency(
        session=session, currency_code=code
    )
    return currency


@router.post(
    "/currencies",
    summary="Добавление новой валюты",
    status_code=status.HTTP_201_CREATED,
)
async def add_one_currency(
    currency: Annotated[InCurrencySchemas, Form()],
    session: AsyncSession = TransactionSessionDep,
    service: CurrencyService = Depends(currency_service_depends),
) -> CurrencySchemas:

    currency = await service.create_one_currency(session=session, currency=currency)
    return currency
