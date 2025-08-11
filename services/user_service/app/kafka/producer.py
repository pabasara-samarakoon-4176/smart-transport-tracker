from confluent_kafka import Producer
import json
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(conf)

def send_user_created_event(user_data: dict):
    producer.produce('user-events', key=str(user_data['id']), value=json.dumps(user_data))
    producer.flush()