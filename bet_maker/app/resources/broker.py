import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


class Producer:

    @staticmethod
    async def produce(topic: str, message: dict):
        producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
        await producer.start()
        try:
            await producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))
        except ValueError as e:
            return e
        finally:
            await producer.stop()


class Consumer:

    async def consume(self):
        consumer = AIOKafkaConsumer("bet_status", bootstrap_servers='localhost:9092')
        await consumer.start()
        try:
            async for msg in consumer:
                await self.handle(msg)
        finally:
            await consumer.stop()

    async def handle(self, message):
        print(message)