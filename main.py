from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.exeption_handler import register_exception_handlers
from src.routers import currencies, exchange_rate, exchange


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(currencies.router)
app.include_router(exchange_rate.router)
app.include_router(exchange.router)

register_exception_handlers(app)
