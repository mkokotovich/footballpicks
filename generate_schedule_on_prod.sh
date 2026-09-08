#!/bin/bash
set -euo pipefail

# 1. Fetch the remote DATABASE_URL and swap the hostname for local Docker access
echo "Fetching DATABASE_URL from Fly..."
DB_URL=$(fly ssh console -q -C "printenv DATABASE_URL" 2>/dev/null | tr -d '\r' | sed 's|@fbpickspg.internal:5432|@host.docker.internal:15432|')

if [ -z "$DB_URL" ]; then
  echo "Error: Failed to retrieve DATABASE_URL from Fly."
  exit 1
fi
echo "Database URL configured."

# 2. Start the Fly proxy in the background
echo "Starting Fly proxy on port 15432..."
fly proxy 15432:5432 -a fbpickspg &
PROXY_PID=$!

# Ensure the background proxy process is killed when the script exits or is cancelled
trap "echo 'Stopping proxy...'; kill $PROXY_PID 2>/dev/null || true" EXIT INT TERM

# Give the proxy a moment to establish its WireGuard connection
sleep 2

# 3. Optional confirmation pause
read -p "Press [Enter] to generate the schedule against the prod database..."

# 4. Run the Django management command via docker compose
echo "Running generate_schedule inside container..."
docker compose run --rm -e DATABASE_URL="$DB_URL" django python manage.py generate_schedule

echo "Task completed successfully!"

