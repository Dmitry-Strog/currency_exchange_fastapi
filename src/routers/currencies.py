from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path, Form, status, Depends, APIRouter

from src.dependencies import get_currency_service, get_currency_service_with_transaction
from src.services.currency_service import CurrencyService
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
    service: CurrencyService = Depends(get_currency_service),
) -> list[CurrencySchemas]:
    currencies = await service.find_all_currency()
    return currencies


@router.get(
    "/currency/{code}",
    summary="Получение конкретной валюты",
    status_code=status.HTTP_200_OK,
)
async def get_one_currency(
    code: Annotated[str, Path(min_length=3, max_length=3, examples="RUB")],
    service: CurrencyService = Depends(get_currency_service),
) -> CurrencySchemas:
    currency = await service.find_one_or_none_currency(currency_code=code)
    return currency


@router.post(
    "/currencies",
    summary="Добавление новой валюты",
    status_code=status.HTTP_201_CREATED,
)
async def add_one_currency(
    currency: Annotated[InCurrencySchemas, Form()],
    service: CurrencyService = Depends(get_currency_service_with_transaction),
) -> CurrencySchemas:

    currency = await service.create_one_currency(currency=currency)
    return currency
