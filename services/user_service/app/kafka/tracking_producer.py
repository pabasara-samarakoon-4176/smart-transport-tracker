from confluent_kafka import Producer
import json
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)

def send_user_location_event(user_data: dict):
    topic = "user_location_updates"
    try:
        producer.produce(topic, key=str(user_data["id"]), value=json.dumps(user_data))
        producer.flush()
        print(f"✅ Sent user location event to {topic}: {user_data}")
    except Exception as e:
        print(f"❌ Failed to send user location event: {e}")
