from typing import Annotated

from fastapi import status, Depends, APIRouter, Query

from src.services.conversion_service import ConversionService

from src.dependencies import convert_service_depends
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
    service: ConversionService = Depends(convert_service_depends),
) -> ExchangeConvertOutSchemas:
    exchange = await service.convert_rate(schema=exchange_amount)
    return exchange
