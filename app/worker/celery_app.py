from celery import Celery
import os

broker_url = f'kafka://{os.getenv("KAFKA_SERVER", "kafka:9092")}'
backend_url = None  # Kafka doesn't act as backend, results are not important here

celery_app = Celery(
    'user_management',
    broker=broker_url,
    backend=backend_url,
    broker_transport_options={'acks_late': True},
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
)

# Only import tasks AFTER celery_app is defined
from app.worker import tasks  # <-- IMPORT HERE SAFELY