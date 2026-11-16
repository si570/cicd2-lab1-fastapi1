import asyncio
import json
import os

import aio_pika
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_URL = (
    os.getenv("RABBITMQ_URL")
    or os.getenv("RABBIT_URL")
    or "amqp://labuser:labpass@localhost:5672/%2F"
)
ORDER_QUEUE = "orders"


class run:
    async def process_order(self, order):
        print(f"Received order {order['order_id']}")
        await asyncio.sleep(12)
        print(f"Processed: {order['quantity']} x {order['product']}")

    async def run(self):
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)
            queue = await channel.declare_queue(ORDER_QUEUE, durable=True)
            print("Waiting for orders...")

            async with queue.iterator() as messages:
                async for message in messages:
                    async with message.process():
                        order = json.loads(message.body.decode())
                        await self.process_order(order)


async def main():
    await run().run()


if __name__ == "__main__":
    asyncio.run(main())
