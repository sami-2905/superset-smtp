FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python dependencies file to the container
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY worker_app.py .

# Use a custom start script
COPY start-celery_worker.sh /app/start-celery_worker.sh
COPY test_email.py /app/test_email.py
RUN chmod +x /app/start-celery_worker.sh
# Create a user to run the application
RUN useradd -m celeryuser
# Change the ownership of the /app directory to the new user
RUN chown -R celeryuser:celeryuser /app
# Switch to the non-root user
USER celeryuser

# Command to run on container start
CMD ["/app/start-celery_worker.sh"]

