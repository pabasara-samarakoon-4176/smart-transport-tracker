from confluent_kafka import Consumer, KafkaError
import json
from app.database import SessionLocal
from app.models.models import Alert
from app.models.models import User
from app.models.models import Bus
from datetime import datetime
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': "alert-service-group",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['bus-events'])

def consume_bus_events():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print("Error: {}".format(msg.error()))
            continue

        data = json.loads(msg.value().decode('utf-8'))
        print(f"Received bus event: {data}")

        db = SessionLocal()

        try:
            new_bus = Bus(
                id=data["id"],
                registration_no=data.get("registration_no", ""),
                route_id=data.get("route_id", 0),
                latitude=data.get("latitude", 0.0),
                longitude=data.get("longitude", 0.0),
                timestamp=datetime.utcnow()
            )
            db.add(new_bus)

            users = db.query(User).filter(User.route_id == data["route_id"]).all()
            for user in users:
                new_alert = Alert(
                    bus_id=data["id"],
                    location_id=0, 
                    user_id=user.id,
                    radius_m=0,
                    alert_triggered=True,
                    triggered_at=datetime.utcnow(),
                    message=f"A new bus ({data['registration_no']}) has been added to your route."
                )
                db.add(new_alert)
            db.commit()
            print(f"Alerts created for route {data['route_id']}")

        except Exception as e:
            db.rollback()
            print(f"Failed to create bus alert: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    consume_bus_events()