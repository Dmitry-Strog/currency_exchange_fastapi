from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.exeption_handler import register_exception_handlers
from src.routers import currencies, exchange_rate


app = FastAPI()


app.include_router(currencies.router)
app.include_router(exchange_rate.router)

register_exception_handlers(app)
