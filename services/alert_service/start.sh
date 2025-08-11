#!/bin/sh
set -e  # exit if any command fails

# Start API server
uvicorn app.main:app --host 0.0.0.0 --port 9003 &

# Start Kafka consumer
python -m app.kafka.consumer