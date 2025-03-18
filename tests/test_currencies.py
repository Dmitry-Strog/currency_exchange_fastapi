import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_get_currencies(client):
    response = await client.get("/currencies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(response.json())


@pytest.mark.parametrize("code", ["USD", "RUB", "CNY"])
@pytest.mark.asyncio(loop_scope="session")
async def test_get_one_currency(client, code):
    response = await client.get(f"/currency/{code}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["code"] == code


@pytest.mark.parametrize("code", ["ABC", "XYZ", "123"])
@pytest.mark.asyncio(loop_scope="session")
async def test_currency_not_found(client, code):
    response = await client.get(f"/currency/{code}")
    assert response.status_code == 404
    assert response.json()["message"] == "Валюта не найдена"


@pytest.mark.parametrize(
    "currency",
    [
        {"code": "USD", "fullname": "US Dollar", "sign": "$"},
        {"code": "RUB", "fullname": "Russian Ruble", "sign": "₽"},
        {"code": "CNY", "fullname": "Chinese Yuan", "sign": "¥"},
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_add_duplicate_currency(client, currency):
    response = await client.post("/currencies", data=currency)
    print(response.json(), "QQQ")
    assert response.status_code == 409
    assert response.json()["message"] == "Валюта с таким кодом уже существует"


@pytest.mark.parametrize(
    "currency",
    [
        {"code": "QWE", "fullname": "QWQ", "sign": "@"},
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_add_currency(client, currency):
    response = await client.post("/currencies", data=currency)
    assert response.status_code == 201
    assert response.json()["code"] == "QWE"
    assert response.json()["fullname"] == "QWQ"
    assert response.json()["sign"] == "@"
