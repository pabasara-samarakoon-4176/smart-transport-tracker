from confluent_kafka import Producer
import json
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)

def send_bus_created_event(bus_data: dict):
    producer.produce('bus-events', key=str(bus_data['id']), value=json.dumps(bus_data))
    producer.flush()