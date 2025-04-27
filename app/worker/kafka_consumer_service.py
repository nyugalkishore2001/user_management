from app.worker.kafka_consumer import consume_events

def start_consumer_service():
    consume_events()

if __name__ == "__main__":
    start_consumer_service()