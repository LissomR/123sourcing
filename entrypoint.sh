#!/bin/bash
set -e

echo "=========================================="
echo "  Starting 123sourcing Application"
echo "=========================================="
echo "  MySQL REMOVED - Using SQLite instead"
echo "  No external database required"
echo "=========================================="

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input 2>/dev/null || true

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn api_channel.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --timeout 300 \
    --workers 2 \
    --access-logfile - \
    --error-logfile -
