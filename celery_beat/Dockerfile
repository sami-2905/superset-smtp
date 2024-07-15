FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker_app.py .
COPY beat_app.py .

CMD ["celery", "-A", "beat_app", "beat", "--loglevel=info"]

