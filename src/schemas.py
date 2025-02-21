from pydantic import BaseModel, ConfigDict


class BaseSchemas(BaseModel):
    # from_attributes = True: это позволяет модели автоматически маппить атрибуты Python объектов на поля модели
    model_config = ConfigDict(from_attributes=True)


class CurrencySchemas(BaseSchemas):
    id: int
    code: str
    fullname: str
    sign: str


class CurrencyCodeSchemas(BaseSchemas):
    code: str


class ExchangeRateSchemas(BaseSchemas):
    id: int
    base_currency_id: int
    target_currency_id: int
    rate: int
