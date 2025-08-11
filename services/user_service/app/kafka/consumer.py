import os
import json
from confluent_kafka import Consumer
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USER_TOPIC = os.getenv("KAFKA_USER_TOPIC", "user-events")

consumer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "user-service-group",
    "auto.offset.reset": "earliest"
}

def consume_events():
    consumer = Consumer(consumer_config)
    consumer.subscribe([KAFKA_USER_TOPIC])

    print(f"📡 Listening to Kafka topic: {KAFKA_USER_TOPIC}")

    try:
        while True:
            msg = consumer.poll(1.0)  # Wait 1 second
            if msg is None:
                continue
            if msg.error():
                print(f"⚠ Error: {msg.error()}")
                continue

            event_data = json.loads(msg.value().decode("utf-8"))
            print(f"📩 Received event: {event_data}")
            # TODO: Process the event here

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()