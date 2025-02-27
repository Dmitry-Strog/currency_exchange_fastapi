from decimal import Decimal

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field


class BaseSchemas(BaseModel):
    # from_attributes = True: это позволяет модели автоматически маппить атрибуты Python объектов на поля модели
    model_config = ConfigDict(from_attributes=True)


class CurrencySchemas(BaseSchemas):
    id: int
    code: str
    fullname: str
    sign: str


class InCurrencySchemas(BaseSchemas):
    code: str = Field(min_length=3, max_length=3)
    fullname: str
    sign: str


class CurrencyCodeSchemas(BaseSchemas):
    code: str = Field(min_length=3, max_length=3)


class ExchangeRateSchemas(BaseSchemas):
    id: int
    base_currency: CurrencySchemas
    target_currency: CurrencySchemas
    rate: Decimal


class InExchangeRateSchemas(BaseSchemas):
    base_currency: str = Field(min_length=3, max_length=3)
    target_currency: str = Field(min_length=3, max_length=3)


class ExchangeRateAddSchemas(BaseSchemas):
    base_currency: str = Field(min_length=3, max_length=3)
    target_currency: str = Field(min_length=3, max_length=3)
    rate: Decimal = Field(max_digits=9, decimal_places=6, ge=0)


class ExchangeRateIDAddSchemas(BaseSchemas):
    base_currency_id: int
    target_currency_id: int
    rate: Decimal = Field(max_digits=9, decimal_places=6, ge=0)


class ExchangeConvertAddSchemas(BaseSchemas):
    base_currency: str = Field(min_length=3, max_length=3)
    target_currency: str = Field(min_length=3, max_length=3)
    amount: Decimal = Field(max_digits=100, decimal_places=6, ge=0)


class ExchangeConvertOutSchemas(BaseSchemas):
    base_currency: CurrencySchemas
    target_currency: CurrencySchemas
    rate: Decimal = Field(max_digits=9, decimal_places=6, ge=0)
    amount: Decimal = Field(max_digits=100, decimal_places=6, ge=0)
    converted_amount: Decimal = Field(max_digits=100, decimal_places=6, ge=0)
