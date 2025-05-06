from confluent_kafka import Consumer
from settings.config import settings
import json
from app.worker.tasks import (
    send_verification_email_task,
    send_user_locked_email_task,
    send_user_unlocked_email_task,
    send_role_upgraded_email_task,
    send_professional_status_email_task,
)

consumer = Consumer({
    'bootstrap.servers': settings.kafka_bootstrap_servers,
    'group.id': 'email_notification_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([settings.kafka_topic_email_notifications])
consumer.subscribe(['user_unlocked'])

def consume_events():
    print("Starting Kafka consumer...")
    while True:
        msg = consumer.poll(1.0)  # timeout in seconds
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        data = json.loads(msg.value().decode('utf-8'))
        event_type = data.get("type")

        print(f"Received event: {event_type}")

        if event_type == "account_verification":
            send_verification_email_task.delay(data)
        elif event_type == "account_locked":
            send_user_locked_email_task.delay(data)
        elif event_type == "account_unlocked":
            send_user_unlocked_email_task.delay(data)
        elif event_type == "role_upgrade":
            send_role_upgraded_email_task.delay(data)
        elif event_type == "professional_status_upgrade":
            send_professional_status_email_task.delay(data)

        consumer.commit()