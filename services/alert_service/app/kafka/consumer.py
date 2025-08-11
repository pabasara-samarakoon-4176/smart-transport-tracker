from confluent_kafka import Consumer, KafkaError
import json
from app.database import SessionLocal
from app.models.models import Alert
from datetime import datetime
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': "alert-service-group",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['user-events'])

def consume_events():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print("Error: {}".format(msg.error()))
            continue
        
        data = json.loads(msg.value().decode('utf-8'))
        print(f"Received user event: {data}")
        
        db = SessionLocal()
        try:
            welcome_alert = Alert(
                bus_id=0,
                location_id=0,
                user_id=data["id"],
                radius_m=0,
                alert_triggered=True,
                triggered_at=datetime.utcnow(),
                message=f"Welcome {data['email']} to the system!"
            )
            db.add(welcome_alert)
            db.commit()
            db.refresh(welcome_alert)
            print(f"Created welcome alert for user {data['id']}")
        except Exception as e:
            db.rollback()
            print(f"Failed to create welcome alert: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    consume_events()