#!/bin/sh

# Wait until MySQL is available
echo "Waiting for MySQL..."
while ! nc -z db 3306; do
  sleep 1
done
echo "MySQL is up!"

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput


# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn polln.wsgi:application --bind 0.0.0.0:8000 --workers=4 --threads=2 --timeout=120 --log-file=-
