from datetime import datetime
import math
import sys
from confluent_kafka import Consumer, KafkaError
import json
from app.database import SessionLocal
from app.models.models import Alert, Bus, User
import os

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
group_id = os.getenv("KAFKA_GROUP_ID", "alert_service_bus_tracking_group")
topic = os.getenv("KAFKA_BUS_TRACK_TOPIC", "bus_location_updates")

PROXIMITY_THRESHOLD = 500 

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

def haversine_distance(lat1, lon1, lat2, lon2):
    """Returns distance in meters between two lat/lon points."""
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def alert_users_for_bus(bus: Bus):
    """Alert all users on the same route if the bus is nearby."""
    db = SessionLocal()
    try:
        users_on_route = db.query(User).filter(User.route_id == bus.route_id).all()
        alerts_to_add = []

        for user in users_on_route:
            if user.latitude is None or user.longitude is None:
                continue

            distance = haversine_distance(
                float(user.latitude),
                float(user.longitude),
                float(bus.latitude),
                float(bus.longitude)
            )

            if distance <= PROXIMITY_THRESHOLD:
                alerts_to_add.append(Alert(
                    bus_id=bus.id,
                    location_id=0,  # TODO: remove this field
                    user_id=user.id,
                    radius_m=0,    # TODO: remove this field
                    alert_triggered=True,
                    triggered_at=datetime.utcnow(),
                    message=f"The bus {bus.id} is nearby."
                ))

            if alerts_to_add:
                db.add_all(alerts_to_add)
                db.commit()
                print(f"✅ Created {len(alerts_to_add)} proximity alerts for route {bus.route_id}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error in alert_users_for_bus: {e}", file=sys.stderr)
    finally:
        db.close()

def update_bus_location(bus_data: dict):
    """Update bus's location in the database."""
    db = SessionLocal()
    try:
        bus = db.query(Bus).filter(Bus.id == bus_data["id"]).first()
        if bus:
            bus.latitude = bus_data["latitude"]
            bus.longitude = bus_data["longitude"]
            bus.timestamp = datetime.utcnow()
            db.commit()
            print(f"✅ Updated location for Bus {bus.id}")
            alert_users_for_bus(bus)
        else:
            print(f"⚠️ Bus with id {bus_data['id']} not found.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating bus location: {e}", file=sys.stderr)
    finally:
        db.close()

def consume_messages():
    """Consume bus location update events and process them."""
    consumer.subscribe([topic])
    print(f"🚀 Listening for bus location updates on topic '{topic}'...")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"❌ Kafka error: {msg.error()}", file=sys.stderr)
                break
        try:
            bus_data = json.loads(msg.value().decode('utf-8'))
            update_bus_location(bus_data)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        consume_messages()
    except KeyboardInterrupt:
        print("🛑 Stopping consumer...")
    finally:
        consumer.close()