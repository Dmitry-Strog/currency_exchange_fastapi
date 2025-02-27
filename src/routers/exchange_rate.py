from decimal import Decimal
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path, Form, status, Depends, APIRouter

from src.services.exchange_service import ExchangeService

from src.dependencies import exchange_service_depends
from src.models.session_maker import SessionDep, TransactionSessionDep
from src.schemas import (
    ExchangeRateSchemas,
    ExchangeRateAddSchemas,
)


router = APIRouter(tags=["exchange_rates"])


@router.get(
    "/exchange_rates",
    summary="Получение списка всех обменных курсов",
    status_code=status.HTTP_200_OK,
)
async def get_all_exchange_rates(
    session: AsyncSession = SessionDep,
    service: ExchangeService = Depends(exchange_service_depends),
) -> list[ExchangeRateSchemas]:
    exchange_rate = await service.find_all_exchange(session=session)
    return exchange_rate


@router.get(
    "/exchange_rate/{code}",
    summary="Получение конкретного обменного курса",
    status_code=status.HTTP_200_OK,
)
async def get_one_exchange_rates(
    code: Annotated[str, Path(min_length=6, max_length=6, example="USDRUB")],
    session: AsyncSession = SessionDep,
    service: ExchangeService = Depends(exchange_service_depends),
) -> ExchangeRateSchemas:
    currency = await service.find_one_or_none_exchange(
        session=session, currency_code=code
    )
    print(code)
    return currency


@router.post(
    "/exchange_rates",
    summary="Добавление нового обменного курса",
    status_code=status.HTTP_201_CREATED,
)
async def add_exchange_rates(
    code: Annotated[ExchangeRateAddSchemas, Form()],
    session: AsyncSession = TransactionSessionDep,
    service: ExchangeService = Depends(exchange_service_depends),
) -> ExchangeRateSchemas:
    exchange_rate = await service.create_one_exchange(
        session=session, currency_exchange=code
    )
    return exchange_rate


@router.patch(
    "/exchange_rate/{currency_pair}",
    summary="Обновление существующего в базе обменного курса",
    status_code=status.HTTP_200_OK,
)
async def update_exchange_rates(
    currency_pair: Annotated[str, Path(min_length=6, max_length=6, example="USDRUB")],
    rate: Annotated[Decimal, Form(max_digits=9, decimal_places=6, ge=0)],
    session: AsyncSession = TransactionSessionDep,
    service: ExchangeService = Depends(exchange_service_depends),
) -> ExchangeRateSchemas:
    exchange_rate = await service.update_exchange_pair(
        currency_pair=currency_pair, rate=rate, session=session
    )
    return exchange_rate
