import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_exchange_rates(client):
    response = await client.get("/exchange_rates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(response.json())


@pytest.mark.parametrize("code", ["USDRUB", "USDCNY"])
@pytest.mark.asyncio(loop_scope="session")
async def test_get_one_exchange_rates(client, code):
    response = await client.get(f"/exchange_rate/{code}")
    assert response.status_code == 200
    assert response.json()["base_currency"]["code"] == "USD"
    assert response.json()["target_currency"]["code"] == code[3:]


@pytest.mark.parametrize("code", ["QQQWWW", "WWWEEE"])
@pytest.mark.asyncio(loop_scope="session")
async def test_currency_exchange_rates_not_found(client, code):
    response = await client.get(f"/exchange_rate/{code}")
    assert response.status_code == 404
    assert response.json()["message"] == "Обменный курс для пары не найден"


@pytest.mark.parametrize(
    "exchange",
    [
        {"base_currency": "RUB", "target_currency": "CNY", "rate": "33.31"},
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_add__exchange(client, exchange):
    response = await client.post("/exchange_rates", data=exchange)
    assert response.status_code == 201
    assert response.json()["base_currency"]["code"] == "RUB"
    assert response.json()["target_currency"]["code"] == "CNY"


@pytest.mark.parametrize(
    "exchange",
    [
        {"base_currency": "USD", "target_currency": "RUB", "rate": "123.123"},
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_exchange(client, exchange):
    response = await client.post("/exchange_rates", data=exchange)
    print(response.json())
    assert response.status_code == 409
    assert response.json()["message"] == "Валютная пара с таким кодом уже существует"
