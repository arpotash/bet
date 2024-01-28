from aiokafka import AIOKafkaConsumer
from accounts.models import User
import asyncio
import json


class Consumer:

    def __init__(self, topic: str):
        self.topic = topic

    async def consume(self):
        consumer = AIOKafkaConsumer(self.topic, bootstrap_servers='localhost:9092')
        await consumer.start()
        try:
            async for msg in consumer:
                await self.handle(msg)
        finally:
            await consumer.stop()

    async def handle(self, message):
        decoded_message = json.loads(message.value.decode("utf-8"))
        user = await User.get(id=decoded_message.get("user"))
        if decoded_message.get("action") == "decrease":
            await user.decrease_balance(decoded_message.get("bet"))
        elif decoded_message.get("action") == "increase":
            await user.increase_balance(decoded_message.get("bet"))


async def read_kafka():
    task = asyncio.create_task(Consumer("payment").consume())
    await asyncio.gather(task)
