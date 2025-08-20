from confluent_kafka import Producer
import json
import os
import time

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

def create_producer(retries=10, delay=5):
    for i in range(retries):
        try:
            conf = {'bootstrap.servers': bootstrap_servers}
            producer = Producer(conf)
            # Test connection by listing topics (raises exception if not reachable)
            producer.list_topics(timeout=5)
            print("✅ Connected to Kafka")
            return producer
        except Exception as e:
            print(f"⚠️ Kafka not ready, retrying... ({i+1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("❌ Failed to connect to Kafka after retries")

# producer = create_producer()

def send_bus_created_event(bus_data: dict):
    topic = 'bus-events'
    producer = create_producer()
    try:
        producer.produce(topic, key=str(bus_data['id']), value=json.dumps(bus_data))
        producer.flush()
        print(f"✅ Sent bus registration event to {topic}: {bus_data}")
    except Exception as e:
        print(f"❌ Failed to send bus registration event: {e}")

def send_bus_location_event(bus_data: dict):
    topic = "bus-location-updates"
    producer = create_producer()
    try:
        producer.produce(topic, key=str(bus_data["id"]), value=json.dumps(bus_data))
        producer.flush()
        print(f"✅ Sent bus location event to {topic}: {bus_data}")
    except Exception as e:
        print(f"❌ Failed to send bus location event: {e}")