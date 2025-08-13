from confluent_kafka import Producer
import json
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)

def send_bus_location_event(bus_data: dict):
    topic = "bus_location_updates"
    try:
        producer.produce(topic, key=str(bus_data["id"]), value=json.dumps(bus_data))
        producer.flush()
        print(f"✅ Sent bus location event to {topic}: {bus_data}")
    except Exception as e:
        print(f"❌ Failed to send bus location event: {e}")
