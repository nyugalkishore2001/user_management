from confluent_kafka import Producer
from settings.config import settings

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': settings.kafka_bootstrap_servers})

def publish_event(topic: str, key: str, value: str):
    def delivery_report(err, msg):
        if err is not None:
            print(f"Delivery failed for message {msg.key()}: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    producer.produce(topic=topic, key=key, value=value, callback=delivery_report)
    producer.flush()