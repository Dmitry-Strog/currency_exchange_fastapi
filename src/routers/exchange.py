from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, Depends, APIRouter, Query

from src.services.conversion_service import ConversionService

from src.dependencies import convert_service_depends
from src.models.session_maker import SessionDep
from src.schemas import (
    ExchangeConvertAddSchemas,
    ExchangeConvertOutSchemas,
)


router = APIRouter(tags=["exchange"])


@router.get(
    "/exchange",
    summary="Расчёт перевода определённого количества средств из одной валюты в другую",
    status_code=status.HTTP_200_OK,
)
async def get_all_exchange_rates(
    exchange_amount: Annotated[ExchangeConvertAddSchemas, Query()],
    session: AsyncSession = SessionDep,
    service: ConversionService = Depends(convert_service_depends),
) -> ExchangeConvertOutSchemas:
    exchange = await service.convert_rate(session=session, schema=exchange_amount)
    return exchange
