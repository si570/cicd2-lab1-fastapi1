import asyncio

from app import main, worker


def test_worker_uses_configured_broker_and_order_queue(monkeypatch):
    observed = {}

    class EmptyQueue:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, traceback):
            return False

        def iterator(self):
            return self

        def __aiter__(self):
            return self

        async def __anext__(self):
            raise StopAsyncIteration

    class Channel:
        async def set_qos(self, **kwargs):
            observed["qos"] = kwargs

        async def declare_queue(self, name, durable):
            observed["queue"] = (name, durable)
            return EmptyQueue()

    class Connection:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, traceback):
            return False

        async def channel(self):
            return Channel()

    async def connect_robust(url):
        observed["url"] = url
        return Connection()

    monkeypatch.setattr(worker.aio_pika, "connect_robust", connect_robust)

    asyncio.run(worker.run().run())

    assert observed["url"] == worker.RABBITMQ_URL
    assert observed["url"].startswith("amqp://")
    assert observed["queue"] == (main.ORDER_QUEUE, True)
