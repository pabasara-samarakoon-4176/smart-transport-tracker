#!/bin/sh
set -e  # exit if any command fails

# Start API server in background
uvicorn app.main:app --host 0.0.0.0 --port 9003 --reload &

# Start Kafka consumer for user events in background
python -m app.kafka.consumer &

# Wait for all background processes to finish
wait
