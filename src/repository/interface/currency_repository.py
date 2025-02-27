from abc import ABC

from src.models.models import CurrencyModel
from src.repository.interface.base import BaseRepository


class CurrencyRepository(BaseRepository[CurrencyModel], ABC):
    _model: type[CurrencyModel] = CurrencyModel
