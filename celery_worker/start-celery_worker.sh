#!/bin/bash
# Set environment variables for Redis and Celery
export CELERY_BROKER_URL="redis://redis:6379/0"
export CELERY_RESULT_BACKEND="redis://redis:6379/0"

# Start Celery worker with specific logging
celery -A worker_app worker --loglevel=DEBUG

