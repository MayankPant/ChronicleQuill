#!/bin/bash

echo "starting entrypoint.sh"


# Wait for PostgreSQL to be ready
while ! nc -z postgres 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo 'Postgres is ready. Running Migrations'

# Run database migrations
python3 manage.py makemigrations
python3 manage.py migrate

echo "Migrations complete."

# Wait for redis to be ready
while ! nc -z redis 6379; do
  echo "Waiting for redis..."
  sleep 2
done

# Wait for rabbitmq to be ready
while ! nc -z rabbitmq 5672; do
  echo "Waiting for Rabbitmq..."
  sleep 2
done

echo  "Starting application server..."


# Start consumers in the background
python3 manage.py store_log_consumer &  # Runs in background
python3 manage.py run_websocket_consumer &  # Runs in background

# Start the Django application server in the foreground
exec python3 manage.py runserver 0.0.0.0:8001