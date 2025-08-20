from confluent_kafka import Consumer, KafkaError
from datetime import datetime
import json, math, os, time

from app.database import SessionLocal
from app.models.models import Alert, Bus, User

# Kafka config
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

def create_consumer(topics, retries=10, delay=5):
    for i in range(retries):
        try:
            conf = {
                'bootstrap.servers': bootstrap_servers,
                'group.id': "alert-service-group-2",
                'auto.offset.reset': 'earliest'
            }
            while True:
                try:
                    consumer = Consumer(conf)
                    break
                except Exception as e:
                    print(f"Kafka not ready, retrying in 3s: {e}")
                    time.sleep(3)
            # Test connection by listing topics
            consumer.list_topics(timeout=5)
            consumer.subscribe(topics)
            print("✅ Connected to Kafka and subscribed to topics:", topics)
            return consumer
        except Exception as e:
            print(f"⚠️ Kafka not ready, retrying... ({i+1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("❌ Failed to connect to Kafka after retries")

topics = ["user-events", "bus-events", "user-location-updates", "bus-location-updates"]
consumer = create_consumer(topics)

# Proximity threshold (meters)
PROXIMITY_THRESHOLD = 500


# --------------------------
# Utility functions
# --------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# --------------------------
# Handlers for each topic
# --------------------------
def handle_user_event(data):
    """Handle new user registration events"""
    db = SessionLocal()
    try:
        new_user = User(
            id=data["id"],
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data["email"],
            route_id=data.get("route_id", 0),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            timestamp=datetime.utcnow()
        )
        db.add(new_user)

        welcome_alert = Alert(
            bus_id=0,
            user_id=data["id"],
            location_id=0,
            alert_triggered=True,
            radius_m=0,
            triggered_at=datetime.utcnow(),
            message=f"Welcome {data.get('name', '')} to the system! You subscribed to route {data.get('route_id', '')}"
        )
        db.add(welcome_alert)
        db.commit()
        print(f"✅ Created welcome alert for user {data['id']}")
    except Exception as e:
        db.rollback()
        print(f"❌ Failed to create user event alert: {e}")
    finally:
        db.close()


def handle_bus_event(data):
    """Handle new bus registration events"""
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
            db.add(Alert(
                bus_id=data["id"],
                location_id=0,
                user_id=user.id,
                radius_m=0,
                alert_triggered=True,
                triggered_at=datetime.utcnow(),
                message=f"A new bus ({data['registration_no']}) has been added to your route."
            ))

        db.commit()
        print(f"✅ Created alerts for bus {data['id']} on route {data['route_id']}")
    except Exception as e:
        db.rollback()
        print(f"❌ Failed to create bus event alert: {e}")
    finally:
        db.close()


def handle_bus_location_update(data):
    """Handle bus location updates and proximity alerts"""
    db = SessionLocal()
    try:
        bus = db.query(Bus).filter(Bus.id == data["id"]).first()
        if bus:
            bus.latitude, bus.longitude = data["latitude"], data["longitude"]
            bus.timestamp = datetime.utcnow()
            db.commit()
            print(f"✅ Updated location for Bus {bus.id}")

            # Alert nearby users
            users = db.query(User).filter(User.route_id == bus.route_id).all()
            alerts = []
            for user in users:
                if user.latitude is None or user.longitude is None:
                    continue
                dist = haversine_distance(user.latitude, user.longitude, bus.latitude, bus.longitude)
                if dist <= PROXIMITY_THRESHOLD:
                    alerts.append(Alert(
                        bus_id=bus.id,
                        location_id=0,
                        user_id=user.id,
                        radius_m=0,
                        alert_triggered=True,
                        triggered_at=datetime.utcnow(),
                        message=f"The bus {bus.id} is nearby."
                    ))
            if alerts:
                db.add_all(alerts)
                db.commit()
                print(f"✅ {len(alerts)} proximity alerts created for bus {bus.id}")
        else:
            print(f"⚠️ Bus {data['id']} not found.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error handling bus location update: {e}")
    finally:
        db.close()


def handle_user_location_update(data):
    """Handle user location updates and alert if buses nearby"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == data["id"]).first()
        if user:
            user.latitude, user.longitude = data["latitude"], data["longitude"]
            user.timestamp = datetime.utcnow()
            db.commit()
            print(f"✅ Updated location for User {user.id}")

            # Check proximity to buses
            buses = db.query(Bus).filter(Bus.route_id == user.route_id).all()
            alerts = []
            for bus in buses:
                if bus.latitude is None or bus.longitude is None:
                    continue
                dist = haversine_distance(user.latitude, user.longitude, bus.latitude, bus.longitude)
                if dist <= PROXIMITY_THRESHOLD:
                    alerts.append(Alert(
                        bus_id=bus.id,
                        location_id=0,
                        user_id=user.id,
                        alert_triggered=True,
                        radius_m=0,
                        triggered_at=datetime.utcnow(),
                        message=f"The bus {bus.id} is nearby."
                    ))
            if alerts:
                db.add_all(alerts)
                db.commit()
                print(f"✅ {len(alerts)} proximity alerts created for user {user.id}")
        else:
            print(f"⚠️ User {data['id']} not found.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error handling user location update: {e}")
    finally:
        db.close()


# --------------------------
# Dispatcher
# --------------------------
handlers = {
    "user-events": handle_user_event,
    "bus-events": handle_bus_event,
    "bus-location-updates": handle_bus_location_update,
    "user-location-updates": handle_user_location_update
}


def consume_messages():
    print(f"🚀 Listening for events on topics {topics}...")
    while True:
        msg = consumer.poll(1.0)
        print(msg)
        if msg is None:
            # print("DEBUG: no message received this poll")
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(f"❌ Kafka error: {msg.error()}")
            continue

        try:
            topic = msg.topic()
            data = json.loads(msg.value().decode('utf-8'))
            print(f"📩 Received message from {topic}: {data}")

            handler = handlers.get(topic)
            if handler:
                handler(data)
            else:
                print(f"⚠️ No handler for topic {topic}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")


if __name__ == "__main__":
    try:
        consume_messages()
    except KeyboardInterrupt:
        print("🛑 Stopping consumer...")
    finally:
        consumer.close()
