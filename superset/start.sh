#!/bin/bash

# Create the admin user if not already present
ADMIN_EXISTS=$(superset fab list-users | grep "admin@example.com" | wc -l)
if [ "$ADMIN_EXISTS" -eq "0" ]; then
    echo "Creating admin user..."
    superset fab create-admin \
        --username admin \
        --firstname Superset \
        --lastname Admin \
        --email admin@example.com \
        --password admin
else
    echo "Admin user already exists, skipping creation."
fi

# Start the Superset application using Gunicorn
exec gunicorn --bind 0.0.0.0:8088 --timeout 120 "superset.app:create_app()"

