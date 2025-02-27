from abc import ABC

from src.models.models import ExchangeRateModel
from src.repository.interface.base import BaseRepository


class ExchangeRepository(BaseRepository[ExchangeRateModel], ABC):
    _model: type[ExchangeRateModel] = ExchangeRateModel
