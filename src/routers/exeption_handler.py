from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import (
    CurrencyNotFoundError,
    CurrencyCodeAlreadyExistsError,
    ExchangeRateNotFoundError,
    ExchangeCodeAlreadyExistsError,
    CurrencyNotFoundException,
    CurrencyPairMissingException,
    DatabaseUnavailableException,
)


def register_exception_handlers(app: FastAPI):
    """Функция для регистрации обработчиков исключений в FastAPI."""

    @app.exception_handler(CurrencyNotFoundError)
    async def currency_not_found_handler(request: Request, exc: CurrencyNotFoundError):
        return JSONResponse(status_code=404, content={"message": exc.message})

    @app.exception_handler(CurrencyCodeAlreadyExistsError)
    async def currency_code_already(
        request: Request, exc: CurrencyCodeAlreadyExistsError
    ):
        return JSONResponse(status_code=409, content={"message": exc.message})

    @app.exception_handler(ExchangeRateNotFoundError)
    async def exchange_rate_not_found(request: Request, exc: ExchangeRateNotFoundError):
        return JSONResponse(status_code=404, content={"message": exc.message})

    @app.exception_handler(ExchangeCodeAlreadyExistsError)
    async def exchange_code_already_exists(
        request: Request, exc: ExchangeCodeAlreadyExistsError
    ):
        return JSONResponse(status_code=409, content={"message": exc.message})

    @app.exception_handler(CurrencyNotFoundException)
    async def currency_not_found(request: Request, exc: CurrencyNotFoundException):
        return JSONResponse(status_code=404, content={"message": exc.message})

    @app.exception_handler(CurrencyPairMissingException)
    async def currency_pair_missing(
        request: Request, exc: CurrencyPairMissingException
    ):
        return JSONResponse(status_code=404, content={"message": exc.message})

    @app.exception_handler(DatabaseUnavailableException)
    async def database_unavailable_(
        request: Request, exc: DatabaseUnavailableException
    ):
        return JSONResponse(status_code=500, content={"message": exc.message})
