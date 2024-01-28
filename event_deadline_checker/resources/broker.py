from aiokafka import AIOKafkaProducer
import json


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
