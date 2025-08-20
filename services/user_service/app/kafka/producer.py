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

producer = create_producer()

def send_user_created_event(user_data: dict):
    topic = 'user-events'
    try:
        producer.produce(topic, key=str(user_data['id']), value=json.dumps(user_data))
        producer.flush()
        print(f"✅ Sent user welcome event to {topic}: {user_data}")
    except Exception as e:
        print(f"❌ Failed to send user welcome event: {e}")

def send_user_location_event(user_data: dict):
    topic = "user-location-updates"
    try:
        producer.produce(topic, key=str(user_data["id"]), value=json.dumps(user_data))
        producer.flush()
        print(f"✅ Sent user location event to {topic}: {user_data}")
    except Exception as e:
        print(f"❌ Failed to send user location event: {e}")