from app import main


def test_submit_order_publishes_to_rabbitmq(client, monkeypatch):
    published_orders = []

    async def publish_order(order):
        published_orders.append(order)

    monkeypatch.setattr(main, "publish_order", publish_order)

    response = client.post(
        "/orders",
        json={"order_id": 1, "product": "Laptop", "quantity": 2},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "received", "order_id": 1}
    assert published_orders[0].model_dump() == {
        "order_id": 1,
        "product": "Laptop",
        "quantity": 2,
    }


def test_submit_order_returns_503_when_rabbitmq_is_unavailable(
    client, monkeypatch
):
    async def fail_to_publish(order):
        raise OSError("Connection refused")

    monkeypatch.setattr(main, "publish_order", fail_to_publish)

    response = client.post(
        "/orders",
        json={"order_id": 1, "product": "Laptop", "quantity": 2},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "Order queue unavailable"
