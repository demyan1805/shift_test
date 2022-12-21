from fastapi.testclient import TestClient

from app.models.output import ContractEvent


endpoint = "/api/contract_events"


def test_get_events_ok(
    client: TestClient,
):
    r = client.get(f"{endpoint}?from_block=0")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    for field in ContractEvent.__fields__:
        assert field in data[0]


def test_get_events_negative_block(
    client: TestClient,
):
    r = client.get(f"{endpoint}?from_block=-1")
    assert r.status_code == 422
    data = r.json()
    assert data["detail"][0]["loc"] == ["query", "from_block"]
    assert data["detail"][0]["type"] == "value_error.number.not_ge"


def test_get_events_wrong_range(
    client: TestClient,
):
    r = client.get(f"{endpoint}?from_block=2&to_block=1")
    assert r.status_code == 400
    assert r.json()["detail"] == "negative block range"


def test_get_events_different_contract(
    client: TestClient,
):
    # random contract from snowtrace, ensure on historical data
    r = client.get(
        f"{endpoint}?from_block=23482313"
        "&to_block=23482314"
        "&contract=0x333E885469d29F623681d8157A2Faad5bF4E3333"
    )
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_events_wrong_contract(
    client: TestClient,
):
    r = client.get(f"{endpoint}?from_block=0&contract=test")
    assert r.status_code == 403
    # passing snowtrace error to detail
    assert r.json()["detail"] == "Invalid Address format"
