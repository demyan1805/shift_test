from fastapi.testclient import TestClient


endpoint = "/api/balance"

# it's random address in avax network
reference_avax_addr = "0xE3E0863382Fe0C431D1Df3b65f881dAB49A883e3"
reference_avax_block_number = 23885270

def test_get_avax_balance_ok(
    client: TestClient,
):
    r = client.get(
        f"{endpoint}?address={reference_avax_addr}"
        f"&block_number={reference_avax_block_number}"
    )
    assert r.status_code == 200
    assert r.json() == 45346540000000000

    # at 0 block balance should be 0
    r = client.get(f"{endpoint}?address={reference_avax_addr}&block_number=0")
    assert r.status_code == 200
    assert r.json() == 0


reference_eth_addr = "0xE13137F55C32CC60a63127E62D8Ed71BE8C361ea"
reference_eth_block_number = 16227240

def test_get_eth_balance_ok(
    client: TestClient,
):
    r = client.get(
        f"{endpoint}?address={reference_eth_addr}"
        f"&block_number={reference_eth_block_number}"
        "&network=eth"
    )
    assert r.status_code == 200
    assert r.json() == 417038730000000000

    # at 0 block balance should be 0
    r = client.get(
        f"{endpoint}?address={reference_eth_addr}"
        f"&block_number=0"
        "&network=eth"
    )
    assert r.status_code == 200
    assert r.json() == 0


def test_get_balance_wrong_network(
    client: TestClient,
):
    r = client.get(
        f"{endpoint}?address={reference_avax_addr}"
        "&network=test"
    )
    assert r.status_code == 422
    data = r.json()
    assert data["detail"][0]["loc"] == ["query", "network"]
    assert data["detail"][0]["type"] == "type_error.enum"


def test_get_balance_negative_block(
    client: TestClient,
):
    r = client.get(
        f"{endpoint}?address={reference_avax_addr}"
        "&block_number=-1"
    )
    assert r.status_code == 422
    data = r.json()
    assert data["detail"][0]["loc"] == ["query", "block_number"]
    assert data["detail"][0]["type"] == "value_error.number.not_ge"


def test_get_balance_wrong_address(
    client: TestClient,
):
    r = client.get(f"{endpoint}?address=test")
    assert r.status_code == 400
    assert r.json()["detail"] == "invalid address"

